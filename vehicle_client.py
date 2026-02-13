import time
import requests
import json
import base64
import random
import os
import signal
import serial  # For GPS communication
# Re-using the crypto module from the server for simplicity in this demo.
# In production, these encryption keys must be securely stored on the vehicle.
from crypto import decrypt_execute 
import subprocess

SERVER_URL = "http://192.168.20.18:8085" # Server IP address
ACS_ID = "ACS03" # UNIQUE ID FOR EACH CAR

# GPS Configuration
GPS_PORT = "/dev/ttyACM0"  # GPS serial port
GPS_BAUDRATE = 38400       # GPS baud rate
GPS_TIMEOUT = 1            # Serial timeout in seconds

# Global variable to track running processes
running_process = None

# Global GPS connection
gps_serial = None
last_gps_position = {"lat": 17.5947, "lon": 78.1230}  # Fallback position

def execute_bash_command(command_str, background=False):
    """
    Executes a command within the context of .bashrc to ensure all aliases/functions are available.
    If background=True, runs the process in background and stores it globally.
    """
    global running_process
    
    try:
        # Source the run.sh script and execute the command
        # Adjust the path to your actual run.sh location
        full_cmd = f"source /home/tihan/DMRC/run_wr.sh && {command_str}"
        
        if background:
            # Start process in background
            running_process = subprocess.Popen(
                full_cmd, 
                shell=True, 
                executable='/bin/bash',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # Create new process group
            )
            print(f">>> Started in background (PID: {running_process.pid}): {full_cmd}")
            return True
        else:
            # Run synchronously
            result = subprocess.run(full_cmd, shell=True, executable='/bin/bash', capture_output=True, text=True)
            
            print(f">>> Executed: {full_cmd}")
            print(f"    Stdout: {result.stdout.strip()}")
            if result.stderr:
                print(f"    Stderr: {result.stderr.strip()}")
            return True
    except Exception as e:
        print(f"!!! Execution Error: {e}")
        return False

def parse_nmea_sentence(nmea_sentence):
    """
    Parse NMEA GNGGA sentence to extract GPS coordinates.
    Extracted from gps.py for use without ROS dependency.
    """
    data = nmea_sentence.split(',')
    
    if data[0] == "$GNGGA":
        try:
            lat_deg = float(data[2][:2])
            lat_min = float(data[2][2:])
            latitude = lat_deg + (lat_min / 60.0)
            if data[3] == 'S':
                latitude = -latitude
            
            lon_deg = float(data[4][:3])
            lon_min = float(data[4][3:])
            longitude = lon_deg + (lon_min / 60.0)
            if data[5] == 'W':
                longitude = -longitude
            
            altitude = float(data[9]) if data[9] else 0.0
            
            return latitude, longitude, altitude
        except (ValueError, IndexError):
            return None, None, None
    return None, None, None

