from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Go to /news to get news"}

@app.get("/news")
async def get_news(query: str = None):
    if query:
        return {"message": "News search"}
    else:
        return {"message": "News list"}