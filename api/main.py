from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import api.front as front
import api.who_said_that as who_said_that
import api.reddit_feed as reddit_feed
import api.redis
import api.i_hate_crypto as i_hate_crypto
from api.settings import settings

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    api.redis.redis_global = await api.redis.init_redis()


@app.on_event("shutdown")
async def shutdown_event():
    api.redis.edis_global.redis.close()
    await api.redis.redis_global.redis.wait_closed()


app.mount("/static", StaticFiles(directory="front/static"), name="static")

app.mount("/api/who-said-that", who_said_that.subapi)
app.mount("/api/reddit-feed", reddit_feed.subapi)
app.mount("/api/i_hate_crypto", i_hate_crypto.subapi)
app.mount("/", front.subapi)
