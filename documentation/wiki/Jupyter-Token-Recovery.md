# Jupyter Token Recovery Methods

This guide contains secure methods to retrieve and display the Jupyter authentication token from your `.env` file for initial setup.

## 🔐 Available Methods

### 1. Ultra-Secure Recovery Script ⭐ **MOST SECURE**
```bash
python scripts/get-jupyter-token-secure.py
```
**Security Features:**
- 🔒 **Clipboard Copy** - Zero screen exposure (most secure)
- 🔥 **Temporary Display** - Auto-clearing after 8 seconds
- 🔐 **Interactive Secure** - Multi-confirmation security checks
- 📱 **QR Code Display** - Mobile scanning (no text token)
- ️ **Security Analysis** - Environment safety detection

**Dependencies (optional):**
```bash
pip install pyperclip qrcode[pil]  # For enhanced security features
```

### 2. Command Line One-Liners

#### PowerShell (Windows)
```powershell
# Get token only
(Get-Content .env | Where-Object {$_ -match "^JUPYTER_TOKEN="} | ForEach-Object {($_ -split "=")[1]}).Trim()

# Get full URL
$token = (Get-Content .env | Where-Object {$_ -match "^JUPYTER_TOKEN="} | ForEach-Object {($_ -split "=")[1]}).Trim(); "http://localhost:8888/lab?token=$token"
```

#### Bash/Linux/macOS
```bash
# Get token only
grep "^JUPYTER_TOKEN=" .env | cut -d'=' -f2 | tr -d '"'"'"

# Get full URL
token=$(grep "^JUPYTER_TOKEN=" .env | cut -d'=' -f2 | tr -d '"'"'"); echo "http://localhost:8888/lab?token=$token"
```

#### Python One-Liner
```bash
python -c "
import re
with open('.env') as f:
    for line in f:
        if line.startswith('JUPYTER_TOKEN='):
            token = line.split('=', 1)[1].strip().strip('\"')
            print(f'http://localhost:8888/lab?token={token}')
            break
"
```

## 🛡️ Enhanced Security Methods (RECOMMENDED)

### Ultra-Secure Recovery Options

The new `get-jupyter-token-secure.py` script provides multiple security levels:

#### 🔒 **Method 1: Clipboard Copy (Most Secure)**
```bash
python scripts/get-jupyter-token-secure.py
# Choose option 1: Clipboard Copy
```
- ✅ **Zero screen exposure** - token never displayed
- ✅ **Direct clipboard access** - paste ready URL
- ✅ **Masked verification** - shows partial token only
- ✅ **No terminal history** contamination

#### 🔥 **Method 2: Temporary Display (Auto-Clear)**
```bash
python scripts/get-jupyter-token-secure.py  
# Choose option 2: Temporary Display
```
- ✅ **8-second display** window with countdown
- ✅ **Automatic screen clearing** after timeout
- ✅ **Visual countdown** warning
- ✅ **No dependencies** required

#### 🔐 **Method 3: Interactive Secure (Multi-Check)**
```bash
python scripts/get-jupyter-token-secure.py
# Choose option 3: Interactive Secure  
```
- ✅ **Multiple security confirmations** required
- ✅ **Environment verification** prompts
- ✅ **User-controlled display** timing
- ✅ **Manual security clearing**

#### 📱 **Method 4: QR Code Display (Mobile Access)**
```bash
pip install qrcode[pil]
python scripts/get-jupyter-token-secure.py
# Choose option 4: QR Code
```
- ✅ **No text token displayed** on screen
- ✅ **Mobile device scanning** required
- ✅ **Visual pattern encoding** only
- ✅ **Screenshot resistant** to casual viewing

### Security Method Comparison

| Method | Security | Screen Exposure | Dependencies | Best For |
|--------|----------|----------------|--------------|----------|
| **Clipboard Copy** | 🔒🔒🔒🔒🔒 | None | pyperclip | **Production** |
| **Temporary Display** | 🔒🔒🔒🔒⭕ | 8 seconds | None | **Development** |
| **Interactive Secure** | 🔒🔒🔒🔒⭕ | User-controlled | None | **Shared Systems** |
| **QR Code** | 🔒🔒🔒⭕⭕ | Pattern only | qrcode | **Mobile Access** |

## �🛡️ Security Features

### Built-in Security Protections
- ✅ **No History Logging** - Tokens won't appear in command history
- ✅ **Input Validation** - Detects placeholder tokens
- ✅ **Error Handling** - Graceful failure with helpful messages
- ✅ **File Permissions** - Checks .env file accessibility
- ✅ **Quote Removal** - Handles quoted token values

