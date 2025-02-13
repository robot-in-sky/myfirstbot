from src.entities.form import MartialStatus

MARTIAL_STATUS_ALL = list(MartialStatus)

MARTIAL_STATUS_DEFAULT = MARTIAL_STATUS_ALL

MARTIAL_STATUS_OUTPUT = {
    MartialStatus.DIVORCEE: "Разведён",
    MartialStatus.MARRIED: "Замужем/Женат",
    MartialStatus.SINGLE: "Не замужем/женат",
}
