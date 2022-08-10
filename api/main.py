from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import api.front as front
import api.who_said_that as who_said_that
import api.reddit_feed as reddit_feed

app = FastAPI()

app.mount("/static", StaticFiles(directory="front/static"), name="static")

app.mount("/api/who-said-that", who_said_that.subapi)
app.mount("/api/reddit-feed", reddit_feed.subapi)
app.mount("/", front.subapi)
