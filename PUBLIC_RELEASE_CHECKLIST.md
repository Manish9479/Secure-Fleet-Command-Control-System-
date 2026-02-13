# ⚠️ PUBLIC RELEASE CHECKLIST

Before pushing to GitHub, you MUST clean proprietary references from your code.

## 🔍 Files Requiring Manual Review

The following files contain references to:
- Local paths (`/home/tihan/`, `/home/tihan40903/`)
- Project-specific names (`PHASE1`, `DMRC`, `TiHAN`)
- Local IP addresses (`192.168.x.x`)

### Files to Review:

1. **vehicle_client.py**
   - Line 14: `SERVER_URL = "http://192.168.20.18:8085"`
   - Line 39: `source /home/tihan/DMRC/run_wr.sh`
   - Line 165: `'/home/tihan/PHASE1/run.sh'`
   - Line 340: `bash /home/tihan/PHASE1/run.sh`
   - Replace with generic placeholders or environment variables

2. **flutter_app/lib/main.dart**
   - Line 10: `const String SERVER_URL = "http://192.168.20.179:5000"`
   - Replace with placeholder or configuration instructions

3. **app.py**
   - Lines 17-20: TiHAN IITH coordinates (optional - can keep as example)
   - Lines 50-51: Hardcoded admin credentials (already documented)

## 🛠️ Required Changes

### 1. Update vehicle_client.py

**Replace:**
```python
SERVER_URL = "http://192.168.20.18:8085"
```

**With:**
```python
SERVER_URL = os.getenv('SERVER_URL', 'http://YOUR_SERVER_IP:5000')
```

---

**Replace:**
```python
full_cmd = f"source /home/tihan/DMRC/run_wr.sh && {command_str}"
```

**With:**
```python
# Path to your vehicle initialization script
INIT_SCRIPT_PATH = os.getenv('INIT_SCRIPT_PATH', '/path/to/your/init.sh')
full_cmd = f"source {INIT_SCRIPT_PATH} && {command_str}"
```

---

**Replace:**
```python
result = subprocess.run(['pkill', '-9', '-f', '/home/tihan/PHASE1/run.sh'],
```

**With:**
```python
RUN_SCRIPT_PATH = os.getenv('RUN_SCRIPT_PATH', '/path/to/your/run.sh')
result = subprocess.run(['pkill', '-9', '-f', RUN_SCRIPT_PATH],
```

---

**Replace:**
```python
cmd = f"bash /home/tihan/PHASE1/run.sh"
```

**With:**
```python
cmd = f"bash {RUN_SCRIPT_PATH}"
```

### 2. Update flutter_app/lib/main.dart

**Replace:**
```dart
const String SERVER_URL = "http://192.168.20.179:5000";
```

**With:**
```dart
// CONFIGURATION: Update this to your Flask server address
// For local development: http://YOUR_LOCAL_IP:5000
// For Android emulator (host machine): http://10.0.2.2:5000
// For production: https://your-domain.com
const String SERVER_URL = "http://YOUR_SERVER_IP:5000";
```

### 3. Add to .env.example

Add these new environment variables:

```bash
# ============================================
# VEHICLE CLIENT - CUSTOM SCRIPT PATHS
# ============================================

# Path to vehicle initialization script
INIT_SCRIPT_PATH=/path/to/your/init.sh

# Path to vehicle run script
RUN_SCRIPT_PATH=/path/to/your/run.sh
```

## ✅ Automated Search Commands

Run these to find remaining references:

```bash
# Search for proprietary names
grep -r "tihan" --include="*.py" --include="*.dart" .

# Search for specific paths
grep -r "PHASE1\|DMRC" --include="*.py" .

# Search for local IPs
grep -r "192\.168\." --include="*.py" --include="*.dart" .

# Search for hardcoded coordinates (optional)
grep -r "17\.60" --include="*.py" --include="*.html" .
```

## 📝 Replacement Strategy

### Option 1: Environment Variables (Recommended)
```python
import os
SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:5000')
```

### Option 2: Configuration File
```python
# config.py
SERVER_URL = "http://localhost:5000"
INIT_SCRIPT_PATH = "/path/to/init.sh"
```

### Option 3: Command Line Arguments
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--server-url', default='http://localhost:5000')
```

## 🎯 Final Verification

Before `git push`:

1. **Remove all personal paths**
   - No `/home/tihan/` references
   - No `/home/tihan40903/` references

2. **Remove all local network IPs**
   - No `192.168.x.x` addresses
   - Replace with placeholders or config

3. **Remove proprietary project names**
   - No `PHASE1` references
   - No `DMRC` references
   - No `TiHAN` in code (OK in comments as example location)

4. **Test with fresh clone**
   ```bash
   cd /tmp
   git clone /path/to/your/repo test-clone
   cd test-clone
   grep -r "tihan\|PHASE1\|DMRC\|192\.168" .
   # Should return NO results in code files
   ```

## 🚀 Ready to Publish When:

- [ ] All proprietary paths removed
- [ ] All local IPs replaced with placeholders
- [ ] All hardcoded credentials documented as demo-only
- [ ] .env.example includes all new environment variables
- [ ] README updated with configuration instructions
- [ ] Git repository initialized
- [ ] .gitignore prevents sensitive files
- [ ] No personal information in commit history

---

**After completing these steps, your project will be 100% public-ready!** 🎉
