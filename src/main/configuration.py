import logging
import os

from main.services.fim_infill_service import FimInfillService
from main.services.infill_service import CompletionsInfillService, InfillService
from main.services.mistral.mistral_fim_wrapper import MistralFimWrapper
from main.services.openai.open_ai_manager import AIProviderWrapper, OpenAIChatCompletionsApiWrapper


class Context:
    """Serves as a factory."""

    @classmethod
    def get_infill_service(cls):
        if cls.get_fim_provider() == "MISTRAL":
            return cls.get_fim_infill_service()
        else:
            return cls.get_completions_infill_service()

    @classmethod
    def get_fim_infill_service(cls) -> InfillService:
        return FimInfillService(
                logger=cls.get_logger(),
                ai_provider_wrapper=cls.get_ai_provider())

    @classmethod
    def get_completions_infill_service(cls) -> InfillService:
        return CompletionsInfillService(
                logger=cls.get_logger(),
                model_fim_prompt=cls.get_completions_model_prompt(),
                openai_wrapper=cls.get_ai_provider(),)

    @classmethod
    def get_ai_provider(cls) -> AIProviderWrapper:
        if cls.get_fim_provider() == "MISTRAL":
            return cls.get_mistral_ai_provider()
        else:
            return cls.get_openai_ai_provider()

    @classmethod
    def get_openai_ai_provider(cls) -> AIProviderWrapper:
        return OpenAIChatCompletionsApiWrapper(
                model=cls.get_openai_model(),
                api_key=cls.get_openai_api_key(),
                logger=cls.get_logger(),)

    @classmethod
    def get_mistral_ai_provider(cls) -> AIProviderWrapper:
        return MistralFimWrapper(
                model=cls.get_mistral_model(),
                api_key=cls.get_mistral_api_key(),
                logger=cls.get_logger())

    @classmethod
    def get_fim_provider(cls) -> str:
        return os.environ.get("FIM_PROVIDER", "OPENAI").strip().upper()

    @classmethod
    def get_openai_api_key(cls) -> str:
        return os.environ.get("OPENAI_API_KEY", "")

    @classmethod
    def get_mistral_api_key(cls) -> str:
        return os.environ.get("MISTRAL_API_KEY", "")

    @classmethod
    def get_mistral_model(cls) -> str:
        return "codestral-latest"

    @classmethod
    def get_openai_model(cls) -> str:
        # return "gpt-4.1-nano"
        return "gpt-5-nano"

    @classmethod
    def get_logger(cls):
        logger = logging.getLogger("uvicorn.error")
        logger.setLevel(logging.INFO)
        return logger

    @classmethod
    def get_completions_model_prompt(cls) -> str:
        return """
You are a fill‑in‑the‑middle engine.
You receive text that contains exactly one occurrence of:
<FIM_PRE>…<FIM_SUF>…<FIM_MID>

Interpretation:
    prefix = text between <FIM_PRE> and <FIM_SUF>
    suffix = text between <FIM_SUF> and <FIM_MID>

Task:
    Output exactly the text that should be inserted between prefix and suffix so that prefix + insertion + suffix is a coherent result.
    Output ONLY the insertion text. No explanations, no quotes, no markers, no code fences.
    Do not repeat any text that appears in the prefix or suffix.
    Do not repeat the same phrase or sentence twice.
    Output only the minimal insertion text required.
    If no insertion is needed, return an empty string.

Examples:
    Input:
    <FIM_PRE>the quick brown<FIM_SUF>lazy dog.<FIM_MID>
    Output:
    fox jumps over the 

    Input:
    <FIM_PRE>def calculate_area(radius):\n<FIM_SUF>    return area<FIM_MID>
    Output:
     = pi * radius ** 2 """
