from sqlalchemy.orm import Session
from sql import models, schemas


def get_quotes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Quote).offset(skip).limit(limit).all()
