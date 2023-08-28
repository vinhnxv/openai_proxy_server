from typing import Optional, List

from pydantic import BaseModel


class ChatCompletionRequest(BaseModel):
    streaming: Optional[bool] = False
    model: Optional[str] = 'gpt-3.5-turbo'
    messages: list


class ChatCompletionUsage(BaseModel):
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class ChatCompletionMessage(BaseModel):
    role: str
    content: str


class ChatCompletionChoice(BaseModel):
    message: Optional[ChatCompletionMessage]
    finish_reason: Optional[str] = None
    index: int = 0


class ChatCompletionDelta(BaseModel):
    content: str


class NormalChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: Optional[ChatCompletionUsage]
    choices: List[ChatCompletionChoice]
