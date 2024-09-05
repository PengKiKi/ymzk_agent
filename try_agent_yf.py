from IPython.display import Image, display

import autogen
from autogen.coding import LocalCommandLineCodeExecutor
from typing import Literal

from pydantic import BaseModel, Field
from typing_extensions import Annotated

import autogen
from autogen.cache import Cache


llm_config = {
    "model": "llama3.1:8b",  # or gpt-3.5-turbo-1106 / gpt-4-1106-preview,
    "base_url": "http://192.168.193.231:11434/v1",  # or forward url / other llm url
    # "base_url": "http://10.111.79.202:11434/v1",  # or forward url / other llm url
    "api_key":  "ollama",
    "price" : [0, 0],
    }


chatbot = autogen.AssistantAgent(
    name="chatbot",
    system_message="For currency exchange tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
    
    llm_config={
        "cache_seed": 41,  # seed for caching and reproducibility
        "config_list": [llm_config],  # a list of OpenAI API configurations
        # "temperature": 0,  # temperature for sampling
    },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={
        # the executor to run the generated code
        # "executor": LocalCommandLineCodeExecutor(work_dir="coding"),
        "use_docker":False,
    },
)


CurrencySymbol = Literal["USD", "EUR"]


def exchange_rate(base_currency: CurrencySymbol, quote_currency: CurrencySymbol) -> float:
    if base_currency == quote_currency:
        return 1.0
    elif base_currency == "USD" and quote_currency == "EUR":
        return 1 / 1.1
    elif base_currency == "EUR" and quote_currency == "USD":
        return 1.1
    else:
        raise ValueError(f"Unknown currencies {base_currency}, {quote_currency}")


@user_proxy.register_for_execution()
@chatbot.register_for_llm(description="Currency exchange calculator.")
def currency_calculator(
    base_amount: Annotated[float, "Amount of currency in base_currency"],
    base_currency: Annotated[CurrencySymbol, "Base currency"] = "USD",
    quote_currency: Annotated[CurrencySymbol, "Quote currency"] = "EUR",
) -> str:
    quote_amount = exchange_rate(base_currency, quote_currency) * base_amount
    return f"{quote_amount} {quote_currency}"


print(chatbot.llm_config["tools"])
