from sqlalchemy.orm import Session
from src.reddit_feed import models
from sqlalchemy import func


async def get_submissions(db: Session, skip: int = 0, limit: int = 10):
    length = db.query(func.count(models.Submission.id)).scalar()
    if skip >= length:
        return []
    return (
        db.query(models.Submission)
        .order_by(models.Submission.rating.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


async def get_comments(db: Session, submission_id: int):
    return (
        db.query(models.Comment)
        .where(models.Comment.submission_id == submission_id)
        .order_by(models.Comment.rating.desc())
        .limit(20)
        .all()
    )
