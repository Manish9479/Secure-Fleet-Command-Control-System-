import threading
import time
import random
import os
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from crypto import encrypt_command, decrypt_execute

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Simulated Car Data - LIMITED TO 3 CARS
# [INTEGRATION POINT]
# Replace this 'CARS' dictionary with a database call or Firebase listener.
# In a real scenario, your Android app pushes GPS data to Firebase/DB,
# and this Flask app should query that DB to populate this 'CARS' object.
# Updated to TiHAN IITH Coordinates
CARS = {
    "ACS01": {"lat": 17.601838, "lon": 78.126866, "status": "Stopped", "path": "Path-A"},
    "ACS02": {"lat": 17.601938, "lon": 78.126966, "status": "Stopped", "path": "Path-B"},
    "ACS03": {"lat": 17.601738, "lon": 78.126766, "status": "Stopped", "path": "Path-C"},
}

# Store pending commands for vehicles to fetch
# Key: acs_id, Value: list of encrypted command strings
PENDING_COMMANDS = {}

# Simulation Thread to move cars
def simulate_movement():
    while True:
        for car_id, data in CARS.items():
            if data["status"] == "Running":
                # Add random small movement
                data["lat"] += random.uniform(-0.00005, 0.00005)
                data["lon"] += random.uniform(-0.00005, 0.00005)
        time.sleep(1)

simulation_thread = threading.Thread(target=simulate_movement, daemon=True)
simulation_thread.start()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Hardcoded admin credentials for demo
        if username == "admin" and password == "admin123":
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error="Invalid Credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('admin.html')

# API Endpoints for UI
@app.route('/api/data')
def get_data():
    return jsonify(CARS)

@app.route('/api/control', methods=['POST'])
def control_car():
    if not session.get('logged_in'):
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    
    data = request.json
    acs_id = data.get('acs_id')
    action = data.get('action') # 'start' or 'stop'
    path = data.get('path', 'default_path')

    if acs_id in CARS:
        # 1. Encrypt Command
        encrypted_command = encrypt_command(acs_id, path, action)
        
        # 2. Store for Vehicle to Fetch
        if acs_id not in PENDING_COMMANDS:
            PENDING_COMMANDS[acs_id] = []
        PENDING_COMMANDS[acs_id].append(encrypted_command)
        
        # 3. Optimistic UI Update (Simulation)
        if action == "start":
            CARS[acs_id]["status"] = "Running"
        elif action == "stop":
            CARS[acs_id]["status"] = "Stopped"
            
        return jsonify({
            "status": "success", 
            "car_status": CARS[acs_id]["status"],
            "encrypted_payload": encrypted_command,
            "decrypted_log": {"raw_command": "Command Queued for Vehicle Fetch"} 
        })
            
    return jsonify({"status": "error", "message": "Car not found"}), 404

# API Endpoints for VEHICLES
@app.route('/api/vehicle/update', methods=['POST'])
def vehicle_update():
    """
    Endpoint for Vehicle Client to push GPS data.
    Expected JSON: {"acs_id": "ACS01", "lat": 17.5, "lon": 78.1, "status": "Running", "path": "Path-A"}
    """
    data = request.json
    acs_id = data.get('acs_id')
    
    if acs_id:
        CARS[acs_id] = {
            "lat": float(data.get('lat', 0)),
            "lon": float(data.get('lon', 0)),
            "status": data.get('status', 'Unknown'),
            "path": data.get('path', 'Unknown')
        }
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Missing acs_id"}), 400

@app.route('/api/vehicle/command/<acs_id>', methods=['GET'])
def get_vehicle_command(acs_id):
    """
    Endpoint for Vehicle Client to poll for commands.
    Returns: {"command": "encrypted_string"} or {"command": null}
    """
    if acs_id in PENDING_COMMANDS and PENDING_COMMANDS[acs_id]:
        cmd = PENDING_COMMANDS[acs_id].pop(0)
        return jsonify({"command": cmd})
    return jsonify({"command": None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
