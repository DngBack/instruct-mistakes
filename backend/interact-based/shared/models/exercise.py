from __future__ import annotations

from enum import Enum


class ExercisesType(str, Enum):
    """Enum for exercise types"""

    COMPLEDTED_WORDS = 'completed_words'
