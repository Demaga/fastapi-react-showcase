from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="front/templates")

subapi = FastAPI()


@subapi.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@subapi.get("/who-said-that", response_class=HTMLResponse)
def who_said_that(request: Request):
    return templates.TemplateResponse(
        "who-said-that.html", context={"request": request}
    )


@subapi.get("/reddit-feed", response_class=HTMLResponse)
def who_said_that(request: Request):
    return templates.TemplateResponse("reddit-feed.html", context={"request": request})


@subapi.get("/i-hate-crypto", response_class=HTMLResponse)
def i_hate_crypto(request: Request):
    return templates.TemplateResponse(
        "i-hate-crypto.html", context={"request": request}
    )
