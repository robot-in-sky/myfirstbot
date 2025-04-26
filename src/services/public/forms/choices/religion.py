from enum import StrEnum, auto


class ReligionInd(StrEnum):
    BAHAI = auto()
    BUDDHISM = auto()
    CHRISTIAN = auto()
    HINDU = auto()
    ISLAM = auto()
    JAINISM = auto()
    JUDAISM = auto()
    OTHERS = auto()
    PARSI = auto()
    SIKH = auto()
    ZOROASTRIAN = auto()


RELIGION_IND_ALL = list(ReligionInd)

RELIGION_IND_FEATURED = [ReligionInd.CHRISTIAN,
                         ReligionInd.HINDU,
                         ReligionInd.BUDDHISM,
                         ReligionInd.ISLAM]


RELIGION_IND_OUTPUT = {
    ReligionInd.BAHAI: "Бахаи",
    ReligionInd.BUDDHISM: "Буддизм",
    ReligionInd.CHRISTIAN: "Христианство",
    ReligionInd.HINDU: "Индуизм",
    ReligionInd.ISLAM: "Ислам",
    ReligionInd.JAINISM: "Джайнизм",
    ReligionInd.JUDAISM: "Иудаизм",
    ReligionInd.PARSI: "Парсизм",
    ReligionInd.SIKH: "Сикхизм",
    ReligionInd.ZOROASTRIAN: "Зороастризм",
    ReligionInd.OTHERS: "Другое",
}
