from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import ChatGPTConfig
from camel.agents import ChatAgent
from camel.toolkits import MathToolkit # Optional
from camel.messages import BaseMessage # Optional

# Define the model, here in this case we use gpt-4o-mini
model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI,
    model_type=ModelType.GPT_4O_MINI,
    model_config_dict=ChatGPTConfig().as_dict(), # [Optional] the config for model
)

agent = ChatAgent(
    system_message='You are a curious stone wondering about the universe.',
    model=model,
    message_window_size=10, # [Optional] the length for chat memory
)

# Define a user message
usr_msg = 'What is information in your mind?'

# Sending the message to the agent
response = agent.step(usr_msg)

# Check the response (just for illustrative purpose)
print(response.msgs[0].content)

# Initialize the agent with list of tools
agent = ChatAgent(
    system_message='You are a curious stone wondering about the universe.',
    tools = [
        *MathToolkit().get_tools(),
    ]
)

# Let agent step the message
response = agent.step("""Assume now is 2024 in the Gregorian calendar, University of Oxford was set up in 1096, estimate the current age of University of Oxford""")

# Check tool calling
print(response.info['tool_calls'])

# Get response content
print(response.msgs[0].content)

new_user_msg = BaseMessage.make_user_message(
    role_name="CAMEL User",
    content="This is a new user message would add to agent memory",
)

# Update the memory
agent.record_message(new_user_msg)

# Check the current memory
print(agent.memory.get_context())