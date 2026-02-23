from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from loguru import logger
import os

from backend.config import settings
from backend.api.websocket import AvatarWebSocket  
from backend.services.stt_service import SpeechToTextService
from backend.services.tts_service import TextToSpeechService
from backend.services.viseme_service import VisemeService
from backend.services.lipsync_service import LipSyncService
from backend.services.avatar_service import AvatarRenderService

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Avatar Communication System"
)

logger.add("app.log", rotation="500 MB")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
app.mount("/avatars", StaticFiles(directory=settings.AVATAR_DIR), name="avatars")
app.mount("/outputs", StaticFiles(directory=settings.OUTPUT_DIR), name="outputs")
stt_service: SpeechToTextService = None
tts_service: TextToSpeechService = None
viseme_service: VisemeService = None
lipsync_service: LipSyncService = None
render_service: AvatarRenderService = None
ws_handler: AvatarWebSocket = None
@app.on_event("startup")
async def startup_event():
    global stt_service, tts_service, viseme_service, lipsync_service, render_service, ws_handler

    stt_service = SpeechToTextService(engine=settings.STT_ENGINE)
    tts_service = TextToSpeechService(engine=settings.TTS_ENGINE)
    viseme_service = VisemeService()
    lipsync_service = LipSyncService(avatar_path=settings.DEFAULT_AVATAR)
    render_service = AvatarRenderService(output_dir=settings.OUTPUT_DIR)

    ws_handler = AvatarWebSocket(
        stt_service=stt_service,
        tts_service=tts_service,
        viseme_service=viseme_service,
        lipsync_service=lipsync_service,
        render_service=render_service
    )

    logger.info("All services initialized!")

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.get("/dashboard")
async def dashboard():
    return FileResponse("frontend/dashboard.html")

@app.get("/api/avatars")
async def get_avatars():
    avatars = []
    for category in settings.AVATAR_MODELS:
        category_path = os.path.join(settings.AVATAR_DIR, category)
        if os.path.exists(category_path):
            for avatar in os.listdir(category_path):
                if os.path.isdir(os.path.join(category_path, avatar)):
                    avatars.append({
                        "id": f"{category}/{avatar}",
                        "name": avatar.replace("_", " ").title(),
                        "category": category,
                        "thumbnail": f"/avatars/{category}/{avatar}/thumbnail.jpg"
                    })
    return JSONResponse({"avatars": avatars})

@app.post("/api/sessions/create")
async def create_session(avatar_id: str):
    import uuid
    session_id = str(uuid.uuid4())
    return JSONResponse({
        "session_id": session_id,
        "avatar_id": avatar_id,
        "websocket_url": f"ws://{settings.HOST}:{settings.PORT}/ws/{session_id}"
    })

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await ws_handler.handle_connection(websocket, client_id)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}
if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,  
        log_level="info"
    )