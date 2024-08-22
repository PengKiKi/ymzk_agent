import autogen
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json


config_list = [    
    {
    "model": "llama2:13b",  # or gpt-3.5-turbo-1106 / gpt-4-1106-preview,
    # "base_url": "http://192.168.193.231:11434/v1",  # or forward url / other llm url
    "base_url": "http://10.111.79.202:11434/v1",  # or forward url / other llm url
    "api_key":  "ollama"
    }
]


assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})


user_proxy = UserProxyAgent("user_proxy", code_execution_config=False)

user_proxy.initiate_chat(assistant, message="给我讲个笑话.")
