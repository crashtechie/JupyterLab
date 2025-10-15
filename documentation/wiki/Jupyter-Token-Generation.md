# Jupyter Token Generation Guide

This guide explains how to generate secure authentication tokens for Jupyter Lab access.

## 🎯 Overview

Jupyter tokens are used for authentication when accessing Jupyter Lab through a web browser. These tokens should be:
- **Cryptographically secure** (64+ characters for 384-bit security)
- **Randomly generated** using cryptographic functions
- **Unique per environment**
- **Not easily guessable**

## 🔐 Generation Methods

### 1. Python Script (Recommended)
```bash
python scripts/generate-jupyter-token.py
```

**Features:**
- Uses **384-bit** secure random generation (`secrets.token_urlsafe(48)`)
- Validates token strength (64-character tokens)
- Updates .env file automatically
- Cross-platform compatibility

### 2. Manual Generation

#### Using Python
```python
import secrets
import string

# Generate a 384-bit secure token (48 bytes = 64 base64 characters)
token = secrets.token_urlsafe(48)  # 384-bit security
print(f"JUPYTER_TOKEN={token}")

# Alternative: 48-character alphanumeric (less entropy)
token_alt = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(48))
print(f"JUPYTER_TOKEN={token_alt}")
```

#### Using OpenSSL
```bash
# Generate 48-byte token (96 hex characters) - 384-bit security
openssl rand -hex 48

# Generate 48-byte base64 token (64 base64 characters)
openssl rand -base64 48
```

#### Using PowerShell
```powershell
# Generate secure random token (64 characters for 384-bit equivalent)
-join ((1..64) | ForEach {[char]((65..90) + (97..122) + (48..57) | Get-Random)})
```

### 3. Online Generators (Use with Caution)
⚠️ **Warning:** Only use trusted, secure online generators for non-production environments.

## 📝 Setting Up Tokens

### 1. Update .env File
```bash
# Add or update the token in your .env file
echo "JUPYTER_TOKEN=your-generated-token-here" >> .env
```

### 2. Verify Token Format
```bash
# Check token length (should be 64+ characters for 384-bit security)
grep "^JUPYTER_TOKEN=" .env | cut -d'=' -f2 | wc -c

# Validate token complexity
grep "^JUPYTER_TOKEN=" .env | cut -d'=' -f2 | grep -E '^[A-Za-z0-9]{32,}$'
```

### 3. Restart Services
```bash
# Apply new token
docker compose restart jupyter
```

## 🛡️ Security Best Practices

### Token Requirements
- ✅ **Recommended: 64+ characters** (384-bit security)
- ✅ **Minimum: 32+ characters** (256-bit security)
- ✅ **Mix of letters, numbers, and URL-safe characters**
- ✅ **Avoid dictionary words**
- ✅ **No personal information**
- ✅ **Unique per environment**

### Storage Security
- 🔐 **Never commit tokens to version control**
- 🔐 **Use .env files (added to .gitignore)**
- 🔐 **Restrict file permissions** (`chmod 600 .env`)
- 🔐 **Rotate tokens regularly**
- 🔐 **Don't share tokens via insecure channels**

### Common Anti-Patterns to Avoid
❌ **Don't use:**
- Simple passwords (`password123`)
- Sequential patterns (`abcd1234`)
- Personal information (`johnsmith2023`)
- Default values (`jupyter-token`)
- Short tokens (< 32 characters)

## 🔄 Token Rotation

### Automated Rotation Script
```bash
#!/bin/bash
# rotate-jupyter-token.sh

echo "🔄 Rotating Jupyter token..."

# Generate new token
NEW_TOKEN=$(python -c "import secrets; print(secrets.token_urlsafe(48))")  # 384-bit security

# Backup current .env
cp .env .env.backup

# Update .env file
sed -i "s/^JUPYTER_TOKEN=.*/JUPYTER_TOKEN=$NEW_TOKEN/" .env

# Restart services
docker compose restart jupyter

echo "✅ Token rotated successfully"
echo "🔗 New access URL: http://localhost:8888/lab?token=$NEW_TOKEN"
```

### Manual Rotation Steps
1. Generate new token
2. Update `.env` file
3. Restart Jupyter services
4. Update any automation scripts
5. Invalidate old bookmarks

## 🚀 Integration Examples

### Docker Compose Integration
```yaml
# docker-compose.yml
services:
  jupyter:
    image: jupyter/datascience-notebook
    environment:
      - JUPYTER_TOKEN=${JUPYTER_TOKEN}
    ports:
      - "8888:8888"
```

### CI/CD Pipeline Integration
```yaml
# .github/workflows/deploy.yml
- name: Generate Jupyter Token
  run: |
    TOKEN=$(python -c "import secrets; print(secrets.token_urlsafe(48))")  # 384-bit security
    echo "JUPYTER_TOKEN=$TOKEN" >> .env
```

### Kubernetes Secret Integration
```yaml
# jupyter-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: jupyter-token
data:
  token: <base64-encoded-token>
```

## 🔧 Troubleshooting

### Common Issues

#### Weak Token Warning
```
⚠️ Warning: Generated token may be weak
```
**Solution:** Regenerate with higher entropy:
```python
import secrets
token = secrets.token_urlsafe(48)  # 384 bits of entropy (recommended)
```

#### Token Not Recognized
```
❌ Error: Invalid token format
```
**Solution:** Ensure token contains only alphanumeric characters:
```bash
# Remove special characters
TOKEN=$(echo "$TOKEN" | tr -cd '[:alnum:]')
```

#### Permission Issues
```
❌ Error: Cannot write to .env file
```
**Solution:** Check file permissions:
```bash
chmod 644 .env
chown $USER .env
```

## 📊 Token Strength Validation

### Entropy Check
```python
import math
from collections import Counter

def calculate_entropy(token):
    """Calculate Shannon entropy of token"""
    counter = Counter(token)
    length = len(token)
    entropy = -sum((count/length) * math.log2(count/length) 
                   for count in counter.values())
    return entropy

# Example usage
token = "your-generated-token"
entropy = calculate_entropy(token)
print(f"Token entropy: {entropy:.2f} bits per character")
print(f"Total entropy: {entropy * len(token):.2f} bits")
```

### Strength Classification
- **Weak:** < 128 bits total entropy
- **Moderate:** 128-255 bits total entropy  
- **Strong:** 256-383 bits total entropy
- **Very Strong:** 384+ bits total entropy ⭐ **Current Implementation**

## 🔗 Related Documentation

- [Jupyter Token Recovery Guide](./Jupyter-Token-Recovery.md)
- [Security Best Practices](../development/Security-Best-Practices.md)
- [Environment Configuration](../development/Environment-Configuration.md)