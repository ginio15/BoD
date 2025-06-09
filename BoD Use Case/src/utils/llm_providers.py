"""
LLM Provider Manager for BoD Presentation Analysis System

Handles integration with multiple LLM providers (Mistral, OpenAI, Ollama)
with cost tracking and provider comparison functionality.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, Union
from abc import ABC, abstractmethod
import time
from dataclasses import dataclass, field

# LLM Provider imports
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from config.settings import Config

logger = logging.getLogger(__name__)

@dataclass
class LLMResponse:
    """Standardized response from LLM providers"""
    content: str
    provider: str
    model: str
    tokens_used: int
    cost: float
    response_time: float
    confidence: Optional[float] = None
    error: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

@dataclass
class ProviderUsage:
    """Track usage and costs for each provider"""
    provider: str
    total_tokens: int = 0
    total_cost: float = 0.0
    request_count: int = 0
    error_count: int = 0
    last_used: Optional[str] = None

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, provider_name: str, config: Dict[str, Any]):
        self.provider_name = provider_name
        self.config = config
        self.usage = ProviderUsage(provider=provider_name)
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate response from the LLM provider"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available and configured"""
        pass
    
    def update_usage(self, tokens: int, cost: float, success: bool = True):
        """Update usage statistics"""
        self.usage.total_tokens += tokens
        self.usage.total_cost += cost
        self.usage.request_count += 1
        self.usage.last_used = time.strftime("%Y-%m-%d %H:%M:%S")
        
        if not success:
            self.usage.error_count += 1

