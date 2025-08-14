# llm_client.py
# Handles LLM assistant creation for student, parent, and teacher

import yaml
import os
from langchain.llms import Gemini

class LLMClient:
    def __init__(self, api_key: str, prompt: str = ""):
        self.api_key = api_key
        self.prompt = prompt
        self.llm = Gemini(api_key=self.api_key)

    def generate_response(self, prompt: str, context: str = "") -> str:
        # Combine prompt and context for the LLM call
        full_prompt = f"{prompt}\nContext: {context}" if context else prompt
        return self.llm(full_prompt)


# Generic factory function

def create_llm_client(api_key: str, prompt: str = "") -> LLMClient:
    return LLMClient(api_key, prompt)

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'config.yml'))

def run_gemini_llm(prompt: str, context: str = "") -> str:
    """
    Utility to create Gemini LLM client from config.yml and run LLM with a prompt/context using LangChain.
    """
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
    api_key = config['llm']['gemini_api_key']
    client = create_llm_client(api_key)
    return client.generate_response(prompt, context)
