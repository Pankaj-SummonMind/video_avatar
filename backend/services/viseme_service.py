import numpy as np
from typing import List, Dict
import json
from loguru import logger

class VisemeService:
    def __init__(self):
        # Load viseme mappings
        self.viseme_map = self._load_viseme_map()
        self.phoneme_to_viseme = self._load_phoneme_map()
        
    def _load_viseme_map(self) -> Dict:
        """Load viseme to shape mapping"""
        return {
            'viseme_silence': {'id': 0, 'jaw': 0.0, 'lip': 0.0, 'mouth_width': 0.2, 'mouth_height': 0.1},
            'viseme_aa': {'id': 1, 'jaw': 0.8, 'lip': 0.2, 'mouth_width': 0.8, 'mouth_height': 0.7},
            'viseme_ii': {'id': 2, 'jaw': 0.3, 'lip': 0.1, 'mouth_width': 0.5, 'mouth_height': 0.9},
            'viseme_uu': {'id': 3, 'jaw': 0.4, 'lip': 0.9, 'mouth_width': 0.6, 'mouth_height': 0.4},
            'viseme_ee': {'id': 4, 'jaw': 0.5, 'lip': 0.3, 'mouth_width': 0.7, 'mouth_height': 0.5},
            'viseme_oo': {'id': 5, 'jaw': 0.5, 'lip': 0.7, 'mouth_width': 0.6, 'mouth_height': 0.5},
            'viseme_k': {'id': 6, 'jaw': 0.3, 'lip': 0.2, 'mouth_width': 0.5, 'mouth_height': 0.3},
            'viseme_g': {'id': 7, 'jaw': 0.3, 'lip': 0.2, 'mouth_width': 0.5, 'mouth_height': 0.3},
            'viseme_t': {'id': 8, 'jaw': 0.2, 'lip': 0.1, 'mouth_width': 0.4, 'mouth_height': 0.2},
            'viseme_d': {'id': 9, 'jaw': 0.2, 'lip': 0.1, 'mouth_width': 0.4, 'mouth_height': 0.2},
            'viseme_n': {'id': 10, 'jaw': 0.2, 'lip': 0.1, 'mouth_width': 0.4, 'mouth_height': 0.2},
            'viseme_m': {'id': 11, 'jaw': 0.2, 'lip': 0.1, 'mouth_width': 0.4, 'mouth_height': 0.2},
            'viseme_p': {'id': 12, 'jaw': 0.1, 'lip': 0.1, 'mouth_width': 0.3, 'mouth_height': 0.1},
            'viseme_b': {'id': 13, 'jaw': 0.1, 'lip': 0.1, 'mouth_width': 0.3, 'mouth_height': 0.1},
            'viseme_s': {'id': 14, 'jaw': 0.1, 'lip': 0.1, 'mouth_width': 0.4, 'mouth_height': 0.1},
            'viseme_h': {'id': 15, 'jaw': 0.3, 'lip': 0.2, 'mouth_width': 0.5, 'mouth_height': 0.3}
        }
        
    def _load_phoneme_map(self) -> Dict:
        """Map phonemes to viseme IDs (simplified)"""
        return {
            'aa': 'viseme_aa', 'ae': 'viseme_aa', 'ah': 'viseme_aa',
            'eh': 'viseme_ee', 'er': 'viseme_ee', 'ey': 'viseme_ee',
            'ih': 'viseme_ii', 'iy': 'viseme_ii',
            'ow': 'viseme_oo', 'oy': 'viseme_oo', 'uw': 'viseme_uu',
            'p': 'viseme_p', 'b': 'viseme_b', 'm': 'viseme_m',
            't': 'viseme_t', 'd': 'viseme_d', 'n': 'viseme_n',
            'k': 'viseme_k', 'g': 'viseme_g', 'ng': 'viseme_g',
            's': 'viseme_s', 'z': 'viseme_s', 'sh': 'viseme_s',
            'h': 'viseme_h',
            'sil': 'viseme_silence'
        }
        
    def generate_visemes(self, timings: List[Dict]) -> List[Dict]:
        """Generate viseme sequence from word timings"""
        viseme_sequence = []
        
        for item in timings:
            word = item.get('word', '')
            start = item.get('start', 0)
            end = item.get('end', 0.5)
            
            # Get phonemes for word (simplified - use actual phonemizer in production)
            phonemes = self._text_to_phonemes(word)
            
            # Distribute phonemes across word duration
            if phonemes:
                phoneme_duration = (end - start) / len(phonemes)
                for i, phoneme in enumerate(phonemes):
                    phoneme_start = start + i * phoneme_duration
                    phoneme_end = phoneme_start + phoneme_duration
                    
                    viseme_name = self.phoneme_to_viseme.get(phoneme, 'viseme_silence')
                    viseme = self.viseme_map.get(viseme_name, self.viseme_map['viseme_silence'])
                    
                    viseme_sequence.append({
                        'viseme': viseme_name,
                        'start': phoneme_start,
                        'end': phoneme_end,
                        'blend': 0.1,  # 100ms blend
                        'shape': viseme
                    })
            else:
                # No phonemes, use silence
                viseme_sequence.append({
                    'viseme': 'viseme_silence',
                    'start': start,
                    'end': end,
                    'blend': 0.1,
                    'shape': self.viseme_map['viseme_silence']
                })
                
        return viseme_sequence
        
    def _text_to_phonemes(self, text: str) -> List[str]:
        """Very simplified phoneme conversion - replace with real phonemizer"""
        # This should use a proper phonemizer like gruut or espeak
        phonemes = []
        for char in text.lower():
            if char in 'aeiou':
                phonemes.append('aa')  # Simplified
            elif char.isalpha():
                phonemes.append(char)
        return phonemes