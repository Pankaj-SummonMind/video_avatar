from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VisemeMapping(Base):
    __tablename__ = "viseme_mappings"
    
    id = Column(Integer, primary_key=True, index=True)
    phoneme = Column(String, unique=True, index=True, nullable=False)
    viseme_name = Column(String, nullable=False)
    mouth_width = Column(Float, default=0.5)
    mouth_height = Column(Float, default=0.3)
    jaw_open = Column(Float, default=0.3)
    lip_round = Column(Float, default=0.2)
    duration_ms = Column(Integer, default=100)

    @classmethod
    def get_default_mappings(cls):
        return {
            "aa": {"viseme": "viseme_aa", "width": 0.8, "height": 0.7, "jaw": 0.8, "round": 0.2},
            "ii": {"viseme": "viseme_ii", "width": 0.5, "height": 0.9, "jaw": 0.3, "round": 0.1},
            "uu": {"viseme": "viseme_uu", "width": 0.6, "height": 0.4, "jaw": 0.4, "round": 0.9},
            "ee": {"viseme": "viseme_e", "width": 0.7, "height": 0.5, "jaw": 0.5, "round": 0.3},
            "oo": {"viseme": "viseme_o", "width": 0.6, "height": 0.5, "jaw": 0.5, "round": 0.7},
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
            "sil": {"viseme": "viseme_silence", "width": 0.2, "height": 0.1, "jaw": 0.0, "round": 0.0},
        }