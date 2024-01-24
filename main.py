import sys
from fastapi import FastAPI

from api.speak import speak_api
from api.listen import listen_api
from api.files import files_api

def debugger_is_active() -> bool:
    """Return if the debugger is currently active"""
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None

app = FastAPI(
    title='Gemi Voice API',
    openapi_url='/gemi_voice.openapi.json' if debugger_is_active() else None,
    docs_url='/swagger' if debugger_is_active() else None
)

app.include_router(speak_api, prefix='/api/speak')
app.include_router(listen_api, prefix='/api/listen')
app.include_router(files_api, prefix='/api/files')

@app.get("/ping")
async def root():
    return {"message": "pong"}