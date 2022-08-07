from sqlalchemy.orm import Session
from sql import models, schemas
from sqlalchemy import func

# who said that
def get_quotes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Quote).offset(skip).limit(limit).all()


def get_quote(db: Session, quote_id: int):
    return db.query(models.Quote).where(models.Quote.id == quote_id).first()


def get_random_quote(db: Session):
    return db.query(models.Quote).order_by(func.random()).first()


def get_random_author(db: Session, author_names_to_filter_out=[]):
    return (
        db.query(models.Author)
        .where(~(models.Author.name.in_(author_names_to_filter_out)))
        .first()
    )


def get_author(db: Session, author_id: int):
    return db.query(models.Author).where(models.Author.id == author_id).first()
