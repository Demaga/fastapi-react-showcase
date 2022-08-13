from fastapi import FastAPI, Request
import api.redis
from api.settings import settings
from datetime import timedelta, datetime, timezone
import httpx
from redis.commands.json.path import Path
import json
import pytz


subapi = FastAPI()


async def fetch_data(client):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    params = {"start": "1", "limit": "50", "convert": "USD"}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": settings.COINMARKETCAP_API_KEY,
    }
    response = await client.get(url, params=params, headers=headers)
    return response.json()


@subapi.get("/")
async def get_coinmarketcap():
    redis = api.redis.redis_global

    try:
        data_str = await redis.get("coinmarketcap")
        data = json.loads(data_str)
    except Exception as e:
        print(e)
        data = None

    if data == None:
        async with httpx.AsyncClient() as client:
            data = await fetch_data(client)
            data_str = json.dumps(data)
            await redis.set("coinmarketcap", data_str)
    elif datetime.now().astimezone(timezone.utc) - datetime.strptime(
        data["status"]["timestamp"].split(".")[0], "%Y-%m-%dT%H:%M:%S"
    ).replace(tzinfo=timezone.utc) > timedelta(hours=1):
        async with httpx.AsyncClient() as client:
            data = await fetch_data(client)
            data_str = json.dumps(data)
            await redis.set("coinmarketcap", data_str)
    return data
