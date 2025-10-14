import secrets

def generate_token():
    """Generate a secure random token for Jupyter Notebook access."""
    return secrets.token_urlsafe(32)

if __name__ == "__main__":
    token = generate_token()
    print(f"JUPYTER_TOKEN={token}")