from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from sql import crud, models, schemas
from sql.db import SessionLocal, engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


tags_metadata = [
    {
        "name": "who-said-that",
        "description": "Who said that? game api.",
    },
]

subapi = FastAPI()


@subapi.get("/", tags=["who-said-that"], response_model=list[schemas.Quote])
def get_all_quotes(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    quotes = crud.get_quotes(db, skip=skip, limit=limit)
    return quotes
