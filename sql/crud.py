from sqlalchemy.orm import Session
from sql import models, schemas
from sqlalchemy import func

# who said that
def get_quotes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Quote).offset(skip).limit(limit).all()


def get_quote(db: Session, quote_id: int):
    return db.query(models.Quote).where(models.Quote.id == quote_id).first()


def create_quote(db: Session, text: str, author: models.Author):
    quote_obj = models.Quote(text=text, author=author)
    db.add(quote_obj)
    db.commit()
    return quote_obj


def get_random_quote(db: Session):
    return db.query(models.Quote).order_by(func.random()).first()


def get_random_author(db: Session, author_names_to_filter_out=[]):
    return (
        db.query(models.Author)
        .where(~(models.Author.name.in_(author_names_to_filter_out)))
        .first()
    )


def create_author(db: Session, name: str):
    author = models.Author(name=name)
    db.add(author)
    db.commit()
    return author


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(models.Author).where(models.Author.id == author_id).first()


def get_author_by_name(db: Session, name: str):
    return db.query(models.Author).where(models.Author.name == name).first()


# reddit feed
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
