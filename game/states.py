"""Finite State Machine states for the Wordle game"""

import enum

class State(enum.Enum):
    """Possible states in the Wordle FSM"""
    WORD_ENTRY = enum.auto()
    CONFIRM = enum.auto()
    SCORE = enum.auto()
    IS_WINNER = enum.auto()
    REVIEW = enum.auto()
    CONFIRM_AFTER_REVIEW = enum.auto()
    DISPLAY = enum.auto()
    BAG_MENU = enum.auto()
    PROCESS_LETTERS = enum.auto()