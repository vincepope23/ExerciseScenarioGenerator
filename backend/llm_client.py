from abc import ABC, abstractmethod
from typing import Optional

class LLMClient(ABC):
    def __init__(self, model_name: str, api_token: Optional[str] = None):
        self.model_name = model_name
        self.api_token = api_token

    @abstractmethod
    def query(self, prompt: str) -> str:
        pass

class LLMClientMistral(LLMClient):
    def __init__(self, model_name: str = "mistral-large-latest", api_token: Optional[str] = None):
        super().__init__(model_name, api_token)
        from mistralai.client import Mistral
        self.client = Mistral(api_key=api_token)

    def query(self, prompt: str) -> str:
        response = self.client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content

class LLMClientClaude(LLMClient):
    def __init__(self, model_name: str = "claude-3-sonnet-20240229", api_token: Optional[str] = None):
        super().__init__(model_name, api_token)
        from anthropic import Anthropic
        self.client = Anthropic(api_key=api_token)

    def query(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

class LLMClientOpenAI(LLMClient):
    def __init__(self, model_name: str = "gpt-4", api_token: Optional[str] = None):
        super().__init__(model_name, api_token)
        from openai import OpenAI
        self.client = OpenAI(api_key=api_token)

    def query(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

def llm_client_factory(client_type: str, api_token: Optional[str] = None):
    if client_type == "mistral":
        return LLMClientMistral("mistral-large-latest", api_token)
    elif client_type == "claude":
        return LLMClientClaude("claude-3-sonnet-20240229", api_token)
    elif client_type == "openai":
        return LLMClientOpenAI("gpt-4", api_token)
    else:
        raise ValueError(f"Unsupported client type: {client_type}")