from enum import StrEnum, auto


class VisaType(StrEnum):
    TOUR_30D = auto()  # eTourist Visa (for 30 Days)
    TOUR_1Y = auto()  # eTourist Visa (for 1 Year)
    TOUR_5Y = auto()  # eTourist Visa (for 5 Years)
