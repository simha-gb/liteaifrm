import os
from dotenv import load_dotenv

def get_openai_api_key(config=None):
    # 1. Через конфиг (если есть)
    if config and "openai_api_key" in config:
        return config["openai_api_key"]
    # 2. Через .env или переменные среды
    load_dotenv()
    return os.environ.get("OPENAI_API_KEY")
