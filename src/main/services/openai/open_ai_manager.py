import abc
from logging import Logger
from typing import Optional, Union

from main.functional.result import Result
import openai
from openai.types import Completion
from openai.types.chat import ChatCompletion
from openai.types.responses import Response
from openai.types.shared_params.reasoning import Reasoning


class AIProviderWrapper(abc.ABC):

    @abc.abstractmethod
    def get_api_key(self) -> str:
        ...

    @abc.abstractmethod
    def get_model(self) -> str:
        ...

    @abc.abstractmethod
    def query(self, prompt: str, instructions: str, suffix: Optional[str] = None) -> Result[Union[Response, ChatCompletion, Completion], Exception]:
        ...

    @abc.abstractmethod
    def extract(self, response: Union[Response, ChatCompletion, Completion]) -> Result[str, Exception]:
        ...


class BaseAIProviderWrapper(AIProviderWrapper, abc.ABC):

    def __init__(self, model: str, api_key: str, logger: Logger):
        self.logger = logger
        self.model = model
        self.api_key = api_key

    def get_api_key(self):
        return self.api_key

    def get_model(self):
        return self.model


class OpenAIResponsesApiWrapper(BaseAIProviderWrapper):
    """For gpt-5 and o1 series of models"""

    def __init__(self, model: str, api_key: str, logger: Logger):
        super().__init__(model, api_key, logger)

    def query(self, prompt: str, instructions: str, suffix: Optional[str] = None):
        return Result.lift(lambda: openai.responses.create(
                    model=self.model,
                    instructions=instructions,
                    store=False,
                    input=prompt,
                    max_output_tokens=1500,
                    reasoning=Reasoning({'effort': 'minimal'}),
                    truncation="auto"))\
                .peek(lambda _: self.logger.debug(f"Response: {str(_)}"))\
                .flat_map(lambda resp: Result.of(resp)\
                                    if not resp.incomplete_details \
                                    else Result.of_error(
                                        Exception(f"The response was not completed successfully: {resp.incomplete_details}")))

    def extract(self, response: Response):
        return Result.lift(lambda: response.output_text)


class OpenAIChatCompletionsApiWrapper(BaseAIProviderWrapper):

    def __init__(self, model: str, api_key: str, logger: Logger):
        super().__init__(model, api_key, logger)

    def query(self, prompt: str, instructions: str, suffix: Optional[str] = None) -> Result[ChatCompletion, Exception]:
        return Result.lift(lambda: openai.chat.completions.create(
                messages=[
                    { "role": "developer", "content": instructions },
                    { "role": "user", "content": prompt }
                ],
                model=self.model,
                max_completion_tokens=1500,
                n=1,
                reasoning_effort="minimal",
                timeout=3.0))\
            .peek(lambda _: self.logger.debug(f"Chat Completion response: {str(_)}"))

    def extract(self, completion: ChatCompletion) -> Result[str, Exception]:
        return Result.lift(lambda: completion.choices[0])\
                .flat_map(lambda c: Result.of(c) \
                                        if c.finish_reason != "content_filter" \
                                        else Result.of_error(Exception(f"Completion did not finish properly: {c.finish_reason}\n {c}")))\
                .map(lambda c: c.message.content or "")

