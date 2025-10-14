import secrets

def generate_password():
    """Generate a secure random password for PostgreSQL access."""
    return secrets.token_urlsafe(32)

if __name__ == "__main__":
    password = generate_password()
    print(f"POSTGRES_PASSWORD={password}")