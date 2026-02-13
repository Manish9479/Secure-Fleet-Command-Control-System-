# Contributing Guide

Thanks for your interest! Here's how to contribute effectively.

---

## 🐛 Reporting Issues

**Before opening an issue**, check if it already exists.

**Include:**
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python version)
- Error messages/logs

---

## 💡 Suggesting Features

**Open an issue with:**
- Clear use case
- Benefits of the feature
- Potential drawbacks

---

## 🔐 Security Issues

**Never** open public issues for security vulnerabilities. See [SECURITY.md](SECURITY.md).

---

## 🚀 Getting Started

### Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/Secure-Fleet-Command-Control-System-.git
cd Secure-Fleet-Command-Control-System-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a branch
git checkout -b feature/your-feature
```

### Running Locally

```bash
python app.py  # Start server
python vehicle_client.py  # Run client (separate terminal)
```

---

## 📝 Code Standards

### Style
- Follow **PEP 8**
- Use `black` for formatting: `black .`
- Check with `flake8 .`

### Naming
- Variables/functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

### Documentation
- Add docstrings to all functions/classes
- Comment complex logic
- Update README for new features

---

## 📨 Commit Messages

Format: `<type>: <description>`

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `refactor` - Code restructuring
- `test` - Tests

**Examples:**
```bash
feat: add GPS fallback positioning
fix: handle GPS timeout gracefully
docs: update configuration guide
```

---

## 🔄 Pull Request Process

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push and open PR**
   ```bash
   git push origin feature/your-feature
   ```

3. **Fill PR template** with:
   - Description of changes
   - Type of change (bug fix/feature/docs)
   - How you tested it
   - Related issue numbers

4. **Wait for review** - Maintainers will review and provide feedback

---

## ✅ Before Submitting

- [ ] Code follows style guidelines
- [ ] Self-reviewed your code
- [ ] Added comments for complex logic
- [ ] Updated documentation
- [ ] No merge conflicts

---

## 🎯 Good First Issues

Look for tags:
- `good-first-issue` - Beginner-friendly
- `help-wanted` - Need assistance
- `documentation` - Docs improvements

---

## 🤝 Code of Conduct

Be respectful, welcoming, and constructive. No harassment or personal attacks.

---

## 📬 Questions?

- General: Open a discussion
- Bugs: Open an issue
- Security: See [SECURITY.md](SECURITY.md)

**Thank you for contributing!** 🚀
