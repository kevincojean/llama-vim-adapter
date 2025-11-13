import abc
import logging
import re
import string

from main.functional.result import Result
from main.model.llama_models import InfillRequest
from main.services.openai.open_ai_manager import AIProviderWrapper

class InfillService(abc.ABC):

    @abc.abstractmethod
    def process(self, request: InfillRequest) -> Result[str, Exception]:
        ...


class CompletionsInfillService(InfillService):

    def __init__(self,
                 openai_wrapper: AIProviderWrapper,
                 logger: logging.Logger,
                 model_fim_prompt: str) -> None:
        self.logger = logger
        self.model_fim_prompt = model_fim_prompt
        self.openai_wrapper = openai_wrapper

    def process(self, request: InfillRequest) -> Result[str, Exception]:
        prefix = request.input_prefix or ""
        suffix = request.input_suffix or ""
        return Result.lift(lambda: self._make_fim_prompt(request))\
                .flat_map(lambda p: self.openai_wrapper.query(prompt=p, instructions=self.model_fim_prompt))\
                .flat_map(lambda r: self.openai_wrapper.extract(r))\
                .map(lambda t: t.strip())\
                .map(lambda t: self._trim_overlap_with_prefix_words(prefix.strip(), t.strip()))\
                .map(lambda t: self._trim_overlap_with_suffix(suffix.strip(), t.strip()))

    def _trim_overlap_with_prefix_words(self, prefix: str, insertion: str) -> str:
        max_overlap = min(len(prefix), len(insertion))
        for k in range(max_overlap, 0, -1):
            if insertion.startswith(prefix[:k]):
                if re.match(r'\W', insertion[k:k+1] or ' '):
                    return insertion[k:].lstrip(string.whitespace + string.punctuation)
        return insertion

    def _trim_overlap_with_suffix(self ,suffix: str, insertion: str) -> str:
        max_overlap = min(len(insertion), len(suffix))
        for k in range(max_overlap, 0, -1):
            if insertion.endswith(suffix[:k]):
                return insertion[:-k]
        return insertion

    def _make_fim_prompt(self, request: InfillRequest) -> str:
        FIM_PRE = "<FIM_PRE>"
        FIM_SUF = "<FIM_SUF>"
        FIM_MID = "<FIM_MID>"
        extra_parts = []
        if request.input_extra:
            for item in request.input_extra:
                extra_parts.append(item.text)
        extra_text = "\n".join(extra_parts) if extra_parts else ""
        parts = []
        if extra_text:
            parts.append(extra_text)
        parts.append(FIM_PRE)
        parts.append(request.input_prefix or "")
        parts.append(FIM_SUF)
        parts.append(request.input_suffix or "")
        parts.append(FIM_MID)
        parts.append(request.prompt or "")
        combined = "".join(parts)
        return combined

