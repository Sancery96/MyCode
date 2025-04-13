import json
from openai import OpenAI
from save_conversations_to_md import save_conversation_to_md
from evn import get_deepseek_api_key, get_deepseek_base_url

# 使用deepseek-chat(deepseek-V3)模型
def use_deepseek_chat():
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

# 使用deepseek-reasoner(deepseek-R1)模型
def use_deepseek_reasoner():
    """
    多轮对话
    """
    api_key = get_deepseek_api_key()
    base_url = get_deepseek_base_url()
    client = OpenAI(api_key=api_key, base_url=base_url)
    # Round 1
    messages = [
        {"role": "system", "content": "请用中文回答用户的问题，分析过程要使用第一性原理思考，输出结果只能使用图表、流程图、mermaid等可视化方式进行呈现"},
        {"role": "user", "content": "普通人如何过好这一生？"},
    ]
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
        stream=False
    )
    reasoning_content = response.choices[0].message.reasoning_content
    content = response.choices[0].message.content
    print("Round 1:")
    print("推理：", reasoning_content)
    print("回答：", content)
    save_conversation_to_md(messages, response, "deepseek-reasoner")
    # Round 2
    messages.append({"role": "assistant", "content": content})
    messages.append({"role": "user", "content": "不工作如何赚钱？"})
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
        stream=False
    )
    reasoning_content = response.choices[0].message.reasoning_content
    content = response.choices[0].message.content
    print("Round 2:")
    print("推理：", reasoning_content)
    print("回答：", content)
    save_conversation_to_md(messages, response, "deepseek-reasoner")

# 使用Fuction Calling
def use_function_calling(query):
    def get_weather(location):
        return f"The weather in {location} is sunny."
    def say_hello(name):
        return f"Hello, {name}!"
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "查询天气，用户需要提供查询地点",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string", "description": "城市名称",
                            "description": "查询天气的地点"
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "say_hello",
                "description": "对用户问好，用户需要提供人名",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "人名"}
                    },
                    
                },
                "required": ["name"]
            }
        }
    ]
    function_map = {
        "get_weather": lambda *agrs: get_weather(*agrs),
        "say_hello": lambda *args: say_hello(*args)
    }
    def send_messages(client, messages, tools):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools,
            stream=False
        )
        return response.choices[0].message
    
    api_key = get_deepseek_api_key()
    base_url = get_deepseek_base_url()
    client = OpenAI(api_key=api_key, base_url=base_url)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ]
    # 用户查询，模型返回函数调用建议
    response_1 = send_messages(client, messages, tools)
    tool_call = response_1.tool_calls[0]
    # print(tool_call)
    # 采用函数调用建议执行对应函数，得到运行结果
    args = json.loads(tool_call.function.arguments)
    result = function_map[tool_call.function.name](args)
    # 把函数执行结果返回大模型，然后让大模型以自然语言返回给用户
    messages.append(response_1)    # append model's function call message
    messages.append({"role":"tool", "tool_call_id":tool_call.id, "content":result})  # append result message
    response_2 = send_messages(client, messages, tools)
    print(response_2.content)
    
    
    

if __name__ == "__main__":
    use_function_calling("北京的天气怎么样？")
    use_function_calling("我的名字是吴琪。")
