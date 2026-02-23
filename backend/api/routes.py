from fastapi import APIRouter, HTTPException
import os
import uuid
from ..config import settings

router = APIRouter(prefix="/api", tags=["api"])

@router.get("/avatars")
async def get_avatars():
    """List all available avatars"""
    avatars = []
    for category in settings.AVATAR_MODELS:
        category_path = os.path.join(settings.AVATAR_DIR, category)
        if os.path.exists(category_path):
            for avatar_name in os.listdir(category_path):
                avatar_dir = os.path.join(category_path, avatar_name)
                if os.path.isdir(avatar_dir):
                    avatars.append({
                        "id": f"{category}/{avatar_name}",
                        "name": avatar_name.replace("_", " ").title(),
                        "category": category,
                        "thumbnail": f"/avatars/{category}/{avatar_name}/thumbnail.jpg"
                    })
    return {"avatars": avatars}

@router.post("/sessions/create")
async def create_session(avatar_id: str):
    """Create a new avatar session"""
    session_id = str(uuid.uuid4())
    return {
        "session_id": session_id,
        "avatar_id": avatar_id,
        "websocket_url": f"ws://{settings.HOST}:{settings.PORT}/ws/{session_id}"
    }

@router.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}