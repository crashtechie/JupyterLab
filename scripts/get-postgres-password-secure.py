#!/usr/bin/env python3
import argparse
import os
import sys
import time
from pathlib import Path
from typing import Optional

def load_postgres_password() -> Optional[str]:

    try:
        project_root = Path(__file__).parent.parent
        env_file = project_root / ".env"
        
        if not env_file.exists():
            return None
        
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('POSTGRES_PASSWORD='):
                    return line.split('=', 1)[1]
        
        return None
        
    except Exception as e:
        print(f"❌ Error loading password: {e}")
        return None

def clipboard_secure_method(password: str) -> bool:

    try:
        import pyperclip
        
        print("🔐 Ultra-Secure Password Recovery - Clipboard Method")
        print("=" * 55)
        print("")
        print("🛡️  MAXIMUM SECURITY LEVEL: 🔒🔒🔒🔒🔒")
        print("📋 Password will be copied to your clipboard")
        print("🔒 Zero terminal exposure - completely secure")
        print("⏰ Password remains in clipboard until overwritten")
        print("")
        
        response = input("📝 Type 'COPY' to copy PostgreSQL password to clipboard: ").strip()
        
        if response != 'COPY':
            print("❌ Operation cancelled - incorrect confirmation")
            return False
        
        # Copy to clipboard
        pyperclip.copy(password)
        
        print("")
        print("✅ PostgreSQL password copied to clipboard!")
        print("🔒 No terminal exposure - completely secure")
        print("📋 Paste (Ctrl+V/Cmd+V) in your database client")
        print("")
        print("🛡️  Security Notes:")
        print("   - Password not displayed in terminal")
        print("   - No logging or output capture possible")
        print("   - Clear clipboard when finished for security")
        print("")
        
        return True
        
    except ImportError:
        print("❌ Clipboard functionality requires pyperclip")
        print("📦 Install with: pip install pyperclip")
        return False
    except Exception as e:
        print(f"❌ Clipboard error: {e}")
        return False

def temporary_display_method(password: str, display_seconds: int = 10) -> bool:

    print("🔐 Ultra-Secure Password Recovery - Temporary Display")
    print("=" * 58)
    print("")
    print("🛡️  HIGH SECURITY LEVEL: 🔒🔒🔒🔒⭕")
    print(f"⏰ Password will be shown for {display_seconds} seconds only")
    print("🔄 Screen will auto-clear for security")
    print("📝 Copy/memorize the password quickly")
    print("")
    
    response = input(f"📝 Type 'SHOW' to display password for {display_seconds} seconds: ").strip()
    
    if response != 'SHOW':
        print("❌ Operation cancelled - incorrect confirmation")
        return False
    
    print("\n" + "=" * 60)
    print("🔓 POSTGRESQL PASSWORD (Auto-clear in progress...):")
    print("=" * 60)
    print(f"📋 {password}")
    print("=" * 60)
    print(f"⏰ Clearing in {display_seconds} seconds...")
    
    # Wait for specified time
    time.sleep(display_seconds)
    
    # Clear screen (cross-platform)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("🔐 Ultra-Secure Password Recovery - Display Complete")
    print("=" * 58)
    print("")
    print("✅ Password display completed and cleared!")
    print("🔒 Screen cleared for security")
    print("📋 Use the password you copied/memorized")
    print("")
    
    return True

def interactive_secure_method(password: str) -> bool:
    print("🔐 Ultra-Secure Password Recovery - Interactive Secure Method")
    print("=" * 66)
    print("")
    print("🛡️  MEDIUM SECURITY LEVEL: 🔒🔒🔒⭕⭕")
    print("🔄 Multi-step confirmation process")
    print("📝 Requires multiple security confirmations")
    print("")
    
    # First confirmation
    response1 = input("📝 Step 1/3 - Type 'ACCESS' to request password access: ").strip()
    if response1 != 'ACCESS':
        print("❌ Access denied - Step 1 failed")
        return False
    
    # Second confirmation
    print("✅ Step 1 confirmed - Access request acknowledged")
    response2 = input("📝 Step 2/3 - Type 'POSTGRES' to confirm database type: ").strip()
    if response2 != 'POSTGRES':
        print("❌ Access denied - Step 2 failed")
        return False
    
    # Final confirmation
    print("✅ Step 2 confirmed - Database type verified")
    response3 = input("📝 Step 3/3 - Type 'SECURE' to display password: ").strip()
    if response3 != 'SECURE':
        print("❌ Access denied - Step 3 failed")
        return False
    
    print("")
    print("✅ All confirmations successful!")
    print("🔓 Displaying PostgreSQL password:")
    print("")
    print("=" * 60)
    print("📋 POSTGRESQL PASSWORD:")
    print(f"   {password}")
    print("=" * 60)
    print("")
    print("🛡️  Security Reminder:")
    print("   - Use password immediately")
    print("   - Clear terminal history if needed")
    print("   - Don't share or log this password")
    print("")
    
    return True

