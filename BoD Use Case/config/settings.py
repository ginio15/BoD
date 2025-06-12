"""
Configuration settings for BoD Presentation Analysis System
"""

import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """Configuration class for the application"""
    
    # Application settings
    APP_NAME = "BoD Presentation Analyzer"
    VERSION = "0.1.0"
    
    # File paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    UPLOADS_DIR = DATA_DIR / "uploads"
    PROCESSED_DIR = DATA_DIR / "processed"
    OUTPUTS_DIR = DATA_DIR / "outputs"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Ensure directories exist
    for directory in [DATA_DIR, UPLOADS_DIR, PROCESSED_DIR, OUTPUTS_DIR, LOGS_DIR]:
        directory.mkdir(exist_ok=True)
    
    # LLM Provider configurations
    LLM_PROVIDERS = {
        "mistral": {
            "api_key_env": "MISTRAL_API_KEY",
            "model": "mistral-small",
            "max_tokens": 4000,
            "temperature": 0.1,
            "budget_limit": 5.00,
            "cost_per_token": 0.000002  # Estimated
        },
        "openai": {
            "api_key_env": "OPENAI_API_KEY", 
            "model": "gpt-3.5-turbo",
            "max_tokens": 4000,
            "temperature": 0.1,
            "budget_limit": 10.00,
            "cost_per_token": 0.0000015  # $0.0015 per 1K tokens
        },
        "ollama": {
            "models": ["llama3.2:3b", "llama2:13b", "mixtral:8x7b"],
            "max_tokens": 4000,
            "temperature": 0.1,
            "budget_limit": 0.00,  # Free
            "cost_per_token": 0.0
        }
    }
    
    # OCR settings
    OCR_CONFIG = {
        "tesseract_path": None,  # Auto-detect
        "languages": ["eng"],
        "config": "--oem 3 --psm 6",  # OCR Engine Mode 3, Page Segmentation Mode 6
        "presentation_config": "--oem 3 --psm 1 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz%.,:()/- ",  # Optimized for presentations
        "min_confidence": 30,
        "preprocessing": {
            "enhance_contrast": 1.8,  # Higher contrast for screenshots
            "min_resize_width": 1200,  # Larger for better OCR
            "min_resize_height": 800,
            "noise_reduction": True
        }
    }
    
    # Document processing settings
    DOCUMENT_CONFIG = {
        "max_file_size_mb": 50,
        "supported_formats": [".pdf", ".pptx", ".txt"],
        "text_density_threshold": 0.1,  # For OCR decision
        "min_text_length": 10
    }
    
    # Analysis settings
    ANALYSIS_CONFIG = {
        "confidence_threshold": 0.7,
        "max_context_length": 8000,  # For LLM processing
        "commitment_patterns": [
            r"(?:will|committed to|plan to|target|goal)\s+(.{10,100}?)\s+(?:by|in|before)\s+(\w+\s+\d{4}|\d{1,2}/\d{4})",
            r"(\d{1,3}%)\s+(?:completion|target|goal)",
            r"reduce|increase|improve\s+(.{10,50}?)\s+(?:by|to)\s+(\d{1,3}%|\d+)"
        ],
        "confidence_indicators": {
            "high": ["will", "committed", "ensure", "guarantee", "definitely", "certainly"],
            "medium": ["plan to", "aim to", "target", "expect", "intend", "propose"],
            "low": ["hope to", "considering", "exploring", "may", "might", "potentially"]
        }
    }
    
    # Budget and cost tracking
    BUDGET_CONFIG = {
        "total_budget": 20.00,  # $20 for POC
        "warning_threshold": 0.8,  # 80% of budget
        "provider_budgets": {
            "mistral": 5.00,
            "openai": 10.00,
            "ollama": 0.00
        }
    }
    
    # Logging configuration
    LOGGING_CONFIG = {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file_max_bytes": 10 * 1024 * 1024,  # 10MB
        "file_backup_count": 5
    }
    
    @classmethod
    def get_api_key(cls, provider: str) -> str:
        """Get API key for the specified provider"""
        if provider not in cls.LLM_PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}")
        
        key_env = cls.LLM_PROVIDERS[provider].get("api_key_env")
        if not key_env:
            return None  # For local providers like Ollama
        
        api_key = os.getenv(key_env)
        if not api_key and provider != "ollama":
            raise ValueError(f"API key not found for {provider}. Set {key_env} environment variable.")
        
        return api_key
    
    @classmethod
    def get_provider_config(cls, provider: str) -> Dict[str, Any]:
        """Get configuration for the specified provider"""
        if provider not in cls.LLM_PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}")
        
        return cls.LLM_PROVIDERS[provider].copy()
    
    @classmethod
    def validate_environment(cls) -> Dict[str, bool]:
        """Validate that all required environment variables and dependencies are available"""
        validation_results = {}
        
        # Check API keys
        for provider, config in cls.LLM_PROVIDERS.items():
            if provider == "ollama":
                validation_results[f"{provider}_available"] = True  # Will check in runtime
            else:
                key_env = config.get("api_key_env")
                validation_results[f"{provider}_api_key"] = bool(os.getenv(key_env))
        
        # Check directories
        for dir_name, dir_path in [
            ("data", cls.DATA_DIR),
            ("uploads", cls.UPLOADS_DIR),
            ("processed", cls.PROCESSED_DIR),
            ("outputs", cls.OUTPUTS_DIR),
            ("logs", cls.LOGS_DIR)
        ]:
            validation_results[f"{dir_name}_dir"] = dir_path.exists()
        
        return validation_results
