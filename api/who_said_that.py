from fastapi import FastAPI, Request
from sqlalchemy.orm import Session
from sql import models, schemas

tags_metadata = [
    {
        "name": "who-said-that",
        "description": "Who said that? game api.",
    },
]

subapi = FastAPI()


@subapi.get("/", tags=["who-said-that"])
def get_all_quotes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Quote).offset(skip).limit(limit).all()
