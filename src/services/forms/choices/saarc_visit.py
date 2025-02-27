from .country import COUNTRY_OUTPUT, COUNTRY_SAARC

SAARC_LIST_TEXT = "\n".join(["• " + COUNTRY_OUTPUT.get(c) for c in COUNTRY_SAARC])

SAARC_YEAR = ["2025", "2024", "2023", "2022"]
SAARC_YEAR_OUTPUT = {i: i for i in SAARC_YEAR}

SAARC_VISIT_NUM = ["1", "2", "3", "4"]
SAARC_VISIT_NUM_OUTPUT = {i: i for i in SAARC_VISIT_NUM}
