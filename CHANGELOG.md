# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Database integration (PostgreSQL/MongoDB)
- WebSocket support for real-time updates
- Multi-user authentication with roles
- Historical path playback
- Geofencing and alerts
- Telemetry data logging
- Docker containerization
- RSA public key infrastructure
- Vehicle health monitoring

## [1.0.0] - 2026-02-13

### Added
- Initial release of Secure Fleet Command & Control System
- **Core Features**:
  - AES-256 encrypted command transmission
  - Real-time GPS tracking with 5Hz update rate
  - Web dashboard with satellite imagery (Leaflet.js + Esri tiles)
  - Admin panel for secure vehicle control
  - Flask REST API server
  - Python vehicle client with GPS integration
  - Flutter mobile app (iOS/Android support)
  - Session-based authentication
  
- **Security**:
  - End-to-end AES-256-CBC encryption
  - Base64 payload encoding
  - Custom encrypted protocol (acsno|path|action|script)
  - Admin authentication system
  
- **Vehicle Client**:
  - Automatic GPS data transmission via serial port
  - NMEA sentence parsing (GNGGA format)
  - Command polling and execution
  - Process lifecycle management
  - Fallback positioning
  - Serial GPS hardware support
  
- **Web Interface**:
  - Live fleet monitoring on satellite map
  - Real-time vehicle status updates (300ms polling)
  - Running/stopped vehicle filtering
  - Detailed vehicle cards with GPS coordinates
  - Responsive design for mobile viewing
  
- **Mobile App**:
  - Dark mode UI with modern design
  - Interactive map with vehicle markers
  - Start/stop vehicle controls
  - Path selection dropdown
  - Real-time status cards
  - Cross-platform support (iOS/Android)
  
- **API Endpoints**:
  - `GET /api/data` - Public vehicle data
  - `POST /api/control` - Send encrypted commands (authenticated)
  - `POST /api/vehicle/update` - Vehicle GPS updates
  - `GET /api/vehicle/command/<id>` - Command polling
  - `GET /` - Public dashboard
  - `GET /login` - Admin login
  - `GET /admin` - Admin control panel
  
- **Documentation**:
  - Comprehensive README with features and usage
  - SECURITY.md with vulnerability reporting process
  - CONFIGURATION.md with production setup guides
  - CONTRIBUTING.md with development guidelines
  - .env.example with configuration template
  - MIT License with security disclaimers

### Security Notes

⚠️ **IMPORTANT**: Version 1.0.0 uses demonstration credentials and keys:
- Default admin credentials: `admin` / `admin123`
- Hardcoded AES keys in `crypto.py`
- HTTP-only communication (no TLS)

**These MUST be changed before production deployment!** See [SECURITY.md](SECURITY.md).

### Known Limitations

- No database persistence (in-memory only)
- Limited to 3 vehicles by default (easily expandable)
- No command replay attack prevention
- No vehicle authentication
- Hardcoded credentials
- HTTP-only (no HTTPS)
- No audit logging

### Dependencies

- Flask 3.0.0
- PyCryptodome 3.19.0
- Requests 2.31.0
- pySerial 3.5
- Flutter 3.0+ (for mobile app)
- Leaflet.js (frontend)

---

## Version History

### Versioning Format

- **Major.Minor.Patch** (e.g., 1.2.3)
  - **Major**: Breaking changes
  - **Minor**: New features (backward compatible)
  - **Patch**: Bug fixes (backward compatible)

### Upgrade Guide

When upgrading between versions:

1. **Read CHANGELOG** for breaking changes
2. **Backup database** (when implemented)
3. **Update dependencies**: `pip install -U -r requirements.txt`
4. **Check CONFIGURATION.md** for new settings
5. **Run tests** (when implemented)
6. **Deploy to staging** first
7. **Monitor logs** after production deployment

---

## Release Notes Template

```markdown
## [Version] - YYYY-MM-DD

### Added
- New features and capabilities

### Changed
- Modifications to existing features

### Deprecated
- Soon-to-be removed features

### Removed
- Deleted features

### Fixed
- Bug fixes

### Security
- Security improvements and patches
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute to this project.

[Unreleased]: https://github.com/your-repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/your-repo/releases/tag/v1.0.0
