# Environment Configuration Guide

This guide covers environment configuration for the Jupyter Lab Docker development setup.

## 🌍 Environment Overview

The project uses environment variables for configuration to ensure:
- **Security** - Sensitive data stays out of version control
- **Flexibility** - Easy configuration across different environments
- **Portability** - Consistent setup across platforms

## 📝 Environment File Structure

### .env File
Primary configuration file containing sensitive and environment-specific settings:

```bash
# Jupyter Authentication
JUPYTER_TOKEN=your-secure-48-character-token-here

# Service Configuration
JUPYTER_PORT=8888
JUPYTER_HOST=0.0.0.0

# Directory Mappings
JUPYTER_DATA_DIR=./jupyter_data
JUPYTER_CONFIG_DIR=./jupyter_config

# Performance Settings
JUPYTER_MEM_LIMIT=2g
JUPYTER_CPU_LIMIT=1.0

# Security Settings
JUPYTER_ENABLE_MATHJAX=true
JUPYTER_SHUTDOWN_NO_ACTIVITY_TIMEOUT=7200
```

### .env.template File
Template file with placeholder values for new setups:

```bash
# Copy this file to .env and customize for your environment
# JUPYTER_TOKEN=generate-secure-token-here
# JUPYTER_PORT=8888
# JUPYTER_DATA_DIR=./jupyter_data
# JUPYTER_CONFIG_DIR=./jupyter_config
```

## 🔧 Configuration Options

### Authentication Settings
```bash
# Primary authentication token (Required)
JUPYTER_TOKEN=<48-character-secure-token>

# Alternative: Use password instead of token
# JUPYTER_PASSWORD_HASH=<argon2-hashed-password>

# Disable authentication (Development only - NOT RECOMMENDED)
# JUPYTER_DISABLE_AUTH=true
```

### Network Configuration
```bash
# Port mapping (Default: 8888)
JUPYTER_PORT=8888

# Host binding (Default: 0.0.0.0 for container access)
JUPYTER_HOST=0.0.0.0

# Base URL prefix (for reverse proxy setups)
# JUPYTER_BASE_URL=/jupyter

# Allow origin for CORS (Default: *)
# JUPYTER_ALLOW_ORIGIN=https://mydomain.com
```

### Storage Configuration
```bash
# Work directory mapping
JUPYTER_DATA_DIR=./jupyter_data

# Configuration directory
JUPYTER_CONFIG_DIR=./jupyter_config

# Additional volume mounts
# JUPYTER_EXTRA_VOLUMES=./datasets:/home/jovyan/datasets,./models:/home/jovyan/models
```

### Resource Limits
```bash
# Memory limit (Docker format: 512m, 1g, 2g, etc.)
JUPYTER_MEM_LIMIT=2g

# CPU limit (Docker format: 0.5, 1.0, 2.0, etc.)
JUPYTER_CPU_LIMIT=1.0

# Shared memory size (for large datasets)
JUPYTER_SHM_SIZE=1g
```

### Feature Toggles
```bash
# Enable/disable MathJax for LaTeX rendering
JUPYTER_ENABLE_MATHJAX=true

# Enable/disable extensions
JUPYTER_ENABLE_EXTENSIONS=true

# Enable server extensions
JUPYTER_SERVER_EXTENSIONS=nbgitpuller,jupyter_server_proxy

# Shutdown timeout (seconds of inactivity)
JUPYTER_SHUTDOWN_NO_ACTIVITY_TIMEOUT=7200
```

## 🔄 Environment Management

### Environment Setup Script
```bash
#!/bin/bash
# setup-environment.sh

echo "🔧 Setting up Jupyter Lab environment..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "📋 Creating .env from template..."
    cp .env.template .env
fi

# Generate secure token if placeholder exists
if grep -q "generate-secure-token-here" .env; then
    echo "🔐 Generating secure Jupyter token..."
    python scripts/generate-jupyter-token.py
fi

# Create required directories
mkdir -p jupyter_data jupyter_config logs

# Set proper permissions
chmod 600 .env
chmod 700 jupyter_data jupyter_config
chmod 755 logs

echo "✅ Environment setup complete!"
```

### Environment Validation
```bash
#!/bin/bash
# validate-environment.sh

echo "🔍 Validating environment configuration..."

# Check required variables
required_vars=("JUPYTER_TOKEN" "JUPYTER_PORT")
for var in "${required_vars[@]}"; do
    if ! grep -q "^$var=" .env; then
        echo "❌ Missing required variable: $var"
        exit 1
    fi
done

# Validate token strength
token=$(grep "^JUPYTER_TOKEN=" .env | cut -d= -f2)
if [ ${#token} -lt 32 ]; then
    echo "⚠️ Warning: Jupyter token is shorter than 32 characters"
fi

# Check port availability
port=$(grep "^JUPYTER_PORT=" .env | cut -d= -f2)
if netstat -tuln | grep -q ":$port "; then
    echo "⚠️ Warning: Port $port is already in use"
fi

echo "✅ Environment validation complete!"
```

## 🏗️ Multi-Environment Setup

### Development Environment
```bash
# .env.development
JUPYTER_TOKEN=dev-token-48-chars-long-for-development-only
JUPYTER_PORT=8888
JUPYTER_HOST=127.0.0.1
JUPYTER_DATA_DIR=./dev_data
JUPYTER_MEM_LIMIT=1g
JUPYTER_CPU_LIMIT=0.5
JUPYTER_ENABLE_MATHJAX=true
JUPYTER_SHUTDOWN_NO_ACTIVITY_TIMEOUT=3600
```

### Production Environment
```bash
# .env.production
JUPYTER_TOKEN=${JUPYTER_PRODUCTION_TOKEN}
JUPYTER_PORT=8888
JUPYTER_HOST=0.0.0.0
JUPYTER_DATA_DIR=/opt/jupyter/data
JUPYTER_CONFIG_DIR=/opt/jupyter/config
JUPYTER_MEM_LIMIT=4g
JUPYTER_CPU_LIMIT=2.0
JUPYTER_ENABLE_MATHJAX=true
JUPYTER_SHUTDOWN_NO_ACTIVITY_TIMEOUT=7200
```

### Testing Environment
```bash
# .env.testing
JUPYTER_TOKEN=test-token-48-chars-long-for-automated-testing
JUPYTER_PORT=8889
JUPYTER_HOST=127.0.0.1
JUPYTER_DATA_DIR=./test_data
JUPYTER_MEM_LIMIT=512m
JUPYTER_CPU_LIMIT=0.25
JUPYTER_ENABLE_MATHJAX=false
JUPYTER_SHUTDOWN_NO_ACTIVITY_TIMEOUT=600
```

## 🔐 Secrets Management

### Local Development
```bash
# Use local .env file (gitignored)
JUPYTER_TOKEN=local-development-token-here
```

### CI/CD Pipeline
```yaml
# GitHub Actions example
env:
  JUPYTER_TOKEN: ${{ secrets.JUPYTER_TOKEN }}
  JUPYTER_PORT: 8888
```

### Docker Secrets
```yaml
# docker-compose.yml with secrets
services:
  jupyter:
    image: jupyter/datascience-notebook
    secrets:
      - jupyter_token
    environment:
      - JUPYTER_TOKEN_FILE=/run/secrets/jupyter_token

secrets:
  jupyter_token:
    file: ./secrets/jupyter_token.txt
```

### Kubernetes ConfigMap/Secrets
```yaml
# kubernetes configmap
apiVersion: v1
kind: ConfigMap
metadata:
  name: jupyter-config
data:
  JUPYTER_PORT: "8888"
  JUPYTER_HOST: "0.0.0.0"

---
apiVersion: v1
kind: Secret
metadata:
  name: jupyter-secrets
data:
  JUPYTER_TOKEN: <base64-encoded-token>
```

## 🔧 Configuration Utilities

### Environment Checker Script
```python
#!/usr/bin/env python3
# check-environment.py

import os
import sys
from pathlib import Path

def check_environment():
    """Validate environment configuration"""
    
    # Check .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    # Load environment variables
    with open(env_file) as f:
        env_vars = dict(line.strip().split('=', 1) for line in f 
                       if line.strip() and not line.startswith('#'))
    
    # Required variables
    required = ['JUPYTER_TOKEN', 'JUPYTER_PORT']
    missing = [var for var in required if var not in env_vars]
    
    if missing:
        print(f"❌ Missing required variables: {', '.join(missing)}")
        return False
    
    # Validate token
    token = env_vars['JUPYTER_TOKEN']
    if len(token) < 32:
        print("⚠️ Token should be at least 32 characters")
    
    if token in ['your-token-here', 'change-me']:
        print("❌ Please generate a real token")
        return False
    
    print("✅ Environment configuration is valid")
    return True

if __name__ == '__main__':
    sys.exit(0 if check_environment() else 1)
```

### Environment Migration Script
```python
#!/usr/bin/env python3
# migrate-environment.py

import shutil
from pathlib import Path

def migrate_environment(old_version, new_version):
    """Migrate environment configuration between versions"""
    
    old_env = Path(f'.env.{old_version}')
    new_env = Path(f'.env.{new_version}')
    
    if old_env.exists():
        # Copy old configuration
        shutil.copy2(old_env, '.env.backup')
        
        # Apply new defaults
        with open(new_env) as f:
            new_config = f.read()
        
        # Preserve existing values
        if Path('.env').exists():
            with open('.env') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        new_config = new_config.replace(f'{key}=<placeholder>', f'{key}={value}')
        
        # Write updated configuration
        with open('.env', 'w') as f:
            f.write(new_config)
        
        print(f"✅ Environment migrated from {old_version} to {new_version}")
    else:
        print(f"❌ Old environment file not found: {old_env}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python migrate-environment.py <old_version> <new_version>")
        sys.exit(1)
    
    migrate_environment(sys.argv[1], sys.argv[2])
```

## 📊 Configuration Reference

### Default Values
| Variable | Default | Description |
|----------|---------|-------------|
| `JUPYTER_TOKEN` | *required* | Authentication token |
| `JUPYTER_PORT` | `8888` | HTTP port |
| `JUPYTER_HOST` | `0.0.0.0` | Bind address |
| `JUPYTER_DATA_DIR` | `./jupyter_data` | Work directory |
| `JUPYTER_CONFIG_DIR` | `./jupyter_config` | Config directory |
| `JUPYTER_MEM_LIMIT` | `2g` | Memory limit |
| `JUPYTER_CPU_LIMIT` | `1.0` | CPU limit |

### Security Recommendations
| Setting | Development | Production |
|---------|------------|------------|
| Token Length | 32+ chars | 48+ chars |
| Host Binding | `127.0.0.1` | `0.0.0.0` |
| Timeout | 3600s | 7200s |
| Resource Limits | Low | High |

## 🔗 Related Documentation

- [Development Setup Guide](./Development-Setup.md)
- [Security Best Practices](./Security-Best-Practices.md)
- [Jupyter Token Generation Guide](../wiki/Jupyter-Token-Generation.md)
- [Jupyter Token Recovery Guide](../wiki/Jupyter-Token-Recovery.md)