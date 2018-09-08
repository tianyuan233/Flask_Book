from enum import Enum


class PendingStatus(Enum):
    """交易状态"""
    waiting = 1
    success = 2
    reject = 3
    redraw = 4
    # gifter_redraw = 5
