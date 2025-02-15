from src.entities.form import ReligionInd

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
    ReligionInd.OTHERS: "Другое",
    ReligionInd.PARSI: "Парсизм",
    ReligionInd.SIKH: "Сикхизм",
    ReligionInd.ZOROASTRIAN: "Зороастризм",
}
