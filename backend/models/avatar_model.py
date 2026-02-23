from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import json

Base = declarative_base()

class Avatar(Base):
    __tablename__ = "avatars"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True) 
    model_path = Column(String)
    thumbnail_path = Column(String)
    gender = Column(String)  # male, female, neutral
    language = Column(String, default="hi-IN")
    voice_id = Column(String)  # TTS voice identifier
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    settings = Column(JSON, default={})  # Avatar specific settings
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "thumbnail": self.thumbnail_path,
            "gender": self.gender,
            "language": self.language,
            "voice_id": self.voice_id,
            "is_active": self.is_active
        }

class AvatarSession(Base):
    __tablename__ = "avatar_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    avatar_id = Column(Integer)
    user_id = Column(String, nullable=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(String, default="active")  # active, ended, error
    metadata = Column(JSON, default={})
    video_path = Column(String, nullable=True)
    
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "avatar_id": self.avatar_id,
            "status": self.status,
            "start_time": self.start_time.isoformat(),
            "video_path": self.video_path
        }

class VisemeMapping(Base):
    __tablename__ = "viseme_mappings"
    
    id = Column(Integer, primary_key=True, index=True)
    phoneme = Column(String, unique=True, index=True)
    viseme_shape = Column(String)  # viseme_aa, viseme_ii, etc.
    mouth_width = Column(Float)
    mouth_height = Column(Float)
    jaw_open = Column(Float)
    lip_round = Column(Float)
    duration_ms = Column(Integer, default=100)
    
    @classmethod
    def get_default_mappings(cls):
        return {
            # Vowels
            "aa": {"viseme": "viseme_aa", "width": 0.8, "height": 0.7, "jaw": 0.8, "round": 0.2},
            "ii": {"viseme": "viseme_ii", "width": 0.5, "height": 0.9, "jaw": 0.3, "round": 0.1},
            "uu": {"viseme": "viseme_uu", "width": 0.6, "height": 0.4, "jaw": 0.4, "round": 0.9},
            "ee": {"viseme": "viseme_e", "width": 0.7, "height": 0.5, "jaw": 0.5, "round": 0.3},
            "oo": {"viseme": "viseme_o", "width": 0.6, "height": 0.5, "jaw": 0.5, "round": 0.7},
            
            # Consonants
            "k": {"viseme": "viseme_k", "width": 0.5, "height": 0.3, "jaw": 0.3, "round": 0.2},
            "g": {"viseme": "viseme_g", "width": 0.5, "height": 0.3, "jaw": 0.3, "round": 0.2},
            "t": {"viseme": "viseme_t", "width": 0.4, "height": 0.2, "jaw": 0.2, "round": 0.1},
            "d": {"viseme": "viseme_d", "width": 0.4, "height": 0.2, "jaw": 0.2, "round": 0.1},
            "n": {"viseme": "viseme_n", "width": 0.4, "height": 0.2, "jaw": 0.2, "round": 0.1},
            "m": {"viseme": "viseme_m", "width": 0.4, "height": 0.2, "jaw": 0.2, "round": 0.1},
            "p": {"viseme": "viseme_p", "width": 0.3, "height": 0.1, "jaw": 0.1, "round": 0.1},
            "b": {"viseme": "viseme_b", "width": 0.3, "height": 0.1, "jaw": 0.1, "round": 0.1},
            "s": {"viseme": "viseme_s", "width": 0.4, "height": 0.1, "jaw": 0.1, "round": 0.1},
            "h": {"viseme": "viseme_h", "width": 0.5, "height": 0.3, "jaw": 0.3, "round": 0.2},
            
            # Silence
            "sil": {"viseme": "viseme_silence", "width": 0.2, "height": 0.1, "jaw": 0.0, "round": 0.0}
        }