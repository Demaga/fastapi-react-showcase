# this script runs daily, parses top reddit posts
import praw
from dotenv import load_dotenv, find_dotenv
import os
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sql.models import Submission, Comment, SubmissionMediaType

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
    user_agent="showcase",
)

subreddits = (
    "EverythingScience",
    "Art",
    "DataIsBeautiful",
    "Funny",
    "TodayILearned",
    "DunderMifflin",
    "HistoryMemes",
    "PCMasterRace",
    "AskScience",
    "Buildapc",
)


DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}:5432/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print(SessionLocal)


with SessionLocal() as session:
    session.query(Submission).delete()
    session.query(Comment).delete()
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).top(time_filter="day", limit=10):
            submission = reddit.submission(submission)
            title = submission.title
            text = submission.selftext
            url = submission.url
            upvotes = submission.score
            comments = submission.comments
            rating = upvotes

            if submission.media != None:
                if "reddit_media" in submission.media:
                    url = submission.media["reddit_media"]["fallback_url"]
                elif "reddit_video" in submission.media:
                    url = submission.media["reddit_video"]["fallback_url"]
                else:
                    continue
                media_type = SubmissionMediaType.video
            else:
                if "i.redd.it" in submission.url:
                    media_type = SubmissionMediaType.image
                else:
                    media_type = SubmissionMediaType.text

            submission_to_upload = Submission(
                title=title,
                text=text,
                url=url,
                upvotes=upvotes,
                media_type=media_type,
            )

            while True:
                try:
                    submission.comments.replace_more()
                    break
                except Exception as e:
                    print(e)
                sleep(1)

            for comment in comments.list():
                author = comment.author
                if author == None:
                    author = "deleted"
                else:
                    author = author.name
                body = comment.body_html
                comment_upvotes = comment.score
                comment_rating = comment_upvotes

                comment_to_upload = Comment(
                    author=author,
                    body=body,
                    upvotes=comment_upvotes,
                    submission=submission_to_upload,
                )

                comment_children = []

                replies = comment.replies

                while True:
                    try:
                        replies.replace_more()
                        break
                    except Exception as e:
                        print(e)
                    sleep(1)

                for reply in replies:
                    author = reply.author
                    if author == None:
                        author = "deleted"
                    else:
                        author = author.name
                    reply_body = reply.body_html
                    reply_upvotes = reply.score
                    reply_rating = upvotes

                    reply_to_upload = Comment(
                        author=author,
                        body=reply_body,
                        upvotes=reply_upvotes,
                        rating=reply_rating,
                    )
                    session.add(reply_to_upload)

                    comment_children.append(reply_to_upload)
                    comment_rating += upvotes

                comment_to_upload.children = comment_children
                comment_to_upload.rating = comment_rating
                session.add(comment_to_upload)

                rating += comment_rating

            submission_to_upload.rating = rating
            session.add(submission_to_upload)

    session.commit()
