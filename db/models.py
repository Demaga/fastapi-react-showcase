from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    color = Column(String, unique=True)

    quotes = relationship("Quote", back_populates="tags")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    born = Column(String)
    bio = Column(String)

    quotes = relationship("Quote", back_populates="author")


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)

    author = relationship("Author", back_populates="quotes")
    tags = relationship("Tag", back_populates="quotes")
