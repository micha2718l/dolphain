from huggingface_hub import HfApi

try:
    api = HfApi()
    user = api.whoami()
    print(f"Logged in as: {user['name']}")
except Exception as e:
    print(f"Not logged in or error: {e}")
