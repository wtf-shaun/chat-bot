import os
import requests

class LLMError(RuntimeError): pass
class LLMProvider:
    def generate(self, messages, temperature=.7, max_tokens=200): raise NotImplementedError

class MockProvider(LLMProvider):
    def generate(self, messages, temperature=.7, max_tokens=200):
        text = messages[-1]["content"] if messages else ""
        return "I don't know enough from the imported chat to answer that." if "yesterday" in text.lower() else "got you — tell me more"

class OpenAICompatibleProvider(LLMProvider):
    def __init__(self, api_key, model, base_url): self.api_key, self.model, self.base_url = api_key, model, (base_url or "https://api.openai.com/v1").rstrip("/")
    def generate(self, messages, temperature=.7, max_tokens=200):
        if not self.api_key or not self.model: raise LLMError("LLM_API_KEY and LLM_MODEL are required")
        try:
            response = requests.post(f"{self.base_url}/chat/completions", json={"model": self.model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}, headers={"Authorization": f"Bearer {self.api_key}"}, timeout=60)
            response.raise_for_status(); return response.json()["choices"][0]["message"]["content"].strip()
        except (requests.RequestException, KeyError, IndexError) as exc: raise LLMError("The language model request failed") from exc

def get_provider(config):
    if config.get("LLM_PROVIDER", "mock").lower() == "mock": return MockProvider()
    return OpenAICompatibleProvider(config.get("LLM_API_KEY"), config.get("LLM_MODEL"), config.get("LLM_BASE_URL"))
