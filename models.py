from pydantic import BaseModel, Field, field_validator
from typing import List, Annotated

class BlogPost(BaseModel):
    title: str
    tags: List[str]
    content: str

class SummarizerRequest(BaseModel):
    content: str

    @field_validator("content")
    def check_word_count(cls, v):
            print("check word count")
            words = v.strip().split()
            if len(words) < 5:
                raise ValueError("Idea must have at least 5 words.")
            if len(words) > 200:
                raise ValueError("Idea must not exceed 200 words.")
            return v