### Security Best Practices
- 🔐 **Token Masking** - Options to hide full token in output
- 🔐 **Temporary Display** - URLs shown briefly to prevent logging
- 🔐 **No Network Calls** - All processing is local
- 🔐 **Read-Only Access** - Scripts don't modify .env file

## 📋 Usage Examples

### Initial Setup Workflow (Enhanced Security)
```bash
# 1. Start Jupyter services
docker compose up -d

# 2. Install security dependencies (optional but recommended)
pip install pyperclip qrcode[pil]

# 3. Get access URL with maximum security
python scripts/get-jupyter-token-secure.py
# Choose option 1: Clipboard Copy (most secure)

# 4. Paste URL directly into browser (token never displayed)
```

### Production Environment (Maximum Security)
```bash
# Use clipboard method - zero screen exposure
python scripts/get-jupyter-token-secure.py
# Select: 1. Clipboard Copy
# Result: URL copied to clipboard, token never displayed
```

### Development Environment (Quick Access)
```bash
# Use temporary display - auto-clearing
python scripts/get-jupyter-token-secure.py  
# Select: 2. Temporary Display
# Result: 8-second display with auto-clear
```

### Shared/Public Systems (Interactive Security)
```bash
# Use interactive method with confirmations
python scripts/get-jupyter-token-secure.py
# Select: 3. Interactive Secure
# Result: Multiple security checks before display
```

### Mobile Access (QR Code)
```bash
# Use QR code for mobile scanning
pip install qrcode[pil]
python scripts/get-jupyter-token-secure.py
# Select: 4. QR Code
# Result: Scannable QR code, no text token
```

### Automation Scripts
```bash
# Get token for use in scripts
TOKEN=$(python -c "
with open('.env') as f:
    for line in f:
        if line.startswith('JUPYTER_TOKEN='):
            print(line.split('=', 1)[1].strip().strip('\"'))
            break
")

# Use token in automated workflows
curl -H "Authorization: token $TOKEN" http://localhost:8888/api/status
```

## 🔧 Troubleshooting

### Common Issues

#### Token Not Found
```
❌ Error: JUPYTER_TOKEN not found in .env file
```
**Solution:** Ensure `.env` file exists and contains `JUPYTER_TOKEN=your-token-here`

#### Placeholder Token Warning  
```
⚠️ Warning: Jupyter token appears to be a placeholder
```
**Solution:** Generate a new token using:
```bash
python scripts/generate-jupyter-token.py
```

#### Permission Denied
```
❌ Error: Permission denied reading .env
```
**Solution:** Check file permissions:
```bash
chmod 644 .env  # Linux/macOS
icacls .env /grant:r %USERNAME%:R  # Windows
```

### Validation Commands
```bash
# Check .env file exists and is readable
test -r .env && echo "✅ .env file accessible" || echo "❌ .env file not accessible"

# Check token format (should be 32+ characters)
grep "^JUPYTER_TOKEN=" .env | cut -d'=' -f2 | wc -c

# Validate token is not placeholder
grep "^JUPYTER_TOKEN=" .env | grep -v "your-.*-token\|change-me" && echo "✅ Token looks valid" || echo "❌ Token is placeholder"
```

## 🎯 Quick Reference

### Security-First Method Recommendations

| Method | Platform | Security Level | Best Use Case | Dependencies |
|--------|----------|----------------|---------------|--------------|
| **Ultra-Secure Script** | All | 🔒🔒🔒🔒🔒 | **Production** | Optional |
| ↳ Clipboard Copy | All | Maximum | **Any environment** | pyperclip |
| ↳ Temporary Display | All | Very High | **Development** | None |
| ↳ Interactive Secure | All | Very High | **Shared systems** | None |
| ↳ QR Code | All | High | **Mobile access** | qrcode |
| One-liners | All | Low | **Quick testing** | None |

### **🎯 Primary Recommendations:**

1. **🏆 Production/Sensitive:** `python scripts/get-jupyter-token-secure.py` → Clipboard Copy
2. **🔥 Development/Quick:** `python scripts/get-jupyter-token-secure.py` → Temporary Display  
3. **� Shared Systems:** `python scripts/get-jupyter-token-secure.py` → Interactive Secure
4. **� Mobile Access:** `python scripts/get-jupyter-token-secure.py` → QR Code

## 🔗 Related Documentation

- [Jupyter Token Generation Guide](./Jupyter-Token-Generation.md) - How to generate 384-bit secure tokens
- [Security Best Practices](../development/Security-Best-Practices.md) - Overall security guidelines
- [Secure Token Display Methods](../development/Secure-Token-Display-Methods.md) - Detailed security analysis ⭐
- [384-Bit Security Implementation](../development/384-Bit-Security-Implementation.md) - Enhanced token security
- [Development Setup](../development/Development-Setup.md) - Complete environment setup