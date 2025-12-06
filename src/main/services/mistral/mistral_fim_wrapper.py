from main.functional.result import Result
from main.services.openai.open_ai_manager import BaseAIProviderWrapper
from mistralai import Mistral
from mistralai import models
from typing import Any, Optional, Union
import logging


class MistralFimWrapper(BaseAIProviderWrapper):
    """Wraps Mistral's /v1/fim/completions endpoint."""

    MISTRAL_FIM_COMPLETIONS_ENDPOINT = "https://api.mistral.ai/v1/fim/completions"

    def __init__(
        self,
        model: str,
        api_key: str,
        logger: logging.Logger,
        *,
        timeout: int = 5,
        max_tokens: int = 1500,
        top_p: Optional[float] = None,
        min_tokens: Optional[int] = None,
        temperature: Optional[float] = 0.2,
        stop: Optional[Union[list[str], str]] = None,
    ) -> None:
        super().__init__(model=model, api_key=api_key, logger=logger)
        self.max_tokens = max_tokens
        self.min_tokens = min_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.stop = stop
        self.timeout_seconds: int =  timeout

    def query(self, prompt: str, suffix: Optional[str] = None, instructions: Optional[str] = None) -> Result[models.FIMCompletionResponse, Exception]:
        api_key = self.api_key.strip()
        if not api_key:
            return Result.failure(ValueError("MISTRAL_API_KEY cannot be empty"))
        
        with Mistral(api_key=api_key) as mistral:
            self.logger.debug(f"prompt: {prompt}")
            self.logger.debug(f"suffix: {suffix}")
            return Result.lift(lambda: \
                    mistral.fim.complete( \
                        model=self.model,
                        prompt=prompt,
                        suffix=suffix,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        stop=self.stop,
                        timeout_ms=self.timeout_seconds * 1000,
                        top_p=self.top_p,
                        stream=False))\
                    .peek(lambda resp: self.logger.debug(f"Mistral FIM response: {resp}"))

    def extract(self, resp: models.FIMCompletionResponse) -> Result[str, Exception]:
        return Result.lift(lambda: resp.choices[0].message.content)  # pyright: ignore[reportReturnType]

