from fastapi import FastAPI, Request, Depends
from sql.db import SessionLocal
from sqlalchemy.orm import Session
from sql import crud


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


subapi = FastAPI()


@subapi.get("/", tags=["reddit-wrapper"])
async def get_feed(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    submissions = await crud.get_submissions(db, skip, limit)
    for submission in submissions:
        submission.comments = await crud.get_comments(db, submission.id)
    return submissions
