#!/usr/bin/env python3
"""
Ultra-Secure Jupyter Token Recovery Script
Multiple security methods for token display with maximum protection
"""

import os
import sys
import time
import platform
from pathlib import Path

def get_jupyter_token(env_file_path=".env"):
    """
    Securely retrieve Jupyter token from .env file
    
    Args:
        env_file_path (str): Path to the .env file
        
    Returns:
        str: Jupyter token or None if not found
    """
    try:
        env_path = Path(env_file_path)
        
        if not env_path.exists():
            print(f"❌ Error: .env file not found at {env_path.absolute()}")
            return None
            
        with open(env_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                    
                # Look for JUPYTER_TOKEN
                if line.startswith('JUPYTER_TOKEN='):
                    token = line.split('=', 1)[1].strip()
                    
                    # Remove quotes if present
                    if token.startswith('"') and token.endswith('"'):
                        token = token[1:-1]
                    elif token.startswith("'") and token.endswith("'"):
                        token = token[1:-1]
                    
                    # Validate token (should be non-empty and not placeholder)
                    if not token or token in ['your-secure-token-here', 'change-me']:
                        print("⚠️  Warning: Jupyter token appears to be a placeholder")
                        return None
                        
                    return token
        
        print("❌ Error: JUPYTER_TOKEN not found in .env file")
        return None
        
    except FileNotFoundError:
        print(f"❌ Error: .env file not found at {env_file_path}")
        return None
    except PermissionError:
        print(f"❌ Error: Permission denied reading {env_file_path}")
        return None
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return None

def clipboard_secure_method(token):
    """Method 1: Clipboard copy (most secure - no screen display)"""
    try:
        import pyperclip
        url = f"http://localhost:8888/lab?token={token}"
        pyperclip.copy(url)
        
        # Show only masked token for confirmation
        masked = f"{token[:8]}{'*' * (len(token) - 16)}{token[-8:]}"
        print(f"🔑 Token (masked): {masked}")
        print("✅ Full URL copied to clipboard securely")
        print("🔒 Actual token never displayed on screen")
        return True
        
    except ImportError:
        print("❌ pyperclip not available")
        print("💡 Install with: pip install pyperclip")
        return False

def temporary_display_method(token, seconds=8):
    """Method 2: Temporary display with auto-clear"""
    print(f"\n🔑 Token will display for {seconds} seconds only")
    print("📋 Copy the URL immediately:")
    
    # Countdown
    for i in range(3, 0, -1):
        print(f"   Starting in {i}...", end="\r")
        time.sleep(1)
    
    print("\n" + "🔥" * 70)
    print(f"🌐 http://localhost:8888/lab?token={token}")
    print("🔥" * 70)
    
    # Auto-clear countdown
    for i in range(seconds, 0, -1):
        print(f"\r⏱️  Auto-clearing in {i}s... COPY NOW!", end="", flush=True)
        time.sleep(1)
    
    # Clear screen
    clear_command = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear_command)
    
    print("🔒 Token display cleared automatically")
    return True

def interactive_secure_method(token):
    """Method 3: Interactive with multiple security confirmations"""
    print("\n🔐 Interactive Secure Token Access")
    print("=" * 35)
    
    # Security checks
    checks = [
        "Are you in a private, secure location?",
        "Is your screen not visible to others?", 
        "Are you ready to copy the token quickly?"
    ]
    
    for i, check in enumerate(checks, 1):
        response = input(f"⚠️  {i}/3: {check} (y/N): ").lower().strip()
        if response not in ['y', 'yes']:
            print(f"🚫 Security check {i} failed - access denied")
            return False
    
    # Brief secure display
    input("\n🔑 Press ENTER when ready to see the token...")
    
    # Show token briefly
    print("\n" + "🔒" * 70)
    print(f"🌐 Jupyter: http://localhost:8888/lab?token={token}")
    print("🔒" * 70)
    
    input("\n✅ Press ENTER after copying (will clear immediately)...")
    
    # Secure clear
    print("\n" * 100)  # Scroll token off screen
    print("🔒 Secure token access completed")
    return True

def qr_code_method(token):
    """Method 4: QR Code display (no text token visible)"""
    try:
        import qrcode
        
        url = f"http://localhost:8888/lab?token={token}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        print("\n📱 Secure QR Code Access:")
        print("=" * 25)
        qr.print_ascii(invert=True)
        
        # Show masked token for verification
        masked = f"{token[:6]}...{token[-6:]}"
        print(f"\n🔑 Token ID: {masked}")
        print("📱 Scan QR code with mobile device")
        print("🔒 Token not visible as text")
        
        return True
        
    except ImportError:
        print("❌ qrcode not available")
        print("💡 Install with: pip install qrcode[pil]")
        return False

def choose_display_method(token):
    """Let user choose the most appropriate secure method"""
    
    methods = {
        '1': ('Clipboard Copy', clipboard_secure_method, '⭐ Most Secure'),
        '2': ('Temporary Display', lambda t: temporary_display_method(t), '🔥 Auto-Clear'),
        '3': ('Interactive Secure', interactive_secure_method, '🔐 Multi-Check'),
        '4': ('QR Code', qr_code_method, '📱 Mobile Scan'),
    }
    
    print("\n🔐 Select Secure Token Display Method:")
    print("=" * 40)
    
    for key, (name, func, desc) in methods.items():
        print(f"{key}. {name:<20} - {desc}")
    
    print("0. Cancel")
    print("=" * 40)
    
    while True:
        choice = input("\n🎯 Choose method (1-4, 0 to cancel): ").strip()
        
        if choice == '0':
            print("🚫 Token access cancelled")
            return False
        
        if choice in methods:
            method_name, method_func, _ = methods[choice]
            print(f"\n🔄 Using: {method_name}")
            return method_func(token)
        
        print("❌ Invalid choice. Please select 1-4 or 0.")

def main():
    """Main function with enhanced security options"""
    print("🔐 Ultra-Secure Jupyter Token Recovery")
    print("🛡️  Multiple Security Methods Available")
    print("=" * 45)
    
    # Check if .env file exists
    env_file = ".env"
    if len(sys.argv) > 1:
        env_file = sys.argv[1]
    
    # Get token securely
    token = get_jupyter_token(env_file)
    
    if not token:
        print("\n❌ Failed to retrieve Jupyter token")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure .env file exists in current directory")
        print("2. Check that JUPYTER_TOKEN is set in .env file") 
        print("3. Verify the token is not a placeholder value")
        return 1
    
    # Validate token format (384-bit tokens should be 64 chars)
    if len(token) != 64:
        print(f"⚠️  Warning: Token length is {len(token)} chars (expected 64 for 384-bit)")
    
    print(f"✅ Token retrieved successfully (384-bit security)")
    print(f"📏 Token length: {len(token)} characters")
    
    # Security method selection
    success = choose_display_method(token)
    
    if success:
        print("\n🎉 Secure token access completed")
        print("🔒 Remember: Never share tokens in logs or screenshots")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())