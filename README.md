# Jupyter Lab Data Science Project

A professional Docker Compose setup for Jupyter Lab using the `jupyter/datascience-notebook` image with additional services for comprehensive data science workflows.

## 🚀 Quick Start

### Prerequisites
- **All Platforms**: Docker Desktop (with Docker Compose v2.39.1+)
- **Windows**: PowerShell 5.1+ or WSL2
- **Linux**: Docker Engine + Docker Compose
- **macOS**: Docker Desktop for Mac
- **Optional**: Git (for version control)

### Platform-Specific Setup

#### 🪟 Windows (PowerShell)
```powershell
# Copy environment file
Copy-Item .env.example .env
# Run comprehensive tests
.\scripts\tests\run_tests.ps1
# Start services
docker compose up -d
```

#### 🐧 Linux
```bash
# Copy environment file
cp .env.example .env
# Run comprehensive tests (choose one):
./scripts/tests/run_tests.sh          # Universal Linux/Unix
./scripts/tests/run_tests_linux.sh    # Linux-optimized
# Start services
docker compose up -d
```

#### 🍎 macOS
```bash
# Copy environment file
cp .env.example .env
# Run comprehensive tests (choose one):
./scripts/tests/run_tests.sh          # Universal Unix
./scripts/tests/run_tests_macos.sh    # macOS-optimized
# Start services
docker compose up -d
```

### Default Access
- **URL**: http://localhost:8888
- **Token**: `datascience-token` (change in `.env` file)
- **Lab Interface**: http://localhost:8888/lab
- **Classic Notebook**: http://localhost:8888/tree

## 📁 Project Structure

```
JupyterLab/
├── docker-compose.yml          # Main Docker Compose configuration
├── .env.example               # Environment variables template
├── .env                      # Your environment variables (create from .env.example)
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── requirements.txt         # Additional Python packages
├── notebooks/               # Jupyter notebooks
│   ├── exploratory/        # Data exploration notebooks
│   ├── analysis/           # Analysis notebooks  
│   ├── modeling/           # Machine learning models
│   └── reports/            # Report notebooks
├── data/                   # Dataset storage
│   ├── raw/               # Raw, unprocessed data
│   ├── processed/         # Cleaned and processed data
│   └── external/          # External datasets
├── scripts/               # Python modules and utilities
│   ├── __init__.py       # Make it a Python package
│   ├── utils.py          # Utility functions
│   ├── data_processing.py # Data processing functions
│   └── visualization.py  # Visualization helpers
├── outputs/               # Generated outputs
│   ├── figures/          # Charts and plots
│   ├── models/           # Trained models
│   └── reports/          # Generated reports
└── database/             # Database initialization scripts
    └── init/             # PostgreSQL init scripts
```

## 🛠 Services

### Jupyter Lab (Primary Service)
- **Image**: `jupyter/datascience-notebook:latest`
- **Port**: 8888
- **Features**: 
  - Pre-installed: pandas, numpy, matplotlib, seaborn, scikit-learn, etc.
  - Conda package manager
  - Git integration
  - JupyterLab extensions

### PostgreSQL (Optional)
- **Image**: `postgres:15-alpine`
- **Port**: 5432
- **Usage**: Enable with `docker compose --profile database up -d`

### Redis (Optional) 
- **Image**: `redis:7-alpine`
- **Port**: 6379
- **Usage**: Enable with `docker compose --profile cache up -d`

## 🧪 Testing & Validation

This project includes comprehensive testing scripts to validate your Docker Compose setup across different platforms:

### Test Scripts Overview

| Platform | Script | Features |
|----------|--------|----------|
| **Windows** | `scripts/tests/run_tests.ps1` | PowerShell-optimized, WSL detection, Windows-specific checks |
| **Linux** | `scripts/tests/run_tests_linux.sh` | Distribution detection, package manager integration, systemd support |
| **macOS** | `scripts/tests/run_tests_macos.sh` | Apple Silicon detection, Homebrew integration, Docker Desktop checks |
| **Universal** | `scripts/tests/run_tests.sh` | Cross-platform compatibility for Linux/Unix/macOS |

### What The Tests Check

✅ **System Requirements**
- Docker and Docker Compose installation
- Python environment setup
- Available memory and disk space
- Platform-specific optimizations

✅ **Docker Compose Validation**
- Configuration file syntax
- Service definitions and networking
- Volume mounts and permissions
- Container health and accessibility

✅ **Jupyter Lab Testing**
- Container startup and readiness
- Web interface accessibility (http://localhost:8888)
- Token authentication
- Package availability (pandas, numpy, matplotlib, etc.)

✅ **Integration Tests**
- Python package imports
- Data processing capabilities
- Visualization functionality
- File system operations

### Running Tests

#### Quick Test (Any Platform)
```bash
# Navigate to project directory
cd JupyterLab

# Run platform-appropriate test
# Windows:
.\scripts\tests\run_tests.ps1

# Linux/macOS:
chmod +x scripts/tests/run_tests*.sh
./scripts/tests/run_tests.sh
```

#### Detailed Platform Tests

**Windows (PowerShell)**
```powershell
# Full system analysis with Windows-specific optimizations
.\scripts\tests\run_tests.ps1 -Verbose

# Check WSL integration
wsl --list --verbose
```

**Linux**
```bash
# Distribution-optimized testing
./scripts/tests/run_tests_linux.sh

# Check systemd integration
systemctl --user status docker
```

**macOS**
```bash
# Apple Silicon and Homebrew optimized
./scripts/tests/run_tests_macos.sh

# Check Docker Desktop status
docker context ls
```

### Test Output

Tests generate detailed reports in `scripts/tests/results/`:
- `test_results.json` - Structured test results
- `system_info.json` - System configuration details
- `docker_info.json` - Docker environment details
- Platform-specific logs and diagnostics

## 📋 Common Commands

### Basic Operations
```bash
# Start all services
docker compose up -d

# Start with database
docker compose --profile database up -d

# Start with all optional services  
docker compose --profile database --profile cache up -d

# Stop services
docker compose down

# Restart Jupyter service
docker compose restart jupyter

# View logs
docker compose logs jupyter
docker compose logs -f jupyter  # Follow logs
```

### Package Management
```bash
# Install additional packages
docker compose exec jupyter pip install package-name
# or use conda
docker compose exec jupyter conda install package-name

# Install from requirements.txt
docker compose exec jupyter pip install -r /home/jovyan/work/requirements.txt
```

### Container Management
```bash
# Access container shell
docker compose exec jupyter bash

# Update services
docker compose pull
docker compose up -d

# Rebuild containers
docker compose down && docker compose up -d --build

# Remove everything (including volumes)
docker compose down -v
```

## 🔧 Customization

### Adding Python Packages
1. **Runtime Installation** (temporary):
   ```bash
   docker compose exec jupyter pip install package-name
   ```

2. **Persistent Installation** (recommended):
   - Add packages to `requirements.txt`
   - Rebuild: `docker compose down && docker compose up -d --build`

3. **Conda Packages**:
   ```bash
   docker compose exec jupyter conda install -c conda-forge package-name
   ```

### Custom Jupyter Configuration
Create `jupyter_notebook_config.py` and mount it:
```yaml
# In docker-compose.yml under jupyter volumes:
volumes:
  - ./configs/jupyter_notebook_config.py:/home/jovyan/.jupyter/jupyter_notebook_config.py
```

### Environment Variables
Edit `.env` file to customize:
- `JUPYTER_TOKEN` - Authentication token
- `JUPYTER_PORT` - Port mapping
- `POSTGRES_*` - Database credentials
- `TZ` - Timezone setting

## 🔒 Security Best Practices

- ✅ **Change Default Token**: Update `JUPYTER_TOKEN` in `.env`
- ✅ **Git Ignore**: Never commit `.env` file to version control
- ✅ **Strong Passwords**: Use complex passwords for database services
- ✅ **Network Isolation**: Use custom Docker networks
- ✅ **Production Secrets**: Consider Docker secrets for production deployments
- ✅ **Regular Updates**: Keep base images updated

## 🐛 Troubleshooting

### Common Issues

#### Port Conflicts
**Problem**: Port 8888 already in use
**Solution**: Change port in `.env`:
```env
JUPYTER_PORT=8889
```

#### Permission Issues
**Problem**: Cannot write files or access directories
**Solution**: Fix ownership in container:
```bash
docker compose exec jupyter chown -R jovyan:users /home/jovyan/work
```

#### Container Won't Start
**Problem**: Docker Compose fails to start
**Solution**: Check logs and run diagnostics:
```bash
docker compose logs jupyter
./scripts/tests/run_tests.ps1  # Windows
./scripts/tests/run_tests.sh   # Linux/macOS
```

#### Package Installation Failures
**Problem**: pip/conda install fails
**Solution**: Use appropriate package manager:
```bash
# For scientific packages, prefer conda:
docker compose exec jupyter conda install -c conda-forge scikit-learn

# For pure Python packages, use pip:
docker compose exec jupyter pip install requests
```

### Platform-Specific Issues

#### Windows
- **WSL2 Integration**: Ensure Docker Desktop WSL2 integration is enabled
- **File Permissions**: Use WSL2 file system for better performance
- **PowerShell Execution Policy**: May need to run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

#### Linux
- **Docker Daemon**: Ensure Docker service is running: `sudo systemctl start docker`
- **User Groups**: Add user to docker group: `sudo usermod -aG docker $USER`
- **SELinux**: On RHEL/CentOS, check SELinux contexts if having volume mount issues

#### macOS
- **Docker Desktop**: Ensure Docker Desktop is running and has sufficient resources
- **File Sharing**: Grant Docker access to project directory in Docker Desktop preferences
- **Apple Silicon**: Use compatible images (most modern images support arm64)

### Debug Mode

Enable verbose logging by setting environment variables:
```bash
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
docker compose --verbose up -d
```

### Getting Help

1. **Run Diagnostics**: Use the appropriate test script for your platform
2. **Check Logs**: `docker compose logs jupyter`
3. **System Info**: `docker system info`
4. **Network Issues**: `docker network ls` and `docker compose port jupyter 8888`
5. **Container Status**: `docker compose ps`

## 📚 Useful Resources

- [Jupyter Docker Stacks Documentation](https://jupyter-docker-stacks.readthedocs.io/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Jupyter Lab Documentation](https://jupyterlab.readthedocs.io/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.