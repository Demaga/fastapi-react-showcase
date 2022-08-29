from pydantic import BaseModel
from typing import Optional


class TagBase(BaseModel):
    name: str
    color: str

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str
    born: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        orm_mode = True


class QuoteBase(BaseModel):
    text: str
    author: AuthorBase
    tags: list[TagBase] = []

    class Config:
        orm_mode = True


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int
    quotes: list[QuoteBase] = []


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    quotes: list[QuoteBase] = []


class QuoteCreate(QuoteBase):
    pass


class Quote(QuoteBase):
    id: int
    author_id: int
