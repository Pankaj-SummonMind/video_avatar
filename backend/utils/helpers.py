import base64
import hashlib
import os
import json
from pathlib import Path
from loguru import logger
import numpy as np
def encode_audio_to_base64(audio_bytes: bytes) -> str:
    """Encode audio bytes to base64 string"""
    return base64.b64encode(audio_bytes).decode('utf-8')

def decode_base64_to_audio(base64_str: str) -> bytes:
    """Decode base64 string to audio bytes"""
    return base64.b64decode(base64_str)

def get_cache_key(text: str, voice: str) -> str:
    """Generate a cache key for TTS"""
    return hashlib.md5(f"{text}_{voice}".encode()).hexdigest()

def ensure_dir(path: str):
    """Ensure directory exists"""
    Path(path).mkdir(parents=True, exist_ok=True)

def save_json(data, filepath):
    """Save data as JSON"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(filepath):
    """Load JSON data"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def bytes_to_ndarray(audio_bytes: bytes, sample_width=2, channels=1, sample_rate=16000):
    """Convert audio bytes to numpy array (simplified)"""
    import numpy as np
    return np.frombuffer(audio_bytes, dtype=np.int16).reshape(-1, channels)

def ndarray_to_bytes(audio_array: np.ndarray):
    """Convert numpy array to bytes"""
    return audio_array.tobytes()