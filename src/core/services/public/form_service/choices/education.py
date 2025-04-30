from enum import StrEnum


class EducationInd(StrEnum):
    BELOW_MATRICULATION = "BELOW MATRICULATION"
    GRADUATE = "GRADUATE"
    HIGHER_SECONDARY = "HIGHER SECONDARY"
    ILLITERATE = "ILLITERATE"
    MATRICULATION = "MATRICULATION"
    NA_BEING_MINOR = "NA BEING MINOR"
    OTHERS = "OTHERS"
    POST_GRADUATE = "POST GRADUATE"
    PROFESSIONAL = "PROFESSIONAL"


EDUCATION_IND_FEATURED = [EducationInd.NA_BEING_MINOR, EducationInd.BELOW_MATRICULATION,
                          EducationInd.MATRICULATION, EducationInd.HIGHER_SECONDARY,
                          EducationInd.PROFESSIONAL, EducationInd.GRADUATE,
                          EducationInd.POST_GRADUATE, EducationInd.ILLITERATE]

EDUCATION_IND_ALL = EDUCATION_IND_FEATURED    # Without OTHERS


EDUCATION_IND_OUTPUT = {
    EducationInd.NA_BEING_MINOR: "Дошкольник",
    EducationInd.BELOW_MATRICULATION: "Школьник",
    EducationInd.MATRICULATION: "Общее",
    EducationInd.HIGHER_SECONDARY: "Среднее",
    EducationInd.PROFESSIONAL: "Профессиональное",
    EducationInd.GRADUATE: "Университет",
    EducationInd.POST_GRADUATE: "Аспирантура",
    EducationInd.ILLITERATE: "Без образования",
    EducationInd.OTHERS: "Другое",
}
