# Configuration Guide

This guide explains how to properly configure the Secure Fleet Command & Control System for your specific deployment.

## Table of Contents

- [Server Configuration](#server-configuration)
- [Vehicle Client Configuration](#vehicle-client-configuration)
- [Security Configuration](#security-configuration)
- [Network Configuration](#network-configuration)
- [GPS Configuration](#gps-configuration)
- [Mobile App Configuration](#mobile-app-configuration)

---

## Server Configuration

### Environment Variables (Recommended for Production)

Create a `.env` file in the project root:

```bash
# Flask Configuration
FLASK_SECRET_KEY=your-super-secret-key-minimum-32-chars
FLASK_ENV=production
FLASK_DEBUG=False

# Server Settings
HOST=0.0.0.0
PORT=5000

# Database (if implementing)
DATABASE_URL=postgresql://user:password@localhost/fleet_db

# Encryption Keys (Base64 encoded)
AES_SECRET_KEY=base64_encoded_32_byte_key_here
AES_IV=base64_encoded_16_byte_iv_here

# Admin Credentials (temporary - replace with database)
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=hashed_password_here
```

### Generating Secure Keys

```python
# Run this once to generate secure keys
import os
import base64

# Generate AES-256 key (32 bytes)
secret_key = os.urandom(32)
print(f"AES_SECRET_KEY={base64.b64encode(secret_key).decode()}")

# Generate IV (16 bytes)
iv = os.urandom(16)
print(f"AES_IV={base64.b64encode(iv).decode()}")

# Generate Flask secret key
flask_key = os.urandom(32)
print(f"FLASK_SECRET_KEY={base64.b64encode(flask_key).decode()}")
```

Save these keys securely and never commit them to version control!

### Updating crypto.py for Production

```python
import os
import base64

# Load from environment variables
SECRET_KEY = base64.b64decode(os.getenv('AES_SECRET_KEY'))
IV = base64.b64decode(os.getenv('AES_IV'))
```

### Updating app.py for Production

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Use environment variables for credentials
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD_HASH = os.getenv('ADMIN_PASSWORD_HASH')
```

---

## Vehicle Client Configuration

### Per-Vehicle Settings

Each vehicle needs unique configuration in `vehicle_client.py`:

```python
# Server Connection
SERVER_URL = os.getenv('SERVER_URL', 'http://192.168.1.100:5000')

# Unique Vehicle Identifier (MUST be unique per vehicle)
ACS_ID = os.getenv('ACS_ID', 'ACS01')  # Change for each vehicle

# GPS Hardware Configuration
GPS_PORT = os.getenv('GPS_PORT', '/dev/ttyACM0')
GPS_BAUDRATE = int(os.getenv('GPS_BAUDRATE', '38400'))
GPS_TIMEOUT = int(os.getenv('GPS_TIMEOUT', '1'))

# Fallback Position (if GPS unavailable)
FALLBACK_LAT = float(os.getenv('FALLBACK_LAT', '17.5947'))
FALLBACK_LON = float(os.getenv('FALLBACK_LON', '78.1230'))

# Polling Interval (seconds)
POLL_INTERVAL = float(os.getenv('POLL_INTERVAL', '0.2'))
```

### Creating Vehicle-Specific .env Files

For each vehicle, create a `.env` file:

```bash
# Vehicle ACS01 Configuration
ACS_ID=ACS01
SERVER_URL=http://192.168.1.100:5000
GPS_PORT=/dev/ttyACM0
GPS_BAUDRATE=38400
FALLBACK_LAT=17.601838
FALLBACK_LON=78.126866
```

---

## Security Configuration

### Step 1: Password Hashing

Install werkzeug (already included with Flask):

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Generate password hash
password_hash = generate_password_hash('your_secure_password', method='pbkdf2:sha256')
print(password_hash)
```

Update `app.py`:

```python
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Fetch from database in production
    if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
        session['logged_in'] = True
        return redirect(url_for('admin'))
```

### Step 2: HTTPS Configuration

Use a reverse proxy like nginx or Caddy:

**nginx configuration:**

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 3: Rate Limiting

Install Flask-Limiter:

```bash
pip install Flask-Limiter
```

Add to `app.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Prevent brute force
def login():
    # ... existing code
```

---

## Network Configuration

### Firewall Rules (iptables)

```bash
# Allow Flask server port from specific subnet only
sudo iptables -A INPUT -p tcp --dport 5000 -s 192.168.1.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5000 -j DROP

# Save rules
sudo iptables-save > /etc/iptables/rules.v4
```

### Vehicle Network Configuration

For production deployments, use VPN:

**WireGuard Configuration Example:**

```ini
# Server: /etc/wireguard/wg0.conf
[Interface]
PrivateKey = SERVER_PRIVATE_KEY
Address = 10.0.0.1/24
ListenPort = 51820

[Peer]
# Vehicle ACS01
PublicKey = ACS01_PUBLIC_KEY
AllowedIPs = 10.0.0.101/32

[Peer]
# Vehicle ACS02
PublicKey = ACS02_PUBLIC_KEY
AllowedIPs = 10.0.0.102/32
```

Update `SERVER_URL` in vehicle clients:

```python
SERVER_URL = "http://10.0.0.1:5000"  # VPN IP
```

---

## GPS Configuration

### Supported GPS Modules

- **u-blox NEO-M8N** (recommended)
- **u-blox NEO-6M**
- **GlobalTop PA6H**
- Any module outputting NMEA sentences

### Serial Port Detection

```bash
# List available serial ports
ls /dev/tty*

# Most common GPS ports:
# - /dev/ttyACM0
# - /dev/ttyUSB0
# - /dev/serial0 (Raspberry Pi)

# Check GPS output
cat /dev/ttyACM0
# Should show NMEA sentences like:
# $GNGGA,123519.00,1735.1234,N,07812.5678,E,1,08,0.9,545.4,M,46.9,M,,*47
```

### Baud Rate Configuration

Common baud rates:
- 9600 (default for many modules)
- 38400 (u-blox default)
- 115200 (high-speed modules)

Update in `vehicle_client.py`:

```python
GPS_BAUDRATE = 38400  # Match your GPS module
```

### Testing GPS Functionality

```python
# Test script - save as test_gps.py
import serial
import time

GPS_PORT = "/dev/ttyACM0"
GPS_BAUDRATE = 38400

gps = serial.Serial(GPS_PORT, GPS_BAUDRATE, timeout=1)
print("Reading GPS data for 10 seconds...")

start = time.time()
while time.time() - start < 10:
    line = gps.readline().decode('ascii', errors='replace').strip()
    if line.startswith('$GNGGA'):
        print(line)

gps.close()
```

---

## Mobile App Configuration

### Flutter App Settings

Edit `flutter_app/lib/main.dart`:

```dart
// PRODUCTION Configuration
const String SERVER_URL = "https://your-domain.com";  // Use HTTPS!

// For local testing
// const String SERVER_URL = "http://192.168.1.100:5000";

// For Android emulator testing (host machine)
// const String SERVER_URL = "http://10.0.2.2:5000";
```

### Android Network Permissions

`android/app/src/main/AndroidManifest.xml`:

```xml
<manifest>
    <!-- Add internet permission -->
    <uses-permission android:name="android.permission.INTERNET"/>
    
    <!-- For HTTP (cleartext) traffic in debug mode only -->
    <application
        android:usesCleartextTraffic="true"
        ...>
    </application>
</manifest>
```

> ⚠️ Remove `usesCleartextTraffic` for production builds!

### iOS Network Configuration

`ios/Runner/Info.plist`:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <!-- For development only - remove for production -->
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

---

## Default Vehicle Locations

Update initial vehicle positions in `app.py`:

```python
CARS = {
    "ACS01": {
        "lat": YOUR_LAT,      # Replace with your coordinates
        "lon": YOUR_LON,      # Replace with your coordinates
        "status": "Stopped",
        "path": "Path-A"
    },
    # Add more vehicles as needed
}
```

### Finding Your Coordinates

1. Go to [Google Maps](https://maps.google.com)
2. Right-click on your location
3. Click coordinates to copy
4. Format: `lat, lon` (e.g., 17.601838, 78.126866)

---

## Path Configuration

Define custom paths for your vehicles in `vehicle_client.py` or database:

```python
# Example path definitions
PATHS = {
    "Path-A": {
        "waypoints": [(17.601, 78.126), (17.602, 78.127)],
        "speed": 5.0,  # m/s
        "description": "Main route"
    },
    "Path-Testing": {
        "waypoints": [(17.601, 78.126)],  # Single waypoint for testing
        "speed": 2.0,
        "description": "Test loop"
    }
}
```

---

## Scaling Configuration

### Multiple Servers (Load Balancing)

Use Redis for shared state:

```bash
pip install redis flask-session
```

```python
from flask_session import Session
import redis

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
Session(app)
```

### Database Integration

For production, replace in-memory `CARS` dict with database:

```python
# Example with SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

class Vehicle(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    status = db.Column(db.String(20))
    path = db.Column(db.String(50))
    last_update = db.Column(db.DateTime)
```

---

## Monitoring Configuration

### Logging

Add to `app.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('fleet.log', maxBytes=10000000, backupCount=3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

@app.route('/api/control', methods=['POST'])
def control_car():
    app.logger.info(f"Command received: {request.json}")
    # ... existing code
```

### Health Check Endpoint

```python
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "vehicles_online": len([v for v in CARS.values() if v['status'] == 'Running']),
        "timestamp": time.time()
    })
```

---

## Troubleshooting Configuration Issues

### Issue: Vehicle can't connect to server

**Check:**
1. Server is running: `curl http://SERVER_IP:5000/health`
2. Firewall allows connections: `sudo iptables -L`
3. `SERVER_URL` matches actual IP
4. Network connectivity: `ping SERVER_IP`

### Issue: GPS not working

**Check:**
1. Port exists: `ls -l /dev/ttyACM0`
2. Permissions: `sudo chmod 666 /dev/ttyACM0`
3. Module connected: `dmesg | grep tty`
4. Baud rate matches: Try different rates (9600, 38400, 115200)

### Issue: Commands not executing

**Check:**
1. Encryption keys match on server and client
2. `ACS_ID` exists in server's `CARS` dictionary
3. Vehicle is polling: Check logs
4. No firewall blocking responses

---

## Quick Start Checklist

- [ ] Generate secure encryption keys
- [ ] Update `crypto.py` with new keys
- [ ] Change admin credentials in `app.py`
- [ ] Set `FLASK_SECRET_KEY` environment variable
- [ ] Configure vehicle IDs uniquely per vehicle
- [ ] Update GPS port and baud rate
- [ ] Set server URL in vehicle clients
- [ ] Configure firewall rules
- [ ] Enable HTTPS in production
- [ ] Test GPS functionality
- [ ] Test command encryption/decryption
- [ ] Configure mobile app server URL
- [ ] Set up monitoring and logging
- [ ] Create backup of encryption keys
- [ ] Document your specific configuration

---

**For additional help, see [SECURITY.md](SECURITY.md) for security best practices.**
