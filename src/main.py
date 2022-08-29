from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import src.front as front
import src.redis
from src.settings import settings
from src.who_said_that import router as who_said_that
from src.reddit_feed import router as reddit_feed
from src.i_hate_crypto import router as i_hate_crypto


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
    src.redis.redis_global = await src.redis.init_redis()
    print("server started")


@app.on_event("shutdown")
async def shutdown_event():
    src.redis.redis_global.close()
    await src.redis.redis_global.redis.wait_closed()
    print("server shutdown")


app.mount("/static", StaticFiles(directory="front/static"), name="static")

app.mount("/api/who-said-that", who_said_that.subapi)
app.mount("/api/reddit-feed", reddit_feed.subapi)
app.mount("/api/i-hate-crypto", i_hate_crypto.subapi)
app.mount("/", front.subapi)

print("apps mounted")
