from fastapi import FastAPI
import requests
import requests.auth
import config # api credentials stored in config.py
import json
from datetime import datetime
import functools

app = FastAPI()

MAX_RESULTS = 5 # will get 5 results from each api 
reddit_access_token = None
time_token_generated = None
SIZE_LRU_CACHES = 128 # this speeds up repeat requests, yet to experiment with the right number

@app.get("/")
async def home():
    return {"message": "Go to /news to get news"}

@app.get("/news")
async def get_news(query: str = None):
    global reddit_access_token, time_token_generated
    # if access token doesn't exist yet or is about to expire, generate new (reddit tokens expire after 60 minutes)
    if (not reddit_access_token or (datetime.now() - time_token_generated).total_seconds() / 60 > 55):
        reddit_access_token = get_reddit_access_token()
        time_token_generated = datetime.now()
    if query:
        reddit_news = search_reddit_news(reddit_access_token, query)
        newsapi_news = search_newsapi_news(query)
    else:
        reddit_news = get_reddit_news(reddit_access_token)
        newsapi_news = get_newsapi_news()
    return reddit_news + newsapi_news

def get_reddit_access_token():
    '''
    get temporary token which is required for sending requests to the reddit api
    '''
    url = "https://www.reddit.com/api/v1/access_token"
    post_data = {"grant_type":"client_credentials"}
    response = requests.post(url, data=post_data, auth=(config.reddit_client_id, config.reddit_client_secret),
    headers={"User-Agent":config.reddit_user_agent})
    return json.loads(response.content)["access_token"]

@functools.lru_cache(maxsize=SIZE_LRU_CACHES)
def get_reddit_news(access_token):
    '''
    get the hottest news from /r/worldnews 
    '''
    url = "https://oauth.reddit.com/r/worldnews/hot"
    params = {"limit": MAX_RESULTS}
    response = requests.get(url,
    headers={"Authorization": "bearer " + access_token, "User-Agent":config.reddit_user_agent},
    params = params)
    news = []
    for item in json.loads(response.content)["data"]["children"]:
        news_item = {"headline": item["data"]["title"], 
        "link": item["data"]["url"],
        "source": "reddit"}
        news.append(news_item)
    return news

@functools.lru_cache(maxsize=SIZE_LRU_CACHES)
def search_reddit_news(access_token, query):
    '''
    search /r/worldnews for the query term
    '''
    url = "https://oauth.reddit.com/r/worldnews/search"
    params = {"limit": MAX_RESULTS, "q": query, "restrict_sr": True} # restrict_sr restricts search results to /r/worldnews
    response = requests.get(url,
    headers={"Authorization": "bearer " + access_token, "User-Agent":config.reddit_user_agent},
    params = params)
    news = []
    for item in json.loads(response.content)["data"]["children"]:
        news_item = {"headline": item["data"]["title"], 
        "link": item["data"]["url"],
        "source": "reddit"}
        news.append(news_item)
    return news

@functools.lru_cache(maxsize=SIZE_LRU_CACHES)
def get_newsapi_news():
    '''
    get top headlines from newsapi's general category
    '''
    url = "https://newsapi.org/v2/top-headlines"
    params = {"category": "general", "pageSize": MAX_RESULTS}
    response = requests.get(url,
    headers={"Authorization": "bearer " + config.news_api_key},
    params = params)
    news = []
    for item in json.loads(response.content)["articles"]:
        news_item = {"headline": item["title"],
        "link": item["url"],
        "source": "newsapi"}
        news.append(news_item)
    return news

@functools.lru_cache(maxsize=SIZE_LRU_CACHES)
def search_newsapi_news(query):
    '''
    search "everything" on newsapi for most relevant results in english for the query term
    '''
    url = "https://newsapi.org/v2/everything" # everything endpoint gets better search results than top-headlines
    params = {"pageSize": MAX_RESULTS, "q": query, "language": "en", "sortBy": "relevancy"}
    response = requests.get(url,
    headers={"Authorization": "bearer " + config.news_api_key},
    params = params)
    news = []
    for item in json.loads(response.content)["articles"]:
        news_item = {"headline": item["title"],
        "link": item["url"],
        "source": "newsapi"}
        news.append(news_item)
    return news
