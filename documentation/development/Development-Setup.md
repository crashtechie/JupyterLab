# Development Setup Guide

This guide walks through setting up the Jupyter Lab Docker development environment from scratch.

## 🎯 Prerequisites

### Required Software
- **Docker Desktop** (v20.10+)
- **Docker Compose** (v2.0+)
- **Git** (v2.30+)
- **Python** (v3.9+) - for token management scripts
- **Code Editor** (VS Code, PyCharm, etc.)

### Platform-Specific Requirements

#### Windows
- Windows 10/11 with WSL2 enabled
- PowerShell 5.1+ or PowerShell Core 7+
- Windows Terminal (recommended)

#### macOS
- macOS 10.15+ (Catalina or later)
- Homebrew (recommended for package management)
- Xcode Command Line Tools

#### Linux
- Ubuntu 20.04+, CentOS 8+, or equivalent
- Docker engine installed via package manager
- Make utility installed

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/crashtechie/JupyterLab.git
cd JupyterLab
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.template .env

# Generate secure Jupyter token
python scripts/generate-jupyter-token.py

# Verify environment configuration
cat .env
```

### 3. Start Services
```bash
# Start Jupyter Lab in detached mode
docker compose up -d

# Check service status
docker compose ps

# View logs
docker compose logs -f jupyter
```

### 4. Access Jupyter Lab
```bash
# Get access URL with ultra-secure methods
python scripts/get-jupyter-token-secure.py

# Or manually construct URL
echo "http://localhost:8888/lab?token=$(grep JUPYTER_TOKEN .env | cut -d= -f2)"
```

## 🔧 Detailed Configuration

### Environment Variables
```bash
# .env file structure
JUPYTER_TOKEN=your-secure-48-character-token-here
JUPYTER_PORT=8888
JUPYTER_DATA_DIR=./jupyter_data
JUPYTER_CONFIG_DIR=./jupyter_config
```

### Docker Compose Configuration
```yaml
# docker-compose.yml key sections
services:
  jupyter:
    image: jupyter/datascience-notebook:latest
    environment:
      - JUPYTER_TOKEN=${JUPYTER_TOKEN}
    ports:
      - "${JUPYTER_PORT}:8888"
    volumes:
      - "${JUPYTER_DATA_DIR}:/home/jovyan/work"
```

### Custom Jupyter Configuration
```bash
# Create custom jupyter config
mkdir -p jupyter_config
cat > jupyter_config/jupyter_lab_config.py << EOF
c.ServerApp.token = ''  # Token managed via environment
c.ServerApp.password = ''
c.ServerApp.open_browser = False
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.allow_origin = '*'
c.ServerApp.allow_root = True
EOF
```

## 🛠️ Development Workflow

### Daily Workflow
```bash
# 1. Start development environment
docker compose up -d

# 2. Check services are running
docker compose ps

# 3. Access Jupyter Lab
python scripts/get-jupyter-token-secure.py

# 4. Work on notebooks/code

# 5. Stop services when done
docker compose down
```

### Testing Workflow
```bash
# Run automated tests
python scripts/tests/run_all_tests.py

# Check security vulnerabilities
python scripts/security/check_vulnerabilities.py

# Validate configuration
python scripts/tests/validate_setup.py
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/new-notebook

# Make changes and commit
git add .
git commit -m "Add data analysis notebook"

# Push and create PR
git push origin feature/new-notebook
```

## 📁 Project Structure

```
JupyterLab/
├── .env                          # Environment variables
├── .env.template                 # Environment template
├── .gitignore                    # Git ignore rules
├── docker-compose.yml            # Docker services
├── LICENSE                       # MIT License
├── README.md                     # Project overview
│
├── documentation/                # Project documentation
│   ├── wiki/                     # User guides
│   │   ├── Jupyter-Token-Generation.md
│   │   └── Jupyter-Token-Recovery.md
│   └── development/              # Developer docs
│       ├── Development-Setup.md
│       ├── Security-Best-Practices.md
│       └── Environment-Configuration.md
│
├── scripts/                      # Automation scripts
│   ├── generate-jupyter-token.py # Token generation
│   ├── get-jupyter-token-secure.py # Ultra-secure token recovery
│   │
│   ├── tests/                    # Test scripts
│   │   ├── run_all_tests.py
│   │   ├── test_token_security.py
│   │   └── validate_setup.py
│   │
│   └── security/                 # Security tools
│       ├── check_vulnerabilities.py
│       └── audit_permissions.py
│
├── jupyter_data/                 # Jupyter notebooks (gitignored)
├── jupyter_config/               # Jupyter configuration
└── logs/                        # Application logs (gitignored)
```

## 🧪 Testing Setup

### Unit Tests
```bash
# Install testing dependencies
pip install -r requirements-dev.txt

# Run unit tests
python -m pytest scripts/tests/

# Run with coverage
python -m pytest --cov=scripts scripts/tests/
```

### Integration Tests
```bash
# Test full environment setup
python scripts/tests/test_full_setup.py

# Test Docker services
python scripts/tests/test_docker_services.py

# Test token functionality
python scripts/tests/test_token_operations.py
```

### Security Tests
```bash
# Check for common vulnerabilities
python scripts/security/vulnerability_scan.py

# Audit file permissions
python scripts/security/audit_permissions.py

# Test token security
python scripts/tests/test_token_security.py
```

## 🔍 Troubleshooting

### Common Issues

#### Docker Permission Denied
```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify access
docker ps
```

#### Port Already in Use
```bash
# Find process using port 8888
netstat -tulpn | grep 8888  # Linux
netstat -ano | findstr 8888  # Windows

# Kill process or change port in .env
JUPYTER_PORT=8889
```

#### Token Authentication Failed
```bash
# Regenerate token
python scripts/generate-jupyter-token.py

# Restart services
docker compose restart jupyter

# Verify token format
grep JUPYTER_TOKEN .env
```

### Debug Mode
```bash
# Enable debug logging
export JUPYTER_LOG_LEVEL=DEBUG

# Start with verbose output
docker compose up --verbose

# Check detailed logs
docker compose logs --details jupyter
```

### Clean Reset
```bash
# Stop all services
docker compose down

# Remove containers and volumes
docker compose down -v --remove-orphans

# Clean up images
docker system prune -a

# Regenerate environment
cp .env.template .env
python scripts/generate-jupyter-token.py
```

## 📚 Additional Resources

### Documentation Links
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/)
- [Jupyter Lab Documentation](https://jupyterlab.readthedocs.io/)

### Security Resources
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Jupyter Security Guide](https://jupyter-server.readthedocs.io/en/latest/operators/security.html)

### Development Tools
- [VS Code Docker Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)
- [Jupyter VS Code Extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)

## 🔗 Related Documentation

- [Jupyter Token Generation Guide](../wiki/Jupyter-Token-Generation.md)
- [Jupyter Token Recovery Guide](../wiki/Jupyter-Token-Recovery.md)
- [Security Best Practices](./Security-Best-Practices.md)
- [Environment Configuration](./Environment-Configuration.md)