#!/usr/bin/env python3
import secrets
import os
from pathlib import Path

def generate_secure_password():
    # Generate 384-bit (48-byte) cryptographically secure password
    # Results in 64 characters with ~384 bits of entropy
    return secrets.token_urlsafe(48)

def save_password_to_env(password):
    try:
        project_root = Path(__file__).parent.parent
        env_file = project_root / ".env"
        
        # Read existing .env file if it exists
        env_lines = []
        postgres_password_updated = False
        
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                env_lines = f.readlines()
        
        # Update or add POSTGRES_PASSWORD entry
        updated_lines = []
        for line in env_lines:
            if line.strip().startswith('POSTGRES_PASSWORD='):
                updated_lines.append(f'POSTGRES_PASSWORD={password}\n')
                postgres_password_updated = True
            else:
                updated_lines.append(line)
        
        # Add POSTGRES_PASSWORD if it wasn't found
        if not postgres_password_updated:
            updated_lines.append(f'POSTGRES_PASSWORD={password}\n')
        
        # Write updated .env file
        with open(env_file, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        
        # Set appropriate file permissions (readable by owner only)
        if hasattr(os, 'chmod'):
            os.chmod(env_file, 0o600)
        
        return True
        
    except Exception as e:
        print(f"Error saving password to .env file: {e}")
        return False

def main():
    print("🔐 Generating PostgreSQL Password...")
    print("   Security Level: 384-bit (Very Strong)")
    print("   Length: 64 characters")
    print("")
    
    # Generate secure password
    password = generate_secure_password()
    
    # Save to .env file securely
    if save_password_to_env(password):
        print("✅ PostgreSQL password generated successfully!")
        print("📁 Saved to .env file as POSTGRES_PASSWORD")
        print("🔒 Password stored securely (not displayed)")
        print("")
        print("📋 Next Steps:")
        print("   1. Restart Docker services to use new password")
        print("   2. Use secure recovery scripts if password access needed")
        print("   3. Update any external database connections")
        print("")
        print("🛡️  Security Notice:")
        print("   - Password has 384-bit cryptographic strength")
        print("   - No sensitive information logged or displayed") 
        print("   - Use 'python scripts/get-postgres-password-secure.py' for secure recovery")
    else:
        print("❌ Failed to save password to .env file")
        print("   Please check file permissions and try again")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())