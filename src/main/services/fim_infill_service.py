
import logging
from main.functional.result import Result
from main.model.llama_models import InfillRequest
from main.services.infill_service import InfillService
from main.services.openai.open_ai_manager import AIProviderWrapper


class FimInfillService(InfillService):
    """
    This class is used to process the infill request and return the completion.
    """

    def __init__(self,
                 ai_provider_wrapper: AIProviderWrapper,
                 logger: logging.Logger) -> None:
        self.logger = logger
        self.ai_provider_wrapper = ai_provider_wrapper

    def process(self, request: InfillRequest) -> Result[str, Exception]:
        self.logger.debug(f"Request: {request}")
        prompt_parts = [str(e.text) for e in request.input_extra or [] if e.text]
        if request.input_prefix:
            prompt_parts.append(request.input_prefix)
        if request.prompt:
            prompt_parts.append(request.prompt)
        prompt = "\n".join(prompt_parts).strip()
        suffix = request.input_suffix or ""
        suffix = suffix.strip()
        return self.ai_provider_wrapper.query(
                prompt=prompt,
                suffix=suffix,
                instructions="")\
            .flat_map(lambda resp: self.ai_provider_wrapper.extract(resp))\
            .map(lambda t: t.strip())\
            .peek(lambda compl: self.logger.debug(f"Fim prompt: {prompt}"))\
            .peek(lambda compl: self.logger.debug(f"Fim suffix: {suffix}"))\
            .peek(lambda compl: self.logger.debug(f"Fim Completion: {compl}"))

