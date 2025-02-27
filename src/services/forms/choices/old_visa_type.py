from src.entities.form import OldVisaTypeInd

OLD_VISA_IND = list(OldVisaTypeInd)

OLD_VISA_IND_OUTPUT = {
    OldVisaTypeInd.E_VISA: "Электронная тур.виза",
    OldVisaTypeInd.TOURIST_VISA: "Тур.виза вклейка",
    OldVisaTypeInd.BUSINESS_VISA: "Бизнес виза",
    OldVisaTypeInd.MEDICAL_VISA: "Медицинская виза",
}
