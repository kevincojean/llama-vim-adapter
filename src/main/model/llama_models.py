from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from pydantic import Field


class InputExtra(BaseModel):
    model_config = ConfigDict(extra="ignore")

    filename: Optional[str] = Field(default=None)
    text: Optional[str] = Field(default=None)


class InfillRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    input_prefix: Optional[str] = Field(default=None)
    input_suffix: Optional[str] = Field(default=None)
    input_extra: Optional[List[InputExtra]] = Field(default=None)
    prompt: Optional[str] = Field(default=None)


class InfillResponseTimings(BaseModel):
    """LlamaResponse Timings"""
    model_config = ConfigDict(extra="forbid")

    prompt_n: int = Field(default=-1)
    prompt_ms: float = Field(default=-1)
    prompt_per_token_ms: float = Field(default=-1)
    prompt_per_second: float = Field(default=-1)
    predicted_n: int = Field(default=-1)
    predicted_ms: float = Field(default=-1)
    predicted_per_token_ms: float = Field(default=-1)
    predicted_per_second: float = Field(default=-1)


class InfillResponse(BaseModel):
    """LlamaResponse"""
    model_config = ConfigDict(extra="forbid")

    content: str = Field()
    timings: InfillResponseTimings = Field(default=InfillResponseTimings())
    truncated: bool = Field(default=False)
    tokens_cached: int = Field(default=-1)

