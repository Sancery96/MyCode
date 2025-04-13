from datetime import datetime
from openai import OpenAI
from evn import get_deepseek_api_key, get_deepseek_base_url

def save_conversation_to_md(messages, response, model_name):
    # 获取当前时间
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 格式化对话内容
    md_content = f"## 对话时间: {timestamp}\n\n"
    md_content += f"**使用的模型**: {model_name}\n\n"
    
    # 添加系统消息
    for msg in messages:
        if msg["role"] == "system":
            md_content += f"**系统**: {msg['content']}\n\n"
    
    # 添加用户消息
    for msg in messages:
        if msg["role"] == "user":
            md_content += f"**用户**: {msg['content']}\n\n"
    
    # 添加 AI 回复
    if model_name == "deepseek-reasoner":
        md_content += f"**推理**：{response.choices[0].message.reasoning_content}\n\n"
        md_content += "---\n\n"
        md_content += f"**AI**: {response.choices[0].message.content}\n\n"
        md_content += "---\n\n"
    else:
        md_content += f"**AI**: {response.choices[0].message.content}\n\n"
    md_content += "---\n\n"  # 添加分隔线
    
    # 追加到文件
    with open(r"D:\MyCode\Documents\conversation_history.md", "a", encoding="utf-8") as f:
        f.write(md_content)

if __name__ == "__main__":
    api_key = get_deepseek_api_key()
    base_url = get_deepseek_base_url()
    client = OpenAI(api_key=api_key, base_url=base_url)
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ]
    messages = [
        {"role": "system", "content": "请使用中文回答用户的提问"},
        {"role": "user", "content": "请用第一性原理说明如何与大模型对话能得到最好的效果"},
    ]
    messages = [
        {"role": "system", "content": "请使用中文回答用户的提问"},
        {"role": "user", "content": "对于我不了解的领域，该如何提问，我不知道有哪些思维模型，思考框架，无法对问题做出具象化的限制"},
    ]
    messages = [
        {"role": "system", "content": "请使用中文回答用户的提问"},
        {"role": "user", "content": "如何避免在了解一个新领域时，陷入细节，对于不理解的细节应该怎么处理"},
    ]
    messages = [
        {"role": "system", "content": "请使用中文回答用户的提问"},
        {"role": "user", "content": "在学习新知识时，是理解重要还是记录重要，花时间把笔记做的好看是否有必要，如果不整理笔记，如何避免遗忘？如果整理笔记，如何避免不去回顾？如何避免耗费时间过多？"},
    ]
    messages = [
        {"role": "system", "content": "请使用中文回答用户的提问"},
        {"role": "user", "content": "我想借助大模型学习一个新的领域（即我的知识来源于大模型的输出），我该如何提问才能得到完整且体系化的教学内容"},
    ]
    messages = [
        {"role": "system", "content": "请使用中文回答用户的提问"},
        {"role": "user", "content": "如何获取高质量的信息？有什么渠道？有什么提问技巧？"},
    ]
    model_name = "deepseek-chat"
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=False
    )

    save_conversation_to_md(messages, response, model_name)
    print(response.choices[0].message.content)