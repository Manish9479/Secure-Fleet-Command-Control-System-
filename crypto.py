import base64
import json
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Hardcoded key for demonstration (In production, use secure key management)
# 32 bytes for AES-256
SECRET_KEY = b'0123456789ABCDEF0123456789ABCDEF' 
IV = b'0000000000000000' # 16 bytes IV

def encrypt_command(acs_id, path, action):
    """
    Encrypts a command structure: acsno + testbed(path) + excuter.py + action
    Returns base64 encoded string.
    """
    # Construct the command payload as requested
    # Structure: acsno|path|action|excuter.py
    # Using pipe | as separator for simplicity in parsing
    payload = f"{acs_id}|{path}|{action}|excuter.py"
    
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    encrypted_bytes = cipher.encrypt(pad(payload.encode('utf-8'), AES.block_size))
    
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def decrypt_execute(encrypted_data):
    """
    Decrypts the command and returns the components.
    Simulates the "execution" by printing/logging.
    """
    try:
        encrypted_bytes = base64.b64decode(encrypted_data)
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        decrypted_str = decrypted_bytes.decode('utf-8')
        
        # Parse the payload
        parts = decrypted_str.split('|')
        if len(parts) != 4:
            return {"status": "error", "message": "Invalid payload structure"}
            
        acs_id = parts[0]
        path = parts[1]
        action = parts[2]
        script = parts[3]
        
        return {
            "status": "success",
            "acs_id": acs_id,
            "path": path,
            "action": action,
            "script": script,
            "raw_command": f"bashrc run {script} on {acs_id} for {path} with action {action}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Test
    enc = encrypt_command("ACS01", "/path/to/waypoint", "start")
    print(f"Encrypted: {enc}")
    dec = decrypt_execute(enc)
    print(f"Decrypted: {dec}")
