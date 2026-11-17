"""
LLM Integration Layer - Configurable provider abstraction
Supports: Google Gemini, Anthropic Claude, Local Ollama
"""

import os
import json
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
from enum import Enum
import httpx


class LLMProvider(str, Enum):
    """Available LLM providers"""
    GOOGLE_GEMINI = "google_gemini"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


class BaseLLMClient(ABC):
    """Abstract base for LLM clients"""
    
    @abstractmethod
    def generate(self, prompt: str, system: str = "", structured_output: Optional[Dict] = None) -> str:
        """Generate text response"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if client is available"""
        pass


class GoogleGeminiClient(BaseLLMClient):
    """Google Gemini LLM client"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = model
        self.client = None
        
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.client = genai
                print(f"✓ Google Gemini initialized: {self.model}")
            except Exception as e:
                print(f"✗ Gemini initialization failed: {e}")
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def generate(self, prompt: str, system: str = "", structured_output: Optional[Dict] = None) -> str:
        """Generate using Google Gemini with structured output support"""
        if not self.is_available():
            raise RuntimeError("Google Gemini client not available")
        
        try:
            if structured_output:
                # Use structured output format
                prompt_with_schema = f"""{system}

{prompt}

Return response in JSON format matching this schema:
{json.dumps(structured_output, indent=2)}

Respond ONLY with valid JSON, no additional text."""
            else:
                prompt_with_schema = f"{system}\n\n{prompt}"
            
            model = self.client.GenerativeModel(self.model)
            response = model.generate_content(prompt_with_schema)
            
            text = response.text
            
            # If structured output was requested, try to parse JSON
            if structured_output:
                try:
                    # Extract JSON from response
                    start_idx = text.find('{')
                    end_idx = text.rfind('}') + 1
                    if start_idx != -1 and end_idx > start_idx:
                        json_str = text[start_idx:end_idx]
                        parsed = json.loads(json_str)
                        return json.dumps(parsed)
                except:
                    pass
            
            return text
        
        except Exception as e:
            raise RuntimeError(f"Gemini generation failed: {e}")


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude LLM client"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.client = None
        
        if self.api_key:
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=self.api_key)
                print(f"✓ Anthropic Claude initialized: {self.model}")
            except Exception as e:
                print(f"✗ Anthropic initialization failed: {e}")
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def generate(self, prompt: str, system: str = "", structured_output: Optional[Dict] = None) -> str:
        """Generate using Claude"""
        if not self.is_available():
            raise RuntimeError("Anthropic client not available")
        
        try:
            if structured_output:
                prompt_with_schema = f"""{prompt}

Return response in JSON format matching this schema:
{json.dumps(structured_output, indent=2)}

Respond ONLY with valid JSON."""
            else:
                prompt_with_schema = prompt
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=system,
                messages=[
                    {"role": "user", "content": prompt_with_schema}
                ]
            )
            
            return response.content[0].text
        
        except Exception as e:
            raise RuntimeError(f"Claude generation failed: {e}")


class OllamaClient(BaseLLMClient):
    """Local Ollama LLM client"""
    
    def __init__(self, model: str = "mistral", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
        print(f"✓ Ollama initialized: {self.model} at {self.host}")
    
    def is_available(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = httpx.get(f"{self.host}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def generate(self, prompt: str, system: str = "", structured_output: Optional[Dict] = None) -> str:
        """Generate using Ollama"""
        if not self.is_available():
            raise RuntimeError("Ollama server not available")
        
        try:
            full_prompt = f"{system}\n\n{prompt}"
            
            if structured_output:
                full_prompt += f"\n\nReturn JSON: {json.dumps(structured_output)}"
            
            response = httpx.post(
                f"{self.host}/api/generate",
                json={"model": self.model, "prompt": full_prompt, "stream": False},
                timeout=30
            )
            
            result = response.json()
            return result.get("response", "")
        
        except Exception as e:
            raise RuntimeError(f"Ollama generation failed: {e}")


class LLMManager:
    """Central manager for LLM providers"""
    
    def __init__(self, provider: str = "google_gemini"):
        self.provider_name = provider
        self.client: Optional[BaseLLMClient] = None
        self._initialize_provider()
    
    def _initialize_provider(self):
        """Initialize the configured provider"""
        if self.provider_name == LLMProvider.GOOGLE_GEMINI:
            self.client = GoogleGeminiClient()
        elif self.provider_name == LLMProvider.ANTHROPIC:
            self.client = AnthropicClient()
        elif self.provider_name == LLMProvider.OLLAMA:
            self.client = OllamaClient()
        else:
            raise ValueError(f"Unknown provider: {self.provider_name}")
        
        if not self.client.is_available():
            print(f"⚠️  {self.provider_name} not available, consider fallback")
    
    def generate(self, prompt: str, system: str = "", structured_output: Optional[Dict] = None) -> str:
        """Generate response"""
        if not self.client or not self.client.is_available():
            raise RuntimeError(f"LLM provider {self.provider_name} not available")
        
        return self.client.generate(prompt, system, structured_output)
    
    def is_available(self) -> bool:
        """Check availability"""
        return self.client is not None and self.client.is_available()


# Global LLM manager
def get_llm_manager() -> LLMManager:
    """Get configured LLM manager"""
    provider = os.getenv("LLM_PROVIDER", LLMProvider.GOOGLE_GEMINI)
    return LLMManager(provider=provider)
