from dataclasses import dataclass
from datetime import datetime

@dataclass
class ParsedMessage:
    timestamp: datetime | None
    sender: str
    message: str
    message_id: int = 0

@dataclass
class StyleProfile:
    average_message_length: float
    formality: str
    uses_slang: bool
    uses_emojis: bool
    common_emojis: list[str]
    common_phrases: list[str]
    typical_response_length: str
    capitalization: str
    punctuation: dict[str, int]
    question_frequency: float
    abbreviations: list[str]
    repeated_expressions: list[str]

    def as_dict(self):
        return self.__dict__
