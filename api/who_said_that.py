from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from sql import crud, models, schemas
from sql.db import get_db
import random


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


@subapi.get("/random", tags=["who-said-that"])
def get_random_quotes(db: Session = Depends(get_db)):
    quote = crud.get_random_quote(db)
    author = crud.get_author(db, author_id=quote.author_id).name
    authors = [{"name": author, "real": True}]
    while len(authors) < 3:
        authors_to_filter = [x["name"] for x in authors]
        author = crud.get_random_author(db, authors_to_filter).name
        authors.append({"name": author, "real": False})
    response = {"text": quote.text, "authors": authors}
    return response
