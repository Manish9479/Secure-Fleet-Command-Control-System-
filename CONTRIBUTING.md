# Contributing to Secure Fleet Command & Control System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)
- [Documentation](#documentation)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:
- Experience level
- Gender identity and expression
- Sexual orientation
- Disability
- Personal appearance
- Race or ethnicity
- Age
- Religion or lack thereof

### Our Standards

**Positive behaviors:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards others

**Unacceptable behaviors:**
- Harassment, trolling, or personal attacks
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**Good bug reports include:**
- Clear and descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, etc.)
- Error messages and logs

**Template:**

```markdown
**Description:**
Brief description of the bug

**Steps to Reproduce:**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.10.5]
- Flask: [e.g., 3.0.0]

**Additional Context:**
Any other relevant information
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**Good enhancement suggestions include:**
- Clear use case
- Current vs proposed behavior
- Benefits of the enhancement
- Potential drawbacks
- Alternative solutions considered

### Security Vulnerabilities

**NEVER** open public issues for security vulnerabilities. See [SECURITY.md](SECURITY.md) for reporting process.

### Your First Code Contribution

Unsure where to start? Look for issues tagged:
- `good-first-issue` - Simple issues for beginners
- `help-wanted` - Issues where we need assistance
- `documentation` - Documentation improvements

---

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- pip or pipenv
- (Optional) virtualenv or conda

### Setup Steps

1. **Fork the repository**

   Click "Fork" button on GitHub

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/ACS_Sec.git
   cd ACS_Sec
   ```

3. **Add upstream remote**

   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/ACS_Sec.git
   ```

4. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If it exists
   ```

6. **Create a branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

### Running the Project

```bash
# Start the server
python app.py

# Run vehicle client (in another terminal)
python vehicle_client.py

# Run tests (if available)
pytest
```

---

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) conventions:

```python
# Good
def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS coordinates.
    
    Args:
        lat1 (float): Latitude of first point
        lon1 (float): Longitude of first point
        lat2 (float): Latitude of second point
        lon2 (float): Longitude of second point
        
    Returns:
        float: Distance in meters
    """
    # Implementation
    pass

# Bad
def calc(a,b,c,d):
    # no docstring, unclear names
    pass
```

### Code Formatting

Use automated formatters:

```bash
# Install tools
pip install black flake8 isort

# Format code
black .
isort .

# Check for issues
flake8 .
```

### Naming Conventions

- **Variables/Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`

```python
# Constants
MAX_VEHICLES = 100
DEFAULT_GPS_TIMEOUT = 1

# Classes
class VehicleManager:
    pass

# Functions
def send_encrypted_command(vehicle_id, command):
    pass

# Private
def _validate_gps_data(data):
    pass
```

### Documentation

- Add docstrings to all functions, classes, and modules
- Use clear, descriptive variable names
- Comment complex logic
- Update README when adding features

Example:

```python
def encrypt_command(acs_id, path, action):
    """Encrypt a command for secure transmission to vehicle.
    
    This function creates a pipe-delimited payload containing
    the vehicle ID, navigation path, and action command, then
    encrypts it using AES-256 in CBC mode.
    
    Args:
        acs_id (str): Vehicle identifier (e.g., "ACS01")
        path (str): Navigation path name
        action (str): Command action ("start" or "stop")
        
    Returns:
        str: Base64-encoded encrypted command
        
    Example:
        >>> cmd = encrypt_command("ACS01", "Path-A", "start")
        >>> print(cmd)
        'ZW5jcnlwdGVkX2RhdGFfaGVyZQ=='
    """
    # Implementation
```

---

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no logic change)
- `refactor`: Code restructuring (no behavior change)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
# Good
feat(crypto): add RSA key exchange for AES keys

Implement RSA public key infrastructure to securely exchange
AES session keys instead of using hardcoded keys.

Closes #123

# Good
fix(gps): handle GPS timeout gracefully

Add fallback to last known position when GPS read times out
instead of crashing the vehicle client.

# Bad
fixed stuff
```

### Commit Rules

- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- Keep subject line under 50 characters
- Wrap body at 72 characters
- Separate subject from body with blank line
- Reference issues in footer

---

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated (if applicable)
- [ ] All tests pass locally
- [ ] No merge conflicts with main branch

### Submission Steps

1. **Update your branch**

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open Pull Request**

   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
Describe how you tested your changes

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally

## Screenshots (if applicable)
Add screenshots for UI changes

## Related Issues
Closes #<issue_number>
```

### Review Process

1. **Automated checks** must pass (if configured)
2. **Code review** by maintainer(s)
3. **Feedback addressed** and changes pushed
4. **Approval** from at least one maintainer
5. **Merge** by maintainer

### After Merge

- Delete your branch (optional)
- Update your fork
- Celebrate! 🎉

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_crypto.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### Writing Tests

Create test files in `tests/` directory:

```python
# tests/test_crypto.py
import pytest
from crypto import encrypt_command, decrypt_execute

def test_encrypt_decrypt_roundtrip():
    """Test that encryption and decryption work correctly."""
    acs_id = "ACS01"
    path = "Path-A"
    action = "start"
    
    # Encrypt
    encrypted = encrypt_command(acs_id, path, action)
    
    # Decrypt
    result = decrypt_execute(encrypted)
    
    # Verify
    assert result['status'] == 'success'
    assert result['acs_id'] == acs_id
    assert result['path'] == path
    assert result['action'] == action

def test_decrypt_invalid_data():
    """Test that invalid data is handled gracefully."""
    result = decrypt_execute("invalid_base64_data")
    assert result['status'] == 'error'
```

### Test Coverage

Aim for:
- **70%+** overall coverage
- **90%+** for critical security functions (crypto, auth)
- **100%** for new features

---

## Documentation

### What to Document

- **README.md**: Overview, quick start, features
- **CONFIGURATION.md**: Setup and configuration
- **API.md**: API endpoints and examples
- **Code comments**: Complex logic and algorithms
- **Docstrings**: All functions, classes, modules

### Documentation Style

- Use clear, concise language
- Provide examples
- Include diagrams where helpful
- Keep up-to-date with code changes

### Updating Documentation

When making changes, update:
- Inline code comments
- Function docstrings
- Relevant markdown files (README, CONFIGURATION, etc.)
- API documentation (if endpoints changed)

---

## Areas Needing Contribution

### High Priority

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] WebSocket support for real-time updates
- [ ] Multi-user authentication system
- [ ] Geofencing and alerts

### Medium Priority

- [ ] Historical path playback
- [ ] Telemetry data logging
- [ ] Vehicle health monitoring
- [ ] Route optimization algorithms
- [ ] Performance benchmarks
- [ ] Docker containerization

### Documentation

- [ ] API documentation with examples
- [ ] Video tutorials
- [ ] Architecture diagrams
- [ ] Deployment guides
- [ ] Troubleshooting wiki

---

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Significant contributors may be invited as project maintainers.

---

## Questions?

- **General questions**: Open a GitHub discussion
- **Bug reports**: Open an issue
- **Security**: See [SECURITY.md](SECURITY.md)

---

**Thank you for contributing! Your work helps make autonomous systems more accessible to everyone.** 🚀
