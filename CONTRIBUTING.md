# Contributing to JupyterLab Docker Environment

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🚀 Quick Start

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/JupyterLab.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `./scripts/tests/run_tests.ps1` (Windows) or `./scripts/tests/run_tests.sh` (Linux/Mac)
6. Commit using conventional commits (see below)
7. Push to your fork and create a Pull Request

## 📋 Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/) for automated semantic versioning and changelog generation.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types and Version Bumps

| Type | Description | Version Bump | Example |
|------|-------------|--------------|---------|
| `feat` | New feature | **Minor** (0.X.0) | `feat: add Redis caching support` |
| `fix` | Bug fix | **Patch** (0.0.X) | `fix: resolve token authentication issue` |
| `perf` | Performance improvement | **Patch** (0.0.X) | `perf: optimize database queries` |
| `refactor` | Code refactoring | **Patch** (0.0.X) | `refactor: restructure data processing module` |
| `docs` | Documentation only | **No bump** | `docs: update installation instructions` |
| `style` | Code style changes | **No bump** | `style: format code with black` |
| `test` | Adding/updating tests | **No bump** | `test: add unit tests for utils module` |
| `chore` | Maintenance tasks | **No bump** | `chore: update dependencies` |
| `ci` | CI/CD changes | **No bump** | `ci: add GitHub Actions workflow` |
| `build` | Build system changes | **No bump** | `build: update Docker configuration` |
| `revert` | Revert previous commit | **Patch** (0.0.X) | `revert: revert commit abc123` |

### Breaking Changes (Major Version Bump)

To trigger a **Major** version bump (X.0.0), use one of these methods:

**Method 1: Add `!` after type:**
```
feat!: migrate to PostgreSQL 16
fix!: change authentication API
```

**Method 2: Include `BREAKING CHANGE:` in footer:**
```
feat: update authentication system

BREAKING CHANGE: API endpoints have changed from /v1/ to /v2/
Users must update their client applications accordingly.
```

### Scope (Optional)

The scope specifies what part of the codebase is affected:

- `security` - Security-related changes
- `docker` - Docker configuration
- `jupyter` - Jupyter Lab configuration
- `database` - Database changes
- `scripts` - Script modifications
- `tests` - Test infrastructure
- `docs` - Documentation

**Examples:**
```
feat(docker): add multi-stage build support
fix(security): patch authentication vulnerability
docs(testing): update cross-platform testing guide
```

### Examples of Good Commit Messages

#### Feature (Minor Bump)
```
feat(jupyter): add custom kernel configurations

- Add support for custom Jupyter kernels
- Update documentation with kernel setup instructions
- Include example kernel.json files
```

#### Bug Fix (Patch Bump)
```
fix(docker): resolve volume permission issues on Linux

Fixed permission denied errors when mounting volumes on Linux systems
by setting appropriate user permissions in docker-compose.yml.

Closes #42
```

#### Breaking Change (Major Bump)
```
feat!: migrate to Python 3.12

BREAKING CHANGE: Minimum Python version is now 3.12
- Update all dependencies
- Remove Python 3.10 compatibility code
- Update CI/CD pipelines

Migration guide: documentation/wiki/Python-3.12-Migration.md
```

#### Documentation (No Bump)
```
docs: reorganize documentation structure

- Created unified /documentation structure
- Added testing and security sections
- Updated all cross-references
```

## 🔄 Automated Semantic Versioning

### How It Works

1. **Commit Analysis**: When you push to `main` or `develop`, GitHub Actions analyzes commit messages
2. **Version Bump**: Based on commit type, the appropriate version bump is triggered:
   - `BREAKING CHANGE` or `type!` → Major (1.0.0 → 2.0.0)
   - `feat:` → Minor (1.0.0 → 1.1.0)
   - `fix:`, `perf:`, `refactor:` → Patch (1.0.0 → 1.0.1)
   - Other types → No version bump
3. **Updates**: Automatically updates `version.txt`, `README.md` badge, and `CHANGELOG.md`
4. **Release**: Creates a Git tag and GitHub release
   - `main` branch → Full release
   - `develop` branch → Pre-release

### Manual Version Bumping

You can also bump versions manually using the Python script:

```bash
# Show current version
python scripts/version_manager.py --current

# Bump patch version (0.6.0 → 0.6.1)
python scripts/version_manager.py --bump patch

# Bump minor version (0.6.0 → 0.7.0)
python scripts/version_manager.py --bump minor

# Bump major version (0.6.0 → 1.0.0)
python scripts/version_manager.py --bump major

# Set specific version
python scripts/version_manager.py --set 2.0.0

# Dry run (preview changes)
python scripts/version_manager.py --bump minor --dry-run
```

After manual version bump:
```bash
# Review changes
git diff

# Commit
git add .
git commit -m "chore: bump version to v0.7.0"

# Tag
git tag -a v0.7.0 -m "Release v0.7.0"

# Push
git push origin develop
git push origin v0.7.0
```

### Triggering Manual Release via GitHub Actions

You can also trigger a release manually from GitHub:

1. Go to **Actions** tab
2. Select **Semantic Release** workflow
3. Click **Run workflow**
4. Choose branch and version bump type
5. Click **Run workflow**

## 🧪 Testing Requirements

Before submitting a PR, ensure all tests pass:

### Windows
```powershell
.\scripts\tests\run_tests.ps1
```

### Linux
```bash
./scripts/tests/run_tests_linux.sh
```

### macOS
```bash
./scripts/tests/run_tests_macos.sh
```

### Docker Security Tests
```bash
./scripts/tests/run_docker_tests.sh
```

All tests must pass before your PR can be merged.

## 📝 Documentation

- Update relevant documentation in `/documentation` for new features
- Add examples and usage instructions
- Update CHANGELOG.md manually if needed
- Include docstrings for new functions/classes

## 🔒 Security

- Report security vulnerabilities privately (don't create public issues)
- Follow security best practices in [Security Best Practices](documentation/development/Security-Best-Practices.md)
- Run security validation tests
- Avoid committing sensitive information

## 🎯 Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and concise
- Write unit tests for new features

## 📊 Pull Request Process

1. **Create PR** against the `develop` branch
2. **Fill out PR template** with description and checklist
3. **Link related issues** using "Closes #123" or "Fixes #456"
4. **Request review** from maintainers
5. **Address feedback** and update PR
6. **Wait for approval** and automated checks to pass
7. **Merge** will be done by maintainers

## 🏷️ Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `security` - Security-related issues
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed

## ❓ Questions?

- Check [documentation](documentation/README.md)
- Search [existing issues](https://github.com/crashtechie/JupyterLab/issues)
- Create a new issue for questions or discussions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to JupyterLab Docker Environment! 🎉**
