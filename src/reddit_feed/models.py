from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Enum
from sqlalchemy.orm import relationship
from src.db import Base
import enum


class SubmissionMediaType(enum.Enum):
    text = 1
    image = 2
    video = 3


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
    subreddit = Column(String)

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
