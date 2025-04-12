from openai import OpenAI
from .. import get_deepseek_api_key, get_deepseek_base_url

if __name__ == "__main__":
    api_key = get_deepseek_api_key()
    base_url = get_deepseek_base_url()
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ],
        stream=False
    )

    print(response.choices[0].message.content)