class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("openai", config)
        self.client = None
        if OPENAI_AVAILABLE:
            api_key = os.getenv(config.get("api_key_env", "OPENAI_API_KEY"))
            if api_key:
                self.client = openai.OpenAI(api_key=api_key)
    
    def is_available(self) -> bool:
        """Check if OpenAI is available and configured"""
        return (OPENAI_AVAILABLE and 
                self.client is not None and 
                os.getenv(self.config.get("api_key_env", "OPENAI_API_KEY")) is not None)
    
    def generate_response(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate response using OpenAI API"""
        start_time = time.time()
        
        if not self.is_available():
            return LLMResponse(
                content="",
                provider=self.provider_name,
                model=self.config.get("model", "gpt-3.5-turbo"),
                tokens_used=0,
                cost=0.0,
                response_time=0.0,
                error="OpenAI provider not available or configured"
            )
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.get("model", "gpt-3.5-turbo"),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", self.config.get("max_tokens", 4000)),
                temperature=kwargs.get("temperature", self.config.get("temperature", 0.1))
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            cost = tokens_used * self.config.get("cost_per_token", 0.0000015)
            response_time = time.time() - start_time
            
            self.update_usage(tokens_used, cost, True)
            
            return LLMResponse(
                content=content,
                provider=self.provider_name,
                model=self.config.get("model"),
                tokens_used=tokens_used,
                cost=cost,
                response_time=response_time,
                raw_response=response.model_dump() if hasattr(response, 'model_dump') else None
            )
            
        except Exception as e:
            error_msg = f"OpenAI API error: {str(e)}"
            logger.error(error_msg)
            self.update_usage(0, 0.0, False)
            
            return LLMResponse(
                content="",
                provider=self.provider_name,
                model=self.config.get("model"),
                tokens_used=0,
                cost=0.0,
                response_time=time.time() - start_time,
                error=error_msg
            )

class MistralProvider(BaseLLMProvider):
    """Mistral AI provider implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("mistral", config)
        self.api_key = os.getenv(config.get("api_key_env", "MISTRAL_API_KEY"))
        self.base_url = "https://api.mistral.ai/v1/chat/completions"
    
    def is_available(self) -> bool:
        """Check if Mistral is available and configured"""
        return (REQUESTS_AVAILABLE and 
                self.api_key is not None)
    
    def generate_response(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate response using Mistral API"""
        start_time = time.time()
        
        if not self.is_available():
            return LLMResponse(
                content="",
                provider=self.provider_name,
                model=self.config.get("model", "mistral-small"),
                tokens_used=0,
                cost=0.0,
                response_time=0.0,
                error="Mistral provider not available or configured"
            )
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.config.get("model", "mistral-small"),
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": kwargs.get("max_tokens", self.config.get("max_tokens", 4000)),
                "temperature": kwargs.get("temperature", self.config.get("temperature", 0.1))
            }
            
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            tokens_used = result.get("usage", {}).get("total_tokens", 0)
            cost = tokens_used * self.config.get("cost_per_token", 0.000002)
            response_time = time.time() - start_time
            
            self.update_usage(tokens_used, cost, True)
            
            return LLMResponse(
                content=content,
                provider=self.provider_name,
                model=self.config.get("model"),
                tokens_used=tokens_used,
                cost=cost,
                response_time=response_time,
                raw_response=result
            )
            
        except Exception as e:
            error_msg = f"Mistral API error: {str(e)}"
            logger.error(error_msg)
            self.update_usage(0, 0.0, False)
            
            return LLMResponse(
                content="",
                provider=self.provider_name,
                model=self.config.get("model"),
                tokens_used=0,
                cost=0.0,
                response_time=time.time() - start_time,
                error=error_msg
            )

class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("ollama", config)
        self.base_url = "http://localhost:11434/api/generate"
        self.available_models = config.get("models", ["llama2:13b"])
    
    def is_available(self) -> bool:
        """Check if Ollama is available locally"""
        if not REQUESTS_AVAILABLE:
            return False
        
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_response(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate response using Ollama local API"""
        start_time = time.time()
        
        if not self.is_available():
            return LLMResponse(
                content="",
                provider=self.provider_name,
                model=self.available_models[0],
                tokens_used=0,
                cost=0.0,
                response_time=0.0,
                error="Ollama not available. Make sure Ollama is running locally."
            )
        
        try:
            model = kwargs.get("model", self.available_models[0])
            data = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", self.config.get("temperature", 0.1))
                }
            }
            
            response = requests.post(self.base_url, json=data, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            content = result.get("response", "")
            
            # Estimate tokens (rough approximation)
            tokens_used = len(prompt.split()) + len(content.split())
            cost = 0.0  # Ollama is free
            response_time = time.time() - start_time
            
            self.update_usage(tokens_used, cost, True)
            
            return LLMResponse(
                content=content,
                provider=self.provider_name,
                model=model,
                tokens_used=tokens_used,
                cost=cost,
                response_time=response_time,
                raw_response=result
            )
            
        except Exception as e:
            error_msg = f"Ollama API error: {str(e)}"
            logger.error(error_msg)
            self.update_usage(0, 0.0, False)
            
            return LLMResponse(
                content="",
                provider=self.provider_name,
                model=self.available_models[0],
                tokens_used=0,
                cost=0.0,
                response_time=time.time() - start_time,
                error=error_msg
            )

class LLMProviderManager:
    """Manager for multiple LLM providers with cost tracking and comparison"""
    
    def __init__(self):
        self.config = Config()
        self.providers = {}
        self.total_budget_used = 0.0
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize all available LLM providers"""
        provider_configs = self.config.LLM_PROVIDERS
        
        # Initialize OpenAI
        if "openai" in provider_configs:
            self.providers["openai"] = OpenAIProvider(provider_configs["openai"])
        
        # Initialize Mistral
        if "mistral" in provider_configs:
            self.providers["mistral"] = MistralProvider(provider_configs["mistral"])
        
        # Initialize Ollama
        if "ollama" in provider_configs:
            self.providers["ollama"] = OllamaProvider(provider_configs["ollama"])
        
        logger.info(f"Initialized {len(self.providers)} LLM providers")
    
    def get_available_providers(self) -> List[str]:
        """Get list of available and configured providers"""
        return [name for name, provider in self.providers.items() if provider.is_available()]
    
    def generate_response(self, prompt: str, provider: str = "openai", **kwargs) -> LLMResponse:
        """Generate response from specified provider"""
        if provider not in self.providers:
            return LLMResponse(
                content="",
                provider=provider,
                model="unknown",
                tokens_used=0,
                cost=0.0,
                response_time=0.0,
                error=f"Provider '{provider}' not available"
            )
        
        # Check budget limits
        provider_config = self.config.LLM_PROVIDERS.get(provider, {})
        budget_limit = provider_config.get("budget_limit", 0.0)
        current_usage = self.providers[provider].usage.total_cost
        
        if budget_limit > 0 and current_usage >= budget_limit:
            return LLMResponse(
                content="",
                provider=provider,
                model=provider_config.get("model", "unknown"),
                tokens_used=0,
                cost=0.0,
                response_time=0.0,
                error=f"Budget limit reached for {provider} (${budget_limit})"
            )
        
        response = self.providers[provider].generate_response(prompt, **kwargs)
        self.total_budget_used += response.cost
        
        return response
    
    def compare_providers(self, prompt: str, providers: Optional[List[str]] = None) -> Dict[str, LLMResponse]:
        """Generate responses from multiple providers for comparison"""
        if providers is None:
            providers = self.get_available_providers()
        
        results = {}
        for provider in providers:
            if provider in self.providers:
                logger.info(f"Generating response with {provider}")
                results[provider] = self.generate_response(prompt, provider)
            else:
                logger.warning(f"Provider {provider} not available")
        
        return results
    
    def get_usage_summary(self) -> Dict[str, Any]:
        """Get usage summary for all providers"""
        summary = {
            "total_budget_used": self.total_budget_used,
            "providers": {}
        }
        
        for name, provider in self.providers.items():
            provider_config = self.config.LLM_PROVIDERS.get(name, {})
            budget_limit = provider_config.get("budget_limit", 0.0)
            
            summary["providers"][name] = {
                "available": provider.is_available(),
                "total_cost": provider.usage.total_cost,
                "budget_limit": budget_limit,
                "budget_remaining": max(0, budget_limit - provider.usage.total_cost),
                "total_tokens": provider.usage.total_tokens,
                "request_count": provider.usage.request_count,
                "error_count": provider.usage.error_count,
                "last_used": provider.usage.last_used
            }
        
        return summary
    
    def reset_usage(self, provider: Optional[str] = None):
        """Reset usage statistics for one or all providers"""
        if provider and provider in self.providers:
            self.providers[provider].usage = ProviderUsage(provider=provider)
        else:
            for provider_obj in self.providers.values():
                provider_obj.usage = ProviderUsage(provider=provider_obj.provider_name)
            self.total_budget_used = 0.0
