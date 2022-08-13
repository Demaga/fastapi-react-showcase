from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from sql import crud, models, schemas
from sql.db import get_db


subapi = FastAPI()


@subapi.get("/", tags=["reddit-wrapper"])
async def get_feed(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    submissions = await crud.get_submissions(db, skip, limit)
    for submission in submissions:
        submission.comments = await crud.get_comments(db, submission.id)
    return submissions
