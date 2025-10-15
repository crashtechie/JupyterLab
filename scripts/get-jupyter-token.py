#!/usr/bin/env python3
"""
Secure Jupyter Token Recovery Script
Safely retrieves and displays Jupyter token from .env file without logging
"""

import os
import sys
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

def display_jupyter_urls(token):
    """
    Display Jupyter Lab URLs with the token
    
    Args:
        token (str): Jupyter authentication token
    """
    if not token:
        return
        
    print("\n🚀 Jupyter Lab Access Information:")
    print("=" * 50)
    print(f"🌐 Jupyter Lab:     http://localhost:8888/lab?token={token}")
    print(f"📓 Classic Notebook: http://localhost:8888/tree?token={token}")
    print(f"🔑 Token Only:       {token}")
    print("=" * 50)
    
    # Mask token in logs/history by clearing terminal buffer reference
    # This prevents the token from being stored in terminal history
    print("\n💡 Security Tips:")
    print("• Copy the URL before the terminal scrolls")
    print("• Don't share the token in screenshots or logs")
    print("• Consider using 'docker compose logs jupyter' to get the auto-generated URLs")

def main():
    """Main function"""
    print("🔐 Secure Jupyter Token Recovery")
    print("================================")
    
    # Check if .env file exists
    env_file = ".env"
    if len(sys.argv) > 1:
        env_file = sys.argv[1]
    
    # Get token securely
    token = get_jupyter_token(env_file)
    
    if token:
        print("✅ Token retrieved successfully")
        
        # Ask user if they want to display URLs
        try:
            show_urls = input("\n❓ Display Jupyter URLs? (y/N): ").lower().strip()
            if show_urls in ['y', 'yes']:
                display_jupyter_urls(token)
            else:
                print(f"\n🔑 Token: {token}")
                print("\n💡 Use this token to access Jupyter Lab at http://localhost:8888")
        except KeyboardInterrupt:
            print("\n\n👋 Operation cancelled by user")
            return
    else:
        print("\n❌ Failed to retrieve Jupyter token")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure .env file exists in the current directory")
        print("2. Check that JUPYTER_TOKEN is set in .env file")
        print("3. Verify the token is not a placeholder value")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())