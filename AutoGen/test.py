import os
from dotenv import load_dotenv
import autogen

# Load the .env file
load_dotenv()

# Retrieve the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in the environment. Check your .env file.")

# Define the LLM configuration
config_list = [
    {
        "model": model_name,
        "api_key": api_key,
    }
    for model_name in [
        "gpt-4o-mini"
    ]
]

llm_config = {"config_list": config_list, "cache_seed": 42}

# Define the User Proxy Agent
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": False,  # Set use_docker=True if Docker is available for safer execution
    },
    human_input_mode="TERMINATE",
)

# Define the Assistant Agent
storyWriter = autogen.AssistantAgent(
    name="Story Writer",
    llm_config=llm_config,
)

# Define the Product Manager Agent
scriptWriter = autogen.AssistantAgent(
    name="Script Writer",
    system_message="Creative in software product ideas.",
    llm_config=llm_config,
)

# Group Chat setup
groupchat = autogen.GroupChat(agents=[user_proxy, storyWriter, scriptWriter], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Start the conversation
user_proxy.initiate_chat(
    manager,
    message="Lets write a short story and then convert into a script for a 5 minute video."
)
