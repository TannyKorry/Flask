from typing import Optional, Type

from pydantic import BaseModel, validator


class CreateAds(BaseModel):
    title: str
    text: str

    @validator("title")
    def secure_title(cls, value):
        if len(value) < 1 or len(value) > 50:
            raise ValueError("Title should be from 1 to 50 characters")
        return value

    @validator("text")
    def secure_text(cls, value):
        if len(value) > 250:
            raise ValueError("Text is too large (max 250 characters are allowed)")
        return value
