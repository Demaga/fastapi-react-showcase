from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.reddit_feed import crud
from src.db import get_db


subapi = FastAPI()


@subapi.get("/", tags=["reddit-wrapper"])
async def get_feed(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    submissions = await crud.get_submissions(db, skip, limit)
    for submission in submissions:
        submission.comments = await crud.get_comments(db, submission.id)
    return submissions
