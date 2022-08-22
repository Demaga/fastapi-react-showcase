from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import api.front as front
import api.who_said_that as who_said_that
import api.reddit_feed as reddit_feed
import api.redis
import api.i_hate_crypto as i_hate_crypto
from api.settings import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = [
    "http://showcase.chill-party.com",
    "https://showcase.chill-party.com",
    "http://127.0.0.1:8000",
    "https://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    api.redis.redis_global = await api.redis.init_redis()
    print("server started")


@app.on_event("shutdown")
async def shutdown_event():
    api.redis.redis_global.close()
    await api.redis.redis_global.redis.wait_closed()
    print("server shutdown")


app.mount("/static", StaticFiles(directory="front/static"), name="static")

app.mount("/api/who-said-that", who_said_that.subapi)
app.mount("/api/reddit-feed", reddit_feed.subapi)
app.mount("/api/i-hate-crypto", i_hate_crypto.subapi)
app.mount("/", front.subapi)

print("apps mounted")
