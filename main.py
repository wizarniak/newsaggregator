from fastapi import FastAPI
import requests
import requests.auth
import config # api credentials stored in config.py
import json
from datetime import datetime
from aggregator import NewsAggregator

app = FastAPI()

MAX_RESULTS = 5 # will get 5 results from each api 
reddit_access_token = None
time_token_generated = None
news_aggregator = NewsAggregator()

@app.get("/")
async def home():
    return {"message": "Go to /news to get news"}

@app.get("/news")
async def get_news(query: str = None):
    if query:
        return news_aggregator.search(query)
    else:
        return news_aggregator.listing()
