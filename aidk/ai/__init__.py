"""AI runtime primitives for AIDK."""

from aidk.ai.config import (
    AIConfigurationError,
    AISettings,
    load_ai_settings,
)
from aidk.ai.factory import (
    UnknownAIProviderError,
    build_llm_provider,
)
from aidk.ai.runtime import (
    AIRuntime,
    build_ai_runtime,
)
from aidk.ai.engine import (
    AssistantAnswer,
    AssistantEngine,
)
from aidk.ai.providers import (
    HTTPResponse,
    HTTPTransport,
    LLMConnectionError,
    LLMProvider,
    LLMProviderError,
    LLMRequest,
    LLMResponse,
    LLMResponseError,
    LLMTimeoutError,
    LocalRuleProvider,
    OllamaConfig,
    OllamaProvider,
    UrllibHTTPTransport,
)
from aidk.ai.retrieval import (
    CodeContextRetriever,
    GraphContextRetriever,
    ProjectMetadataRetriever,
    RetrievedContext,
    RetrievalPipeline,
)

__all__ = [
    "AIRuntime",
    "build_ai_runtime",
    "AIConfigurationError",
    "AISettings",
    "UnknownAIProviderError",
    "build_llm_provider",
    "load_ai_settings",
    "AssistantAnswer",
    "AssistantEngine",
    "CodeContextRetriever",
    "GraphContextRetriever",
    "HTTPResponse",
    "HTTPTransport",
    "LLMConnectionError",
    "LLMProvider",
    "LLMProviderError",
    "LLMRequest",
    "LLMResponse",
    "LLMResponseError",
    "LLMTimeoutError",
    "LocalRuleProvider",
    "OllamaConfig",
    "OllamaProvider",
    "ProjectMetadataRetriever",
    "RetrievedContext",
    "RetrievalPipeline",
    "UrllibHTTPTransport",
]
