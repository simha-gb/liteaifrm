import openai
from utils.secdata  import get_openai_api_key

def get_client(config=None):
    api_key = get_openai_api_key(config)
    openai.api_key = api_key
    return openai