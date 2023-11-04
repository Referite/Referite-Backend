from enum import Enum


class SportStatus(Enum):
    CEREMONIES = "CEREMONIES"
    COMPETITIVE = "COMPETITIVE"
    TROPHY = "TROPHY"
    RECORDED = "RECORDED"

    def __str__(self):
        return self.value
