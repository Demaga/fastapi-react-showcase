from fastapi import FastAPI, Request
import api.redis
from api.settings import settings
from datetime import timedelta, datetime
import httpx

subapi = FastAPI()


async def fetch_data(client):
    url = "https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    params = {"start": "1", "limit": "50", "convert": "USD"}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c",
    }
    response = await client.get(url, params=params, headers=headers)
    return response.json()


@subapi.get("/")
async def get_coinmarketcap():
    redis = api.redis.redis_global
    data = await redis.get("coinmarketcap")
    if data == None:
        async with httpx.AsyncClient() as client:
            response = await fetch_data(client)
            print(response)
    elif timedelta(data["last_fetched"]) - timedelta(datetime.now()) > timedelta(
        hours=1
    ):
        async with httpx.AsyncClient() as client:
            response = await fetch_data(client)
            print(response)
    else:
        return data