def kill_all_processes():
    """
    Kills ONLY processes spawned by run.sh AND closes their terminal windows.
    Keeps vehicle_client.py and main terminal running.
    """
    global running_process
    
    killed_count = 0
    my_pid = os.getpid()
    terminal_pids_to_close = set()
    
    print("\n" + "="*60)
    print("STOPPING VEHICLE PROCESSES AND TERMINALS")
    print("="*60)
    
    # First, find all terminal windows spawned by run.sh processes
    print(">>> Finding terminal windows to close...")
    try:
        # Get all processes and find terminals spawned by run.sh
        ps_output = subprocess.run(
            ['ps', 'aux'], 
            capture_output=True, text=True
        ).stdout
        
        for line in ps_output.split('\n'):
            # Look for gnome-terminal processes
            if 'gnome-terminal' in line and 'tihan' in line:
                parts = line.split()
                if len(parts) > 1:
                    try:
                        pid = int(parts[1])
                        # Check if this terminal is related to PHASE1/run.sh
                        # by checking its children
                        children = subprocess.run(
                            ['pgrep', '-P', str(pid)],
                            capture_output=True, text=True
                        ).stdout.strip()
                        
                        if children:
                            for child_pid in children.split('\n'):
                                # Check if child is running something from PHASE1
                                cmdline = subprocess.run(
                                    ['ps', '-p', child_pid, '-o', 'cmd='],
                                    capture_output=True, text=True
                                ).stdout
                                
                                if 'PHASE1' in cmdline or 'run.sh' in cmdline:
                                    terminal_pids_to_close.add(pid)
                                    print(f"    Found terminal to close: PID {pid}")
                                    break
                    except (ValueError, IndexError):
                        pass
    except Exception as e:
        print(f"!!! Error finding terminals: {e}")
    
    # Method 1: Kill the tracked process group (most important)
    if running_process and running_process.poll() is None:
        try:
            pgid = os.getpgid(running_process.pid)
            print(f">>> Killing process group {pgid} (run.sh and children)...")
            os.killpg(pgid, signal.SIGKILL)
            killed_count += 1
            print(f">>> Successfully killed process group {pgid}")
        except Exception as e:
            print(f"!!! Error killing tracked process: {e}")
    else:
        print(">>> No tracked process running")
    
    # Method 2: Kill processes matching run.sh path
    print(">>> Killing run.sh processes...")
    try:
        result = subprocess.run(['pkill', '-9', '-f', '/home/tihan/PHASE1/run.sh'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f">>> Killed run.sh processes")
            killed_count += 1
    except Exception as e:
        pass
    
    # Method 3: Kill ROS/RViz processes (if spawned by run.sh)
    print(">>> Killing ROS/RViz processes...")
    for process_name in ['rviz', 'roscore', 'rosmaster', 'roslaunch', 'rosrun']:
        try:
            result = subprocess.run(['pkill', '-9', process_name], capture_output=True)
            if result.returncode == 0:
                print(f"    Killed {process_name}")
        except:
            pass
    
    # Method 4: Close terminal windows that were spawned by run.sh
    print(">>> Closing terminal windows...")
    closed_terminals = 0
    
    # Method 4a: Close terminals by PID
    for term_pid in terminal_pids_to_close:
        try:
            # Don't close our own terminal
            my_terminal = subprocess.run(
                ['ps', '-o', 'ppid=', '-p', str(my_pid)],
                capture_output=True, text=True
            ).stdout.strip()
            
            if str(term_pid) != my_terminal:
                os.kill(term_pid, signal.SIGTERM)
                print(f"    Closed terminal window: PID {term_pid}")
                closed_terminals += 1
        except (ProcessLookupError, PermissionError) as e:
            pass
    
    # Method 4b: Use wmctrl to close terminal windows with PHASE1 in title (if available)
    try:
        result = subprocess.run(
            ['wmctrl', '-l'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'PHASE1' in line or 'run.sh' in line:
                    # Extract window ID (first column)
                    parts = line.split()
                    if parts:
                        window_id = parts[0]
                        subprocess.run(['wmctrl', '-i', '-c', window_id], capture_output=True)
                        print(f"    Closed window: {window_id}")
                        closed_terminals += 1
    except FileNotFoundError:
        # wmctrl not installed, skip
        pass
    except Exception as e:
        pass
    
    if closed_terminals > 0:
        killed_count += closed_terminals
        print(f"    Total terminals closed: {closed_terminals}")
    else:
        print(f"    No additional terminals to close")
    
    # Wait for cleanup
    time.sleep(0.5)
    
    running_process = None
    print(f">>> Stop complete. Killed {killed_count} process groups/terminals")
    print("="*60 + "\n")
    return True

def get_gps_data():
    """
    Read real GPS data from serial port.
    Parses NMEA sentences and returns current position.
    Falls back to last known position if GPS unavailable.
    """
    global gps_serial, last_gps_position
    
    # Try to read from GPS
    if gps_serial and gps_serial.is_open:
        try:
            # Read multiple lines to find GNGGA sentence
            for _ in range(10):  # Try up to 10 lines
                line = gps_serial.readline().decode('ascii', errors='replace').strip()
                
                if line.startswith("$GNGGA"):
                    lat, lon, alt = parse_nmea_sentence(line)
                    
                    if lat is not None and lon is not None:
                        # Update last known position
                        last_gps_position = {"lat": lat, "lon": lon}
                        
                        return {
                            "acs_id": ACS_ID,
                            "lat": lat,
                            "lon": lon,
                            "status": "Running" if running_process else "Stopped",
                            "path": "Active-Path"
                        }
        except (serial.SerialException, UnicodeDecodeError) as e:
            print(f"[GPS] Read error: {e}")
    
    # Fallback to last known position
    return {
        "acs_id": ACS_ID,
        "lat": last_gps_position["lat"],
        "lon": last_gps_position["lon"],
        "status": "Running" if running_process else "Stopped",
        "path": "Active-Path"
    }

def main():
    global gps_serial
    
    print(f"Vehicle Client Started for {ACS_ID}")
    print("="*60)
    
    # Initialize GPS connection
    try:
        print(f"[GPS] Connecting to GPS on {GPS_PORT} at {GPS_BAUDRATE} baud...")
        gps_serial = serial.Serial(GPS_PORT, GPS_BAUDRATE, timeout=GPS_TIMEOUT)
        time.sleep(1)  # Wait for GPS to initialize
        print(f"[GPS] Connected successfully!")
    except serial.SerialException as e:
        print(f"[GPS] WARNING: Could not connect to GPS: {e}")
        print(f"[GPS] Will use fallback position: {last_gps_position}")
        gps_serial = None
    
    print("="*60)
    print()
    
    while True:
        # 1. Send GPS Data to Server
        try:
            gps_data = get_gps_data()
            resp = requests.post(f"{SERVER_URL}/api/vehicle/update", json=gps_data, timeout=2)
            if resp.status_code == 200:
                print(f"[GPS] Updated: Lat={gps_data['lat']:.6f}, Lon={gps_data['lon']:.6f}, Status={gps_data['status']}")
        except Exception as e:
            print(f"[GPS] Update Error: {e}")
        
        # 2. Poll for Commands
        try:
            resp = requests.get(f"{SERVER_URL}/api/vehicle/command/{ACS_ID}", timeout=2)
            if resp.status_code == 200:
                data = resp.json()
                encrypted_cmd = data.get("command")
                
                if encrypted_cmd:
                    print(f"\n[COMMAND] Received encrypted command: {encrypted_cmd[:50]}...")
                    
                    # 3. Decrypt and Execute
                    try:
                        decrypted_data = decrypt_execute(encrypted_cmd)
                        print(f"[DECRYPT] Command decrypted successfully")
                        print(f"[DECRYPT] ACS ID: {decrypted_data.get('acs_id')}")
                        print(f"[DECRYPT] Path: {decrypted_data.get('path')}")
                        print(f"[DECRYPT] Action: {decrypted_data.get('action')}")
                        
                        # Execute the bash command based on action
                        action = decrypted_data.get('action')
                        path = decrypted_data.get('path')
                        
                        if action == 'start':
                            # Kill any existing processes first
                            print(f"[ACTION] Stopping any existing processes before starting...")
                            kill_all_processes()
                            
                            # Start the run.sh script in background
                            print(f"[ACTION] Starting vehicle on path: {path}")
                            # Execute the actual run.sh script
                            cmd = f"bash /home/tihan/PHASE1/run.sh"
                            execute_bash_command(cmd, background=True)
                            print(f"[ACTION] Vehicle started successfully")
                            
                        elif action == 'stop':
                            # Kill all running processes
                            print(f"[ACTION] Stopping vehicle and killing all processes...")
                            success = kill_all_processes()
                            if success:
                                print(f"[ACTION] Vehicle stopped successfully")
                            else:
                                print(f"[ACTION] No processes were running")
                        else:
                            print(f"[WARN] Unknown action: {action}")
                            
                    except Exception as e:
                        print(f"[ERROR] Decryption/Execution failed: {e}")
                        
        except Exception as e:
            print(f"[COMMAND] Poll Error: {e}")
            
        # Fast polling for smooth live tracking (5 updates per second)
        time.sleep(0.2)

if __name__ == "__main__":
    main()
