import asyncio
import json
import uuid
from fastapi import WebSocket, WebSocketDisconnect
from loguru import logger
from typing import Dict, Set
import base64
class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.sessions: Dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept a WebSocket connection and register it."""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected")

    async def disconnect(self, client_id: str):
        """Remove a disconnected client."""
        websocket = self.active_connections.pop(client_id, None)
        if websocket:
            await websocket.close()
            logger.info(f"Client {client_id} disconnected")
        self.sessions.pop(client_id, None)
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        logger.info(f"Client {client_id} disconnected")
        
    async def send_message(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)
            
    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)

class AvatarWebSocket:
    def __init__(self, stt_service, tts_service, viseme_service, lipsync_service, render_service):
        self.manager = WebSocketManager()
        self.stt = stt_service
        self.tts = tts_service
        self.viseme = viseme_service
        self.lipsync = lipsync_service
        self.render = render_service
        
    async def handle_connection(self, websocket: WebSocket, client_id: str = None):
        if not client_id:
            client_id = str(uuid.uuid4())
            
        await self.manager.connect(websocket, client_id)
        
        try:
          
            await self.manager.send_message(client_id, {
                "type": "connected",
                "client_id": client_id,
                "message": "Connected to AI Avatar System"
            })
            
            while True:

                data = await websocket.receive_text()
                message = json.loads(data)
                
            
                if message["type"] == "audio":
                    await self.handle_audio(client_id, message)
                elif message["type"] == "text":
                    await self.handle_text(client_id, message)
                elif message["type"] == "llm_response":
                    await self.handle_llm_response(client_id, message)
                elif message["type"] == "select_avatar":
                    await self.handle_avatar_select(client_id, message)
                elif message["type"] == "ping":
                    await self.manager.send_message(client_id, {"type": "pong"})
                    
        except WebSocketDisconnect:
            self.manager.disconnect(client_id)
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            self.manager.disconnect(client_id)
            
    async def handle_audio(self, client_id: str, message: dict):
        """Handle incoming audio"""
        try:
            audio_data = base64.b64decode(message["audio"])
            text = await self.stt._convert_chunk(audio_data)
            
            if text:
                await self.manager.send_message(client_id, {
                    "type": "text_recognized",
                    "text": text,
                    "session_id": message.get("session_id")
                })
                
        except Exception as e:
            logger.error(f"Audio handling error: {e}")
            
    async def handle_text(self, client_id: str, message: dict):
        """Handle text message (to be sent to LLM)"""
        try:
            text = message["text"]
            await self.manager.send_message(client_id, {
                "type": "text_received",
                "text": text
            })

            await asyncio.sleep(1)
            
            await self.manager.send_message(client_id, {
                "type": "llm_request",
                "text": text,
                "callback_id": message.get("callback_id")
            })
            
        except Exception as e:
            logger.error(f"Text handling error: {e}")
            
    async def handle_llm_response(self, client_id: str, message: dict):
        """Handle LLM response and generate avatar video"""
        try:
            text = message["text"]
            avatar_id = message.get("avatar_id", "default")
            
            # Generate TTS
            audio_data, timings = await self.tts.synthesize(text)
            
            if not audio_data:
                raise Exception("TTS failed")
                
            # Generate visemes
            viseme_sequence = self.viseme.generate_visemes(timings)
            
            # Load avatar
            avatar_id = "professional/male"
            avatar_path = "avatars/professional/male/model.png"
            
            # Generate lip sync frames
            frames = self.lipsync.generate_frames(
                viseme_sequence,
                duration=len(audio_data) / 16000  
            )
            
            # Render video
            video_path = await self.render.render_video(frames, audio_data)
            
            if video_path:
                # Send video path back
                await self.manager.send_message(client_id, {
                    "type": "video_ready",
                    "video_path": video_path,
                    "session_id": message.get("session_id")
                })

                with open(video_path, 'rb') as f:
                    video_data = f.read()
                    
                await self.manager.send_message(client_id, {
                    "type": "video_data",
                    "video": base64.b64encode(video_data).decode(),
                    "format": "mp4"
                })
                
        except Exception as e:
            logger.error(f"LLM response handling error: {e}")
            await self.manager.send_message(client_id, {
                "type": "error",
                "message": str(e)
            })
            
    async def handle_avatar_select(self, client_id: str, message: dict):
        """Handle avatar selection"""
        try:
            avatar_id = message["avatar_id"]
            
            # Update session
            session_id = message.get("session_id", str(uuid.uuid4()))
            
            await self.manager.send_message(client_id, {
                "type": "avatar_selected",
                "avatar_id": avatar_id,
                "session_id": session_id,
                "message": f"Avatar {avatar_id} selected"
            })
            
        except Exception as e:
            logger.error(f"Avatar selection error: {e}")