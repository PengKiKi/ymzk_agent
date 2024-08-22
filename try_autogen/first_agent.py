from autogen import ConversableAgent
import pprint


llm_config = {
    "model": "llama3.1:8b",  # or gpt-3.5-turbo-1106 / gpt-4-1106-preview,
    # "base_url": "http://192.168.193.231:11434/v1",  # or forward url / other llm url
    "base_url": "http://10.111.79.202:11434/v1",  # or forward url / other llm url
    "api_key":  "ollama",
    "price" : [0, 0],
    }


agent = ConversableAgent(
    name="chatbot",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# reply = agent.generate_reply(
#     messages=[{"content": "Tell me a joke.", "role": "user"}]
# )
# print(reply)


# reply = agent.generate_reply(
#     messages=[{"content": "Repeat the joke.", "role": "user"}]
# )
# print(reply)



# setup role

cathy = ConversableAgent(
    name="cathy",
    system_message=
    "Your name is Cathy and you are a stand-up comedian.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

joe = ConversableAgent(
    name="joe",
    system_message=
    "Your name is Joe and you are a stand-up comedian. "
    "Start the next joke from the punchline of the previous joke.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)



# chat_result = joe.initiate_chat(
#     recipient=cathy, 
#     message="I'm Joe. Cathy, let's keep the jokes rolling.",
#     max_turns=5,
# )
# pprint.pprint(chat_result.chat_history)

# pprint.pprint(chat_result.cost)
# pprint.pprint(chat_result.summary)


# # run summary
# chat_result = joe.initiate_chat(
#     cathy, 
#     message="I'm Joe. Cathy, tell me a joke that not a joke.", 
#     max_turns=5, 
#     summary_method="reflection_with_llm",
#     summary_prompt="Summarize the conversation",
# )

# pprint.pprint(chat_result.summary)


# Chat Termination
cathy = ConversableAgent(
    name="cathy",
    system_message=
    "Your name is Cathy and you are a stand-up comedian. "
    "When you're ready to end the conversation, say 'I gotta go'.",
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"],
)

joe = ConversableAgent(
    name="joe",
    system_message=
    "Your name is Joe and you are a stand-up comedian. "
    "When you're ready to end the conversation, say 'I gotta go'.",
    llm_config=llm_config,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "I gotta go" in msg["content"] or "Goodbye" in msg["content"],
)

chat_result = joe.initiate_chat(
    recipient=cathy,
    message="I'm Joe. Cathy, tell me how to get a driver for our in car testing."
)

cathy.send(message="What's last joke we talked about?", recipient=joe)
