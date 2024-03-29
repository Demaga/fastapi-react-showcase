from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Enum
from sqlalchemy.orm import relationship
from src.db import Base


# who said that
class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    color = Column(String, unique=True)

    quotes = relationship("Quote", secondary="quote_tag", back_populates="tags")

    def __repr__(self):
        return repr(self.name)


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    born = Column(String)
    bio = Column(String)

    quotes = relationship("Quote", back_populates="author")


class Quote(Base):
    __tablename__ = "quote"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    author_id = Column(Integer, ForeignKey("author.id", ondelete="CASCADE"))

    author = relationship("Author", back_populates="quotes")
    tags = relationship("Tag", secondary="quote_tag", back_populates="quotes")

    def __repr__(self):
        return repr("author: " + self.author.name + "; tags: " + str(self.tags))


quote_tag = Table(
    "quote_tag",
    Base.metadata,
    Column("quote_id", Integer, ForeignKey("quote.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="CASCADE")),
)
