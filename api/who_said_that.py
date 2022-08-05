from fastapi import FastAPI, Request

tags_metadata = [
    {
        "name": "who-said-that",
        "description": "Who said that? game api.",
    },
]

subapi = FastAPI()


@subapi.get("/", tags=["who-said-that"])
def read_root(request: Request):
    return {"text": "text"}
