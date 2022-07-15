from fastapi import FastAPI, Request

subapi = FastAPI()

@subapi.get("/")
def read_root(request: Request):
    return {"text": "text"}
