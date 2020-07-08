from datetime import datetime
import requests
import json

class RedditNews:
    def __init__(self, client_id, client_secret, user_agent, max_results=5):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.max_results = max_results
        self.access_token = None
        self.time_token_generated = None

    def get_access_token(self):
        '''
        get temporary token which is required for sending requests to the reddit api
        '''
        url = "https://www.reddit.com/api/v1/access_token"
        post_data = {"grant_type":"client_credentials"}
        response = requests.post(url, data=post_data, auth=(self.client_id, self.client_secret),
        headers={"User-Agent":self.user_agent})
        return json.loads(response.content)["access_token"]

    def authenticate(self):
        if (not self.access_token or (datetime.now() - self.time_token_generated).total_seconds() / 60 > 55):
            self.access_token = self.get_access_token()
            self.time_token_generated = datetime.now()

    def listing(self):
        '''
        get the hottest news from /r/worldnews 
        '''
        self.authenticate()
        url = "https://oauth.reddit.com/r/worldnews/hot"
        params = {"limit": self.max_results}
        response = requests.get(url,
        headers={"Authorization": "bearer " + self.access_token, "User-Agent":self.user_agent},
        params = params)
        news = []
        for item in json.loads(response.content)["data"]["children"]:
            news_item = {"headline": item["data"]["title"], 
            "link": item["data"]["url"],
            "source": "reddit"}
            news.append(news_item)
        return news

    def search(self, query):
        '''
        search /r/worldnews for the query term
        '''
        self.authenticate()
        url = "https://oauth.reddit.com/r/worldnews/search"
        params = {"limit": self.max_results, "q": query, "restrict_sr": True} # restrict_sr restricts search results to /r/worldnews
        response = requests.get(url,
        headers={"Authorization": "bearer " + self.access_token, "User-Agent":self.user_agent},
        params = params)
        news = []
        for item in json.loads(response.content)["data"]["children"]:
            news_item = {"headline": item["data"]["title"], 
            "link": item["data"]["url"],
            "source": "reddit"}
            news.append(news_item)
        return news