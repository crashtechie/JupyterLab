import secrets
import os
def generate_secure_token():
    token = secrets.token_urlsafe(48)
    print("token generated successfully. Set JUPYTER_TOKEN environment variable.")
    return token

def save_token_to_env(token: str, env_file: str = ".env"):
    # check if .env file exists and if token already exists
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("JUPYTER_TOKEN="):
                    # update existing token
                    lines[lines.index(line)] = f"JUPYTER_TOKEN={token}\n"
                    with open(env_file, "w") as fw:
                        fw.writelines(lines)
                    print(f"Token updated in {env_file}")
                    return
    # if not, append new token
    with open(env_file, "a") as f:
        f.write(f"JUPYTER_TOKEN={token}\n")
    print(f"Token saved to {env_file}")
    

if __name__ == "__main__":
    token = generate_secure_token()
    save_token_to_env(token)
    print("process completed.")