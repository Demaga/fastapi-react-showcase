from fastapi import FastAPI, Request, Depends
import praw
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    username=USERNAME,
    password=PASSWORD,
)

subapi = FastAPI()


@subapi.get("/", tags=["reddit-wrapper"])
def get_all_quotes(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    quotes = crud.get_quotes(db, skip=skip, limit=limit)
    return quotes


@subapi.get("/random", tags=["reddit-wrapper"])
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