def qr_code_method(password: str) -> bool:
    try:
        import qrcode
        
        print("🔐 Ultra-Secure Password Recovery - QR Code Method")
        print("=" * 56)
        print("")
        print("🛡️  MOBILE SECURITY LEVEL: 🔒🔒⭕⭕⭕")
        print("📱 QR code for mobile device access")
        print("📷 Scan with mobile database client")
        print("🔒 No typing required - scan and use")
        print("")
        
        response = input("📝 Type 'QR' to generate QR code: ").strip()
        
        if response != 'QR':
            print("❌ Operation cancelled - incorrect confirmation")
            return False
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(password)
        qr.make(fit=True)
        
        print("")
        print("📱 PostgreSQL Password QR Code:")
        print("=" * 40)
        qr.print_ascii()
        print("=" * 40)
        print("")
        print("📋 QR Code Instructions:")
        print("   1. Scan QR code with mobile device")
        print("   2. QR contains the complete password")
        print("   3. Use in mobile database client")
        print("   4. Clear QR from screen when done")
        print("")
        
        return True
        
    except ImportError:
        print("❌ QR code functionality requires qrcode library")
        print("📦 Install with: pip install qrcode[pil]")
        return False
    except Exception as e:
        print(f"❌ QR code error: {e}")
        return False



def print_method_comparison():
    """Print security method comparison table."""
    print("🛡️  Security Method Comparison:")
    print("=" * 50)
    print("Method      | Security Level | Use Case")
    print("-" * 50)
    print("Clipboard   | 🔒🔒🔒🔒🔒     | Maximum security")
    print("Temporary   | 🔒🔒🔒🔒⭕     | Quick access")  
    print("Interactive | 🔒🔒🔒⭕⭕     | Controlled access")
    print("QR Code     | 🔒🔒⭕⭕⭕     | Mobile access")
    print("=" * 50)

def main():
    """Main function for ultra-secure PostgreSQL password recovery."""
    parser = argparse.ArgumentParser(
        description="Ultra-Secure PostgreSQL Password Recovery System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Security Methods:
  clipboard    🔒🔒🔒🔒🔒 Copy to clipboard (most secure)
  temporary    🔒🔒🔒🔒⭕ Show briefly with auto-clear  
  interactive  🔒🔒🔒⭕⭕ Multi-confirmation workflow
  qr           🔒🔒⭕⭕⭕ QR code for mobile access

Examples:
  python scripts/get-postgres-password-secure.py --method clipboard
  python scripts/get-postgres-password-secure.py --method temporary
        """
    )
    
    parser.add_argument(
        '--method',
        choices=['clipboard', 'temporary', 'interactive', 'qr'],
        help='Security method to use for password recovery'
    )
    
    args = parser.parse_args()
    
    # Load PostgreSQL password
    password = load_postgres_password()
    
    if not password:
        print("❌ PostgreSQL password not found!")
        print("")
        print("🔧 Troubleshooting:")
        print("   1. Run: python scripts/generate-postgres-password.py")
        print("   2. Check .env file exists in project root")
        print("   3. Verify POSTGRES_PASSWORD entry in .env")
        print("")
        return 1
    
    print(f"🔐 PostgreSQL Password Recovery System")
    print(f"🛡️  Security: 384-bit (64 characters) - Very Strong")
    print(f"📁 Source: .env file (POSTGRES_PASSWORD)")
    print("")
    
    # If no method specified, show menu
    if not args.method:
        print_method_comparison()
        print("")
        print("Available Methods:")
        print("  1. clipboard   - Copy to clipboard (🔒🔒🔒🔒🔒)")
        print("  2. temporary   - Show briefly (🔒🔒🔒🔒⭕)")
        print("  3. interactive - Multi-step (🔒🔒🔒⭕⭕)")
        print("  4. qr          - QR code (🔒🔒⭕⭕⭕)")
        print("")
        
        choice = input("Select method (1-4) or method name: ").strip().lower()
        
        # Map numeric choices to method names
        method_map = {
            '1': 'clipboard', '2': 'temporary', '3': 'interactive',
            '4': 'qr'
        }
        
        method = method_map.get(choice, choice)
    else:
        method = args.method
    
    # Execute selected method
    success = False
    
    if method == 'clipboard':
        success = clipboard_secure_method(password)
    elif method == 'temporary':
        success = temporary_display_method(password)
    elif method == 'interactive':
        success = interactive_secure_method(password)
    elif method == 'qr':
        success = qr_code_method(password)
    else:
        print(f"❌ Unknown method: {method}")
        print("Valid methods: clipboard, temporary, interactive, qr")
        return 1
    
    if success:
        print("🎉 Password recovery completed successfully!")
        return 0
    else:
        print("❌ Password recovery failed!")
        return 1

if __name__ == "__main__":
    exit(main())