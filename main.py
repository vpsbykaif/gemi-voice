from fastapi import FastAPI
from api.speak import speak_api

app = FastAPI()

app.mount('/api/speak', speak_api)

@app.get("/ping")
async def root():
    return {"message": "pong"}