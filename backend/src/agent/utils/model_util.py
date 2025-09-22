import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()
async def get_model():
    model_name = os.getenv('MODEL_NAME')
    api_key = os.getenv('API_KEY')
    base_url = os.getenv('BASE_URL')
    model_name = f'openai:{model_name}'
    return init_chat_model(model_name,api_key=api_key,base_url=base_url)