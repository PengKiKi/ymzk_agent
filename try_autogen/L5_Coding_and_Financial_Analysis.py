#!/usr/bin/env python
# coding: utf-8

# # Lesson 5: Coding and Financial Analysis

# ## Setup

# In[ ]:


llm_config = {"model": "gpt-4-turbo"}


# ## Define a code executor

# In[ ]:


from autogen.coding import LocalCommandLineCodeExecutor


# In[ ]:


executor = LocalCommandLineCodeExecutor(
    timeout=60,
    work_dir="coding",
)


# ## Create agents 

# In[ ]:


from autogen import ConversableAgent, AssistantAgent


# ### 1. Agent with code executor configuration

# In[ ]:


code_executor_agent = ConversableAgent(
    name="code_executor_agent",
    llm_config=False,
    code_execution_config={"executor": executor},
    human_input_mode="ALWAYS",
    default_auto_reply=
    "Please continue. If everything is done, reply 'TERMINATE'.",
)


# ### 2. Agent with code writing capability

# In[ ]:


code_writer_agent = AssistantAgent(
    name="code_writer_agent",
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
)


# In[ ]:


code_writer_agent_system_message = code_writer_agent.system_message


# In[ ]:


print(code_writer_agent_system_message)


# ## The task!
# 
# Ask the two agents to collaborate on a stock analysis task.

# In[ ]:


import datetime

today = datetime.datetime.now().date()
message = f"Today is {today}. "\
"Create a plot showing stock gain YTD for NVDA and TLSA. "\
"Make sure the code is in markdown code block and save the figure"\
" to a file ytd_stock_gains.png."""


# <p style="background-color:#ECECEC; padding:15px; "> <b>Note:</b> In this lesson, you will use GPT 4 for better results. Please note that the lesson has a quota limit. If you want to explore the code in this lesson further, we recommend trying it locally with your own API key.

# **Note**: You might see a different set of outputs than those shown in the video. The agents collaborate to generate the code needed for your task, and they might produce code with errors in the process. However, they will ultimately provide a correct code in the end.

# In[ ]:


chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message=message,
)


# ## Let's see the plot!
# 
# **Note**: 
# * Your plot might differ from the one shown in the video because the LLM's freestyle code generation could choose a different plot type, such as a bar plot. 
# * You can re-run the previous cell and check the generated code. If it produces a bar plot, remember you can directly specify your preference by asking for a specific plot type instead of a bar plot.

# In[ ]:


import os
from IPython.display import Image

Image(os.path.join("coding", "ytd_stock_gains.png"))


# **Note**: The agent will automatically save the code in a .py file and the plot in a .png file. To access and check the files generated by the agents, go to the `File` menu and select `Open....` Then, open the folder named `coding` to find all the generated files.

# ## User-Defined Functions
# 
# Instead of asking LLM to generate the code for downloading stock data 
# and plotting charts each time, you can define functions for these two tasks and have LLM call these functions in the code.

# In[ ]:


def get_stock_prices(stock_symbols, start_date, end_date):
    """Get the stock prices for the given stock symbols between
    the start and end dates.

    Args:
        stock_symbols (str or list): The stock symbols to get the
        prices for.
        start_date (str): The start date in the format 
        'YYYY-MM-DD'.
        end_date (str): The end date in the format 'YYYY-MM-DD'.
    
    Returns:
        pandas.DataFrame: The stock prices for the given stock
        symbols indexed by date, with one column per stock 
        symbol.
    """
    import yfinance

    stock_data = yfinance.download(
        stock_symbols, start=start_date, end=end_date
    )
    return stock_data.get("Close")


# In[ ]:


def plot_stock_prices(stock_prices, filename):
    """Plot the stock prices for the given stock symbols.

    Args:
        stock_prices (pandas.DataFrame): The stock prices for the 
        given stock symbols.
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 5))
    for column in stock_prices.columns:
        plt.plot(
            stock_prices.index, stock_prices[column], label=column
                )
    plt.title("Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.savefig(filename)


# ### Create a new executor with the user-defined functions

# In[ ]:


executor = LocalCommandLineCodeExecutor(
    timeout=60,
    work_dir="coding",
    functions=[get_stock_prices, plot_stock_prices],
)


# In[ ]:


code_writer_agent_system_message += executor.format_functions_for_prompt()
print(code_writer_agent_system_message)


# ### Let's update the agents with the new system message

# In[ ]:


code_writer_agent = ConversableAgent(
    name="code_writer_agent",
    system_message=code_writer_agent_system_message,
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",
)


# In[ ]:


code_executor_agent = ConversableAgent(
    name="code_executor_agent",
    llm_config=False,
    code_execution_config={"executor": executor},
    human_input_mode="ALWAYS",
    default_auto_reply=
    "Please continue. If everything is done, reply 'TERMINATE'.",
)


# ### Start the same task again!

# In[ ]:


chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message=f"Today is {today}."
    "Download the stock prices YTD for NVDA and TSLA and create"
    "a plot. Make sure the code is in markdown code block and "
    "save the figure to a file stock_prices_YTD_plot.png.",
)


# ### Plot the results

# In[ ]:


Image(os.path.join("coding", "stock_prices_YTD_plot.png"))


# **Note**: The agent will automatically save the code in a .py file and the plot in a .png file. To access and check the files generated by the agents, go to the `File` menu and select `Open....` Then, open the folder named `coding` to find all the generated files.
