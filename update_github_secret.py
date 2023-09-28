import requests
import toml
from base64 import b64encode
from nacl import encoding, public

config = toml.load("config.toml")

OWNER = config["github"]["OWNER"]
REPO = config["github"]["REPO"]
SECRET_NAME = config["github"]["SECRET_NAME"]
GH_TOKEN = config["github"]["GH_TOKEN"]
PUBLIC_KEY = config["github"]["PUBLIC_KEY"]
KEY_ID = config["github"]["KEY_ID"]


def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


def get_repo_public_key():
    """Get a repository public key"""
    response = requests.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}/actions/secrets/public-key",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {GH_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    public_key = response.json()["key"]
    key_id = response.json()["key_id"]
    return public_key, key_id


def update_repo_secret(secret_value=toml.dumps(config)):
    """Update a repository secret"""
    response = requests.put(
        f"https://api.github.com/repos/{OWNER}/{REPO}/actions/secrets/{SECRET_NAME}",
        headers={
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {GH_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        json={"encrypted_value": encrypt(PUBLIC_KEY, secret_value), "key_id": KEY_ID},
    )
    return response.status_code == 204


if __name__ == "__main__":
    if not update_repo_secret():
        print("Update repo secret failed.")
        exit(1)
    print("Update repo secret successfully.")
