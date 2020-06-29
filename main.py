from fastapi import FastAPI
import requests
import requests.auth
import config
import json

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Go to /news to get news"}

@app.get("/news")
async def get_news(query: str = None):
    reddit_access_token = get_reddit_access_token()
    print(reddit_access_token)
    if query:
        return {"message": "News search"}
    else:
        reddit_news = get_reddit_news(reddit_access_token)
        return reddit_news

def get_reddit_access_token():
    url = "https://www.reddit.com/api/v1/access_token"
    post_data = {"grant_type":"client_credentials"}
    response = requests.post(url, data=post_data, auth=(config.reddit_client_id, config.reddit_client_secret),
    headers={"User-Agent":config.reddit_user_agent})
    return json.loads(response.content)["access_token"]

def get_reddit_news(access_token):
    url = "https://oauth.reddit.com/r/worldnews/hot?limit=5"
    response = requests.get(url,
    headers={"Authorization": "bearer " + access_token, "User-Agent":config.reddit_user_agent})
    return response.content