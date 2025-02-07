import streamlit as st
import os
import re
from dotenv import load_dotenv
from camel.agents.chat_agent import ChatAgent
from camel.messages.base import BaseMessage
from camel.models import ModelFactory
from camel.societies.workforce import Workforce
from camel.tasks.task import Task
from camel.toolkits import FunctionTool, SearchToolkit, DalleToolkit
from camel.types import ModelPlatformType, ModelType

# Load environment variables
load_dotenv()

def set_openai_key():
    api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        st.sidebar.success("API Key Set Successfully")

def remove_images():
    folder_path = "img"

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path): 
                os.remove(file_path)
        print("All files deleted from 'img' folder.")
    else:
        print("'img' folder does not exist.")

remove_images()

def create_agents():
    search_toolkit = SearchToolkit()
    search_tools = [FunctionTool(search_toolkit.search_duckduckgo)]
    dalletool = DalleToolkit()
    imagegen_tools = [FunctionTool(dalletool.get_dalle_img)]

    guide_agent_model = ModelFactory.create(
        model_platform=ModelPlatformType.DEFAULT,
        model_type=ModelType.DEFAULT,
    )

    real_estate_agent = ChatAgent(
        BaseMessage.make_assistant_message(
            role_name="Real Estate Specialist",
            content="You are a Real Estate Specialist who creates descriptions for upcoming residential projects.",
        ),
        model=guide_agent_model,
    )

    property_title_agent = ChatAgent(
        BaseMessage.make_assistant_message(
            role_name="Real Estate Project Name Specialist",
            content="You generate trendy names for residential projects in India.",
        ),
        model=guide_agent_model,
    )

    location_benefits_agent = ChatAgent(
        BaseMessage.make_assistant_message(
            role_name="Real Estate Location Specialist",
            content="You list all amenities near a given location, including malls, airports, markets, and metro stations, with distances.",
        ),
        model=guide_agent_model,
        tools=search_tools,
    )

    image_generation_agent = ChatAgent(
        BaseMessage.make_assistant_message(
            role_name="Image Generation Specialist",
            content="You generate images for upcoming real estate projects.",
        ),
        model=guide_agent_model,
        tools=imagegen_tools,
    )

    workforce = Workforce("Real Estate Brochure Generator")
    workforce.add_single_agent_worker("Real Estate Specialist", worker=real_estate_agent)
    workforce.add_single_agent_worker("Real Estate Project Name Specialist", worker=property_title_agent)
    workforce.add_single_agent_worker("Location Amenity Specialist", worker=location_benefits_agent)
    workforce.add_single_agent_worker("Image Generation Specialist", worker=image_generation_agent)
    
    return workforce

def display_markdown_with_images(content):
    """
    Parses markdown content and displays text with images in the correct order.
    """
    # Regex to find image patterns ![Alt Text](image_path)
    pattern = r"!\[(.*?)\]\((.*?)\)"
    
    # Splitting text based on image matches
    parts = re.split(pattern, content)

    i = 0
    while i < len(parts):
        text = parts[i]  # Normal text
        if text.strip():
            st.markdown(text)  # Display text as Markdown
        
        if i + 1 < len(parts):  # Check if there's an image next
            alt_text = parts[i + 1]  # Extract image alt text
            img_path = re.sub(r'^sandbox:', '', parts[i + 2])  # Extract image path
            st.image(img_path, caption=alt_text)  # Show image with caption
            
        i += 3  # Move to the next text/image pair

def main():
    st.title("Real Estate Brochure Generator")
    set_openai_key()
    workforce = create_agents()
    
    user_input = st.text_area("Enter the details of the real estate project:", "Craft a brochure for a residential project in Trivandrum, Kerala.")
    if st.button("Generate Brochure"):
        if os.getenv("OPENAI_API_KEY"):
            with st.spinner("Generating brochure..."):
                human_task = Task(content=user_input, id='0')
                response_task = workforce.process_task(human_task)
                responses = response_task.result
                print(responses)
                display_markdown_with_images(responses)
        else:
            st.error("Please enter your OpenAI API key in the sidebar.")

if __name__ == "__main__":
    main()
