import os
from dotenv import load_dotenv

load_dotenv()


def get_deepseek_api_key():
    return os.getenv("DEEPSEEK_API_KEY")

def get_deepseek_base_url():
    return os.getenv("DEEPSEEK_BASE_URL")


