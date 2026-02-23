import asyncio
import json
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate
from aiortc.contrib.media import MediaPlayer
from loguru import logger

class WebRTCService:
    def __init__(self):
        self.peer_connections = {}  # peer_id -> RTCPeerConnection

    async def create_peer_connection(self, peer_id, on_track_callback=None):
        """Create a new RTCPeerConnection"""
        pc = RTCPeerConnection()
        self.peer_connections[peer_id] = pc

        if on_track_callback:
            @pc.on("track")
            async def on_track(track):
                await on_track_callback(track)

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            logger.info(f"ICE connection state for {peer_id}: {pc.iceConnectionState}")
            if pc.iceConnectionState == "failed":
                await pc.close()
                self.peer_connections.pop(peer_id, None)

        return pc

    async def handle_offer(self, peer_id, offer_sdp, on_track_callback=None):
        """Process an offer and return answer"""
        pc = await self.create_peer_connection(peer_id, on_track_callback)
        await pc.setRemoteDescription(RTCSessionDescription(sdp=offer_sdp, type="offer"))
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        return pc.localDescription

    async def add_ice_candidate(self, peer_id, candidate_dict):
        """Add an ICE candidate to the peer connection"""
        pc = self.peer_connections.get(peer_id)
        if pc:
            candidate = RTCIceCandidate(
                sdpMid=candidate_dict["sdpMid"],
                sdpMLineIndex=candidate_dict["sdpMLineIndex"],
                candidate=candidate_dict["candidate"]
            )
            await pc.addIceCandidate(candidate)

    async def close_connection(self, peer_id):
        """Close a peer connection"""
        pc = self.peer_connections.pop(peer_id, None)
        if pc:
            await pc.close()

    def get_connection(self, peer_id):
        return self.peer_connections.get(peer_id)