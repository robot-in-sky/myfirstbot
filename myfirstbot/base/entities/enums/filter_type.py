from enum import Enum


class FilterType(str, Enum):
    EQ = "eq"  # equal
    NE = "ne"  # not equal
    GT = "gt"  # greater than
    LT = "lt"  # less than
    GE = "ge"  # greater than or equal
    LE = "le"  # less than or equal
    IN = "in"  # in (for lists)
    NIN = "nin"  # not in
    LIKE = "like"  # like
    STARTS = "starts"  # starts with
    ENDS = "ends"  # ends with
    AGE = "age"  # age greater than or equal
    ALE = "ale"  # age less than or equal
    RAW = "raw"  # raw SQL