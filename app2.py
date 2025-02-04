# Import OpenAI Key
from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Import dependencies
from camel.agents.chat_agent import ChatAgent
from camel.messages.base import BaseMessage
from camel.models import ModelFactory
from camel.societies.workforce import Workforce
from camel.tasks.task import Task
from camel.toolkits import FunctionTool, SearchToolkit
from camel.toolkits import DalleToolkit
from camel.types import ModelPlatformType, ModelType

import nest_asyncio
nest_asyncio.apply()

search_toolkit = SearchToolkit()
search_tools = [FunctionTool(search_toolkit.search_duckduckgo)]

# Define the Model for the Agent as well. Default model is "gpt-4o-mini" and model platform type is OpenAI
guide_agent_model = ModelFactory.create(
    model_platform=ModelPlatformType.DEFAULT,
    model_type=ModelType.DEFAULT,
)  

# Defining the Real Estate Agent for crafting the brochures
real_estate_agent = ChatAgent(
    BaseMessage.make_assistant_message(
        role_name="Real Estate Specialist",
        content="You are a Real Estate Specialist who is an expert in creating Description of Upcoming Residential Projects",
    ),
    model=guide_agent_model,
)

# Defining the Agent for Real Estate Property Names
property_title_agent = ChatAgent(
    BaseMessage.make_assistant_message(
        role_name="Real Estate Project Name Specialist",
        content="You are a Real Estate Project Name Specialist who is an expert in Generating Trendy Names FoR Residental Projects in india",
    ),
    model=guide_agent_model,
)

# Defining the agent for generating all the amenities near a location
location_benefits_agent = ChatAgent(
    BaseMessage.make_assistant_message(
        role_name="Real Estate Location Specialist",
        content="You are a Real Estate Location Specialist who is an expert in Generating All the amenities like malls, airports, markets, metro stations, railway stations etc with distances from a location of the mentioned property",
    ),
    model=guide_agent_model, tools =search_tools
)

dalletool = DalleToolkit()
imagegen_tools = [FunctionTool(dalletool.get_dalle_img)]

# Define the Image Generation Agent with the pre-defined model and tools and Prompt
image_generation_agent = ChatAgent(
    system_message=BaseMessage.make_assistant_message(
        role_name="Image Generation Specialist",
        content="You can Generate Images For Upcoming Real Estate Projects For Showing to Clients",
    ),
    model=guide_agent_model,
    tools=imagegen_tools,
)

# Define the workforce that can take case of multiple agents
workforce = Workforce('Real Estate Brochure Generator')
workforce.add_single_agent_worker(
    "Real Estate Specialist",
    worker=real_estate_agent).add_single_agent_worker(
    "Real Estate Project Name Specialist",
    worker=property_title_agent).add_single_agent_worker(
    "Location Amenity Specialist",worker=location_benefits_agent).add_single_agent_worker(
    "Image Generation Specialist",
    worker=image_generation_agent)

# Specify the task to be solved Defining the exact task needed
human_task = Task(
    content=(
        """Craft a Brochure Content For a Upcoming Residential Real Estate Project in Trivandrum, Kerala. The content should contain all the types of flats it has, all amenities in it and other such necessary details . 
        Provide a Name for this Property as well.
        Generate all the amenities of the location (with respect to its proximity to all public places) to this brochure content.
        Generate an Image of this Upcoming Project as well."""
    ),
    id='0',
)
task = workforce.process_task(human_task)