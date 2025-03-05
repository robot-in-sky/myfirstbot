from enum import StrEnum


class OldVisaTypeInd(StrEnum):
    E_VISA = "100"
    TOURIST_VISA = "3"
    BUSINESS_VISA = "1"
    MEDICAL_VISA = "16"


OLD_VISA_IND = list(OldVisaTypeInd)


OLD_VISA_IND_OUTPUT = {
    OldVisaTypeInd.E_VISA: "Электронная тур.виза",
    OldVisaTypeInd.TOURIST_VISA: "Тур.виза вклейка",
    OldVisaTypeInd.BUSINESS_VISA: "Бизнес виза",
    OldVisaTypeInd.MEDICAL_VISA: "Медицинская виза",
}
