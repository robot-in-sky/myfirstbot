from src.entities.form import EducationInd

EDUCATION_IND_DEFAULT = [EducationInd.NA_BEING_MINOR, EducationInd.BELOW_MATRICULATION,
                            EducationInd.MATRICULATION, EducationInd.HIGHER_SECONDARY,
                            EducationInd.PROFESSIONAL, EducationInd.GRADUATE,
                            EducationInd.POST_GRADUATE, EducationInd.ILLITERATE]

EDUCATION_IND_ALL = EDUCATION_IND_DEFAULT    # Without OTHERS

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
