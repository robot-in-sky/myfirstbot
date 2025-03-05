from enum import StrEnum, auto


class MartialStatus(StrEnum):
    DIVORCEE = auto()
    MARRIED = auto()
    SINGLE = auto()


MARTIAL_STATUS_ALL = list(MartialStatus)

MARTIAL_STATUS_FEATURED = MARTIAL_STATUS_ALL


MARTIAL_STATUS_OUTPUT = {
    MartialStatus.MARRIED: "В браке",
    MartialStatus.SINGLE: "Холост/Не замужем",
    MartialStatus.DIVORCEE: "В разводе",
}
