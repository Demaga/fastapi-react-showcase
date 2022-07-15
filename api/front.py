from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="../front")

subapi = FastAPI()

@subapi.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

@subapi.get("/who-said-that", response_class=HTMLResponse)
def read_who_said_that(request: Request):
    return templates.TemplateResponse("who-said-that.html", context={"request": request})
