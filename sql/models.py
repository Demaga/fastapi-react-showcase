from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Enum
from sqlalchemy.orm import relationship
from sql.db import Base
import enum


class SubmissionMediaType(enum.Enum):
    text = 1
    image = 2
    video = 3


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


# reddit feed
class Submission(Base):
    __tablename__ = "submission"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(String)
    url = Column(String)
    upvotes = Column(Integer, default=0)
    # rating is calculated right away and stored in a db because it is
    # critical value for this application, and will definitely be
    # calculated on each run, and would require accessing many rows
    # so it makes sense to violate normalization
    rating = Column(Integer, default=0)
    media_type = Column(Enum(SubmissionMediaType), default=1)

    comments = relationship("Comment", back_populates="submission")


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String)
    body = Column(String)
    upvotes = Column(Integer, default=0)
    rating = Column(Integer, default=0)

    parent_id = Column(Integer, ForeignKey("comment.id", ondelete="SET NULL"))
    children = relationship("Comment")

    submission_id = Column(Integer, ForeignKey("submission.id", ondelete="CASCADE"))
    submission = relationship("Submission", back_populates="comments")
