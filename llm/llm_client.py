# llm_client.py
"""
Handles LLM assistant creation and response generation for student, parent, and teacher modules.
Supports Gemini via LangChain, with config-driven API key and model selection.
"""

import os
import yaml
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, BaseMessage

class LLMClient:
    """
    LLMClient wraps LangChain's Gemini chat model for prompt-based generation.
    """
    def __init__(self, api_key: str, prompt: str = "", model: str = ""):  # model defaults to empty string
        if not api_key:
            raise ValueError("API key for Gemini LLM is required.")
        self.api_key = api_key
        self.prompt = prompt
        self.model = model if model else None
        if self.model:
            self.llm = ChatGoogleGenerativeAI(api_key=self.api_key, model=self.model)
        else:
            self.llm = ChatGoogleGenerativeAI(api_key=self.api_key)

    def generate_response(self, prompt: str, context: str = "") -> str:
        """
        Generate a response from the LLM using the given prompt and optional context.
        """
        full_prompt = prompt
        if context:
            full_prompt += f"\nContext: {context}"
        # Use BaseMessage if required by LangChain, otherwise HumanMessage (which is a subclass)
        messages: list[BaseMessage] = [HumanMessage(content=full_prompt)]
        try:
            response = self.llm(messages)
            # response.content may be str or list; handle both
            if isinstance(response.content, str):
                return response.content
            elif isinstance(response.content, list):
                return "\n".join(str(item) for item in response.content)
            else:
                return str(response.content)
        except Exception as e:
            return f"LLM Error: {str(e)}"

# Generic factory function

def create_llm_client(api_key: str, prompt: str = "", model: str = "") -> LLMClient:
    """
    Factory to create an LLMClient with optional model selection.
    """
    return LLMClient(api_key, prompt, model)

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'config.yml'))

def run_gemini_llm(prompt: str, context: str = "") -> str:
    """
    Utility to create Gemini LLM client from config.yml and run LLM with a prompt/context using LangChain.
    Reads API key and model from config.yml.
    """
    if not os.path.exists(CONFIG_PATH):
        return "Config file not found."
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
    llm_config = config.get('llm', {})
    api_key = llm_config.get('gemini_api_key')
    model = llm_config.get('gemini_model', "")  # default to empty string
    if not api_key:
        return "Gemini API key not found in config.yml."
    client = create_llm_client(api_key, model=model)
    return client.generate_response(prompt, context)
