"""
Configuration for Truly Agentic System
"""

import os
from typing import Optional

class Config:
    """Configuration for the agentic system"""

    # LLM Configuration - supports multiple providers
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")  # openai, anthropic, gemini, or mock

    # API Keys (read from environment variables for security)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")

    # Model selection
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest")  # Free tier: 1500 req/day

    # Agent Configuration
    CONFIDENCE_THRESHOLD: float = 0.75  # Minimum confidence before finalizing
    MAX_ITERATIONS: int = 3  # Maximum refinement iterations
    ENABLE_WEB_SEARCH: bool = True  # Enable real web searches

    # Agent Ports (for Fetch.AI uAgents)
    ORCHESTRATOR_PORT: int = 8000
    RESEARCH_AGENT_PORT: int = 8001
    TECH_AGENT_PORT: int = 8002
    COST_AGENT_PORT: int = 8003
    ETHICAL_AGENT_PORT: int = 8004
    MARKET_AGENT_PORT: int = 8005
    VALIDATOR_PORT: int = 8006

    # Timeouts
    AGENT_TIMEOUT: int = 300  # 5 minutes max per agent
    LLM_TIMEOUT: int = 60  # 1 minute max per LLM call

    # Logging
    LOG_LEVEL: str = "INFO"
    VERBOSE_AGENT_REASONING: bool = True  # Show agent thought processes

    @classmethod
    def validate(cls):
        """Validate configuration"""
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            print("⚠️  Warning: OPENAI_API_KEY not set. Using mock LLM.")
            cls.LLM_PROVIDER = "mock"

        if cls.LLM_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            print("⚠️  Warning: ANTHROPIC_API_KEY not set. Using mock LLM.")
            cls.LLM_PROVIDER = "mock"

        if cls.LLM_PROVIDER == "gemini" and not cls.GEMINI_API_KEY:
            print("⚠️  Warning: GEMINI_API_KEY not set. Using mock LLM.")
            cls.LLM_PROVIDER = "mock"

        return cls.LLM_PROVIDER != "mock"


# Validate on import
Config.validate()
