# newsaggregator

Instructions to run with your own credentials:

1) clone repository

2) create a web app on reddit.com/prefs/apps and note down credentials

3) get an API key from NewsAPI

4) add a config.py file with the following values: reddit_client_id, reddit_client_secret, reddit_user_agent, news_api_key 

5) cd into the directory for the repository, activate your virtual environment and run pip install -r requirements.txt

6) run: uvicorn main:app --reload

the application is now live on your localhost
