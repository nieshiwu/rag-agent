import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model, BaseChatModel

load_dotenv()

# Configuration for Qwen/DashScope
api_key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
model_name = os.getenv("MODEL_NAME", "qwen-max")

def get_llm(temperature: float = 0.7) -> BaseChatModel:
    """
    Returns a configured ChatOpenAI instance (using Qwen/DashScope).
    """
    return init_chat_model(
        model="openai:"+model_name,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
    )
