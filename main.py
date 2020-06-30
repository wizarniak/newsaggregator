from fastapi import FastAPI
import requests
import requests.auth
import config
import json

app = FastAPI()

MAX_RESULTS = 5
reddit_access_token = None

@app.get("/")
async def home():
    return {"message": "Go to /news to get news"}

@app.get("/news")
async def get_news(query: str = None):
    global reddit_access_token
    print(reddit_access_token)
    if (not reddit_access_token):
        reddit_access_token = get_reddit_access_token()
    if query:
        reddit_news = search_reddit_news(reddit_access_token, query)
        newsapi_news = search_newsapi_news(query)
    else:
        reddit_news = get_reddit_news(reddit_access_token)
        newsapi_news = get_newsapi_news()
    return reddit_news + newsapi_news

def get_reddit_access_token():
    url = "https://www.reddit.com/api/v1/access_token"
    post_data = {"grant_type":"client_credentials"}
    response = requests.post(url, data=post_data, auth=(config.reddit_client_id, config.reddit_client_secret),
    headers={"User-Agent":config.reddit_user_agent})
    return json.loads(response.content)["access_token"]

def get_reddit_news(access_token):
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

def search_reddit_news(access_token, query):
    url = "https://oauth.reddit.com/r/worldnews/search"
    params = {"limit": MAX_RESULTS, "q": query, "restrict_sr": True}
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

def get_newsapi_news():
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

def search_newsapi_news(query):
    url = "https://newsapi.org/v2/everything"
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
