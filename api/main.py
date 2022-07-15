from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import front, who_said_that

app = FastAPI()

app.mount("/static", StaticFiles(directory="../static"), name="static")

app.mount("/", front.subapi)
app.mount("/api/who-said-that/", who_said_that.subapi)
