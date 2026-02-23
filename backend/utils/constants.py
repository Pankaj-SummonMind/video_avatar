# Viseme IDs (common standard, e.g., Azure viseme IDs)
VISEME_MAP = {
    'sil': 0,
    'aa': 1,
    'ii': 2,
    'uu': 3,
    'ee': 4,
    'oo': 5,
    'k': 6,
    'g': 7,
    't': 8,
    'd': 9,
    'n': 10,
    'm': 11,
    'p': 12,
    'b': 13,
    's': 14,
    'h': 15,
}

# Mouth shape parameters for each viseme ID (normalized)
MOUTH_SHAPES = {
    0: {'width': 0.2, 'height': 0.1, 'jaw': 0.0, 'round': 0.0},   # silence
    1: {'width': 0.8, 'height': 0.7, 'jaw': 0.8, 'round': 0.2},   # aa
    2: {'width': 0.5, 'height': 0.9, 'jaw': 0.3, 'round': 0.1},   # ii
    3: {'width': 0.6, 'height': 0.4, 'jaw': 0.4, 'round': 0.9},   # uu
    4: {'width': 0.7, 'height': 0.5, 'jaw': 0.5, 'round': 0.3},   # ee
    5: {'width': 0.6, 'height': 0.5, 'jaw': 0.5, 'round': 0.7},   # oo
    6: {'width': 0.5, 'height': 0.3, 'jaw': 0.3, 'round': 0.2},   # k
    7: {'width': 0.5, 'height': 0.3, 'jaw': 0.3, 'round': 0.2},   # g
    8: {'width': 0.4, 'height': 0.2, 'jaw': 0.2, 'round': 0.1},   # t
    9: {'width': 0.4, 'height': 0.2, 'jaw': 0.2, 'round': 0.1},   # d
    10: {'width': 0.4, 'height': 0.2, 'jaw': 0.2, 'round': 0.1},  # n
    11: {'width': 0.4, 'height': 0.2, 'jaw': 0.2, 'round': 0.1},  # m
    12: {'width': 0.3, 'height': 0.1, 'jaw': 0.1, 'round': 0.1},  # p
    13: {'width': 0.3, 'height': 0.1, 'jaw': 0.1, 'round': 0.1},  # b
    14: {'width': 0.4, 'height': 0.1, 'jaw': 0.1, 'round': 0.1},  # s
    15: {'width': 0.5, 'height': 0.3, 'jaw': 0.3, 'round': 0.2},  # h
}

# Default avatar settings
DEFAULT_AVATAR_SETTINGS = {
    'fps': 30,
    'width': 1920,
    'height': 1080,
}

# Supported languages
SUPPORTED_LANGUAGES = ['hi-IN', 'en-US', 'gu-IN', 'ta-IN', 'te-IN', 'bn-IN']