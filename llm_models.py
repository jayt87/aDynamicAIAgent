from langchain.chat_models import init_chat_model
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize LLMs
llm_reasoning04mini = init_chat_model(
    "azure_openai:o4-mini",
    azure_deployment="o4-mini",
    reasoning_effort="high",
)

llm_reasoning03pro = AzureChatOpenAI(
    azure_deployment="o3-pro",
    model="o3-pro",
    api_version="2025-04-01-preview",
    use_responses_api=True,
    reasoning={
        "effort": "high",  # can be "low", "medium", or "high"
        "summary": "auto",  # can be "auto", "concise", or "detailed"
    }
)

grokllm = init_chat_model(
    "azure_openai:grok-3",
    azure_deployment="grok-3",
)

llm5 = init_chat_model(
    "azure_openai:gpt-5",
    azure_deployment="gpt-5"
)

llm41 = init_chat_model(
    "azure_openai:gpt-4.1",
    azure_deployment="gpt-4.1"
)

llm5mini = init_chat_model(
    "azure_openai:gpt-5-mini",
    azure_deployment="gpt-5-mini"
)