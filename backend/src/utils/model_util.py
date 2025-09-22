from langchain.chat_models import init_chat_model
async def get_model(model_name):
    return init_chat_model(model_name)