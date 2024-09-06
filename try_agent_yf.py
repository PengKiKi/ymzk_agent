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

assert user_proxy.function_map["currency_calculator"]._origin == currency_calculator


with Cache.disk() as cache:
    # start the conversation
    res = user_proxy.initiate_chat(
        chatbot, message="How much is 123.45 USD in EUR?", summary_method="reflection_with_llm", cache=cache
    )


print("Chat summary:", res.summary)





# chatbot = autogen.AssistantAgent(
#     name="chatbot",
#     system_message="For currency exchange tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
#     llm_config=llm_config,
# )

# # create a UserProxyAgent instance named "user_proxy"
# user_proxy = autogen.UserProxyAgent(
#     name="user_proxy",
#     is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
#     human_input_mode="NEVER",
#     max_consecutive_auto_reply=10,
# )


# class Currency(BaseModel):
#     currency: Annotated[CurrencySymbol, Field(..., description="Currency symbol")]
#     amount: Annotated[float, Field(0, description="Amount of currency", ge=0)]


# # another way to register a function is to use register_function instead of register_for_execution and register_for_llm decorators
# def currency_calculator(
#     base: Annotated[Currency, "Base currency: amount and currency symbol"],
#     quote_currency: Annotated[CurrencySymbol, "Quote currency symbol"] = "USD",
# ) -> Currency:
#     quote_amount = exchange_rate(base.currency, quote_currency) * base.amount
#     return Currency(amount=quote_amount, currency=quote_currency)


# autogen.agentchat.register_function(
#     currency_calculator,
#     caller=chatbot,
#     executor=user_proxy,
#     description="Currency exchange calculator.",
# )


# with Cache.disk() as cache:
#     # start the conversation
#     res = user_proxy.initiate_chat(
#         chatbot, message="How much is 112.23 Euros in US Dollars?", summary_method="reflection_with_llm", cache=cache
#     )
    
# print("Chat summary:", res.summary)


# with Cache.disk() as cache:
#     # start the conversation
#     res = user_proxy.initiate_chat(
#         chatbot,
#         message="How much is 123.45 US Dollars in Euros?",
#         cache=cache,
#     )
    
# print("Chat history:", res.chat_history)

