import re

TRANSLIT_DICT_LOWER = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}
TRANSLIT_DICT_UPPER = {k.upper(): v.title() for k, v in TRANSLIT_DICT_LOWER.items()}
TRANSLIT_DICT = TRANSLIT_DICT_LOWER | TRANSLIT_DICT_UPPER

def translit(text: str) -> str:
    result = ""
    for char in text:
        result += TRANSLIT_DICT.get(char, char)
    return result


REGIONS_TRANSLATIONS = {
    # Россия
    "МОСКВА": "MOSCOW",
    "САНКТ ПЕТЕРБУРГ": "SAINT PETERSBURG",
    "СЕВАСТОПОЛЬ": "SEVASTOPOL",
    "АДЫГЕЯ": "ADYGEA REPUBLIC",
    "РЕСПУБЛИКА АЛТАЙ": "ALTAY REPUBLIC",
    "РЕСП АЛТАЙ": "ALTAY REPUBLIC",
    "БАШКОРТОСТАН": "BASHKORTOSTAN REPUBLIC",
    "БУРЯТИЯ": "BURYATIA REPUBLIC",
    "ДАГЕСТАН": "DAGESTAN REPUBLIC",
    "ИНГУШЕТИЯ": "INGUSHETIA REPUBLIC",
    "КАБАРДИНО БАЛКАРСКАЯ РЕСП": "KABARDINO-BALKAR REPUBLIC",
    "КАБАРДИНО БАЛКАРИЯ": "KABARDINO-BALKAR REPUBLIC",
    "КАРАЧАЕВО ЧЕРКЕССКАЯ РЕСП": "KARACHAY-CHERKESS REPUBLIC",
    "КАРАЧАЕВО ЧЕРКЕСИЯ": "KARACHAY-CHERKESS REPUBLIC",
    "КАЛМЫКИЯ": "KALMYKIA REPUBLIC",
    "КАРЕЛИЯ": "KARELIA REPUBLIC",
    "КОМИ": "KOMI REPUBLIC",
    "МАРИЙ ЭЛ": "MARI EL REPUBLIC",
    "МОРДОВИЯ": "MORDOVIA REPUBLIC",
    "САХА": "SAKHA (YAKUTIA) REPUBLIC",
    "ЯКУТИЯ": "SAKHA (YAKUTIA) REPUBLIC",
    "СЕВЕРНАЯ ОСЕТИЯ": "NORTH OSSETIA-ALANIA REPUBLIC",
    "ТАТАРСТАН": "TATARSTAN REPUBLIC",
    "ТЫВА": "TUVA REPUBLIC",
    "ХАКАСИЯ": "KHAKASSIA REPUBLIC",
    "ЧЕЧЕНСКАЯ РЕСП": "CHECHEN REPUBLIC",
    "ЧЕЧНЯ": "CHECHEN REPUBLIC",
    "ЧУВАШСКАЯ РЕСП": "CHUVASH REPUBLIC",
    "ЧУВАШИЯ": "CHUVASH REPUBLIC",
    "АЛТАЙСКИЙ КРАЙ": "ALTAY REGION",
    "ЗАБАЙКАЛЬСКИЙ КРАЙ": "ZABAIKAL REGION",
    "КАМЧАТСКИЙ КРАЙ": "KAMCHATKA REGION",
    "КРАСНОДАРСКИЙ КРАЙ": "KRASNODAR REGION",
    "КРАСНОЯРСКИЙ КРАЙ": "KRASNOYAR REGION",
    "ПЕРМСКИЙ КРАЙ": "PERM REGION",
    "ПРИМОРСКИЙ КРАЙ": "PRIMORYE REGION",
    "СТАВРОПОЛЬСКИЙ КРАЙ": "STAVROPOL REGION",
    "ХАБАРОВСКИЙ КРАЙ": "KHABAROVSK REGION",
    "АМУРСКАЯ ОБЛ": "AMUR REGION",
    "АРХАНГЕЛЬСКАЯ ОБЛ": "ARKHANGELSK REGION",
    "АСТРАХАНСКАЯ ОБЛ": "ASTRAKHAN REGION",
    "БЕЛГОРОДСКАЯ ОБЛ": "BELGOROD REGION",
    "БРЯНСКАЯ ОБЛ": "BRYANSK REGION",
    "ВЛАДИМИРСКАЯ ОБЛ": "VLADIMIR REGION",
    "ВОЛГОГРАДСКАЯ ОБЛ": "VOLGOGRAD REGION",
    "ВОЛОГОДСКАЯ ОБЛ": "VOLOGDA REGION",
    "ВОРОНЕЖСКАЯ ОБЛ": "VORONEZH REGION",
    "ИВАНОВСКАЯ ОБЛ": "IVANOVO REGION",
    "ИРКУТСКАЯ ОБЛ": "IRKUTSK REGION",
    "КАЛИНИНГРАДСКАЯ ОБЛ": "KALININGRAD REGION",
    "КАЛУЖСКАЯ ОБЛ": "KALUGA REGION",
    "КЕМЕРОВСКАЯ ОБЛ": "KEMEROVO REGION",
    "КИРОВСКАЯ ОБЛ": "KIROV REGION",
    "КУРГАНСКАЯ ОБЛ": "KURGAN REGION",
    "КУРСКАЯ ОБЛ": "KURSK REGION",
    "ЛЕНИНГРАДСКАЯ ОБЛ": "LENINGRAD REGION",
    "ЛИПЕЦКАЯ ОБЛ": "LIPETSK REGION",
    "МАГАДАНСКАЯ ОБЛ": "MAGADAN REGION",
    "МОСКОВСКАЯ ОБЛ": "MOSCOW REGION",
    "МУРМАНСКАЯ ОБЛ": "MURMANSK REGION",
    "НИЖЕГОРОДСКАЯ ОБЛ": "NIZHNY NOVGOROD REGION",
    "НОВГОРОДСКАЯ ОБЛ": "NOVGOROD REGION",
    "НОВОСИБИРСКАЯ ОБЛ": "NOVOSIBIRSK REGION",
    "ОМСКАЯ ОБЛ": "OMSK REGION",
    "ОРЕНБУРГСКАЯ ОБЛ": "ORENBURG REGION",
    "ОРЛОВСКАЯ ОБЛ": "OREL REGION",
    "ПЕНЗЕНСКАЯ ОБЛ": "PENZA REGION",
    "ПСКОВСКАЯ ОБЛ": "PSKOV REGION",
    "РОСТОВСКАЯ ОБЛ": "ROSTOV REGION",
    "РЯЗАНСКАЯ ОБЛ": "RYAZAN REGION",
    "САМАРСКАЯ ОБЛ": "SAMARA REGION",
    "САРАТОВСКАЯ ОБЛ": "SARATOV REGION",
    "САХАЛИНСКАЯ ОБЛ": "SAKHALIN REGION",
    "СМОЛЕНСКАЯ ОБЛ": "SMOLENSK REGION",
    "СВЕРДЛОВСКАЯ ОБЛ": "SVERDLOVSK REGION",
    "ТАМБОВСКАЯ ОБЛ": "TAMBOV REGION",
    "ТВЕРСКАЯ ОБЛ": "TVER REGION",
    "ТОМСКАЯ ОБЛ": "TOMSK REGION",
    "ТУЛЬСКАЯ ОБЛ": "TULA REGION",
    "ТЮМЕНСКАЯ ОБЛ": "TYUMEN REGION",
    "УЛЬЯНОВСКАЯ ОБЛ": "ULYANOVSK REGION",
    "ЧЕЛЯБИНСКАЯ ОБЛ": "CHELYABINSK REGION",
    "ЯРОСЛАВСКАЯ ОБЛ": "YAROSLAVL REGION",
    "ЕВРЕЙСКАЯ": "JEWISH AUTONOMOUS REGION",
    "ХАНТЫ МАНСИЙСКИЙ А": "KHANTY-MANSI AUTONOMOUS DISTRICT",
    "ЧУКОТСКИЙ А": "CHUKOTKA AUTONOMOUS DISTRICT",
    "ЯМАЛО НЕНЕЦКИЙ А": "YAMALO-NENETS AUTONOMOUS DISTRICT",
    "НЕНЕЦКИЙ А": "NENETS AUTONOMOUS DISTRICT",

    # Казахстан
    "АКМОЛИНСКАЯ ОБЛ": "AKMOLA REGION",
    "АКТЮБИНСКАЯ ОБЛ": "AKTOBE REGION",
    "АЛМАТИНСКАЯ ОБЛ": "ALMATY REGION",
    "АТЫРАУСКАЯ ОБЛ": "ATYRAU REGION",
    "ВОСТОЧНО КАЗАХСТАНСКАЯ ОБЛ": "EAST KAZAKHSTAN REGION",
    "ЖАМБЫЛСКАЯ ОБЛ": "ZHAMBUL REGION",
    "ЗАПАДНАО КАЗАХСТАНСКАЯ ОБЛ": "WEST KAZAKHSTAN REGION",
    "КАРАГАНДИНСКАЯ ОБЛ": "KARAGANDA REGION",
    "КЫЗЫЛОРДИНСКАЯ ОБЛ": "KYZYLORDA REGION",
    "КОСТАНАЙСКАЯ ОБЛ": "KOSTANAY REGION",
    "МАНГУСТАУСКАЯ ОБЛ": "MANGYSTAU REGION",
    "ПАВЛОДАРСКАЯ ОБЛ": "PAVLODAR REGION",
    "ТУРКЕСТАНСКАЯ ОБЛ": "TURKESTAN REGION",
    "СЕВЕРО КАЗАХСТАНСКАЯ ОБЛ": "NORTH KAZAKHSTAN REGION",
    "АБАЙСКАЯ ОБЛ": "ABAY REGION",
    "ЖЕТЫСУСКАЯ ОБЛ": "ZHETYSU REGION",
    "УЛЫТАУСКАЯ ОБЛ": "ULYTAU REGION",

    # Беларусь
    "МИНСКАЯ ОБЛ": "MINSK REGION",
    "БРЕСТСКАЯ ОБЛ": "BREST REGION",
    "ВИТЕБСКАЯ ОБЛ": "VITEBSK REGION",
    "ГОМЕЛЬСКАЯ ОБЛ": "GOMEL REGION",
    "ГРОДНЕНСКАЯ ОБЛ": "GRODNO REGION",
    "МОГИЛЁВСКАЯ ОБЛ": "MOGILEV REGION",
}

def normalize_name(text: str) -> str:
    text = text.strip().upper().replace("-", " ")
    return re.sub(r"\s+", " ", text)


def remove_city_prefix(text: str) -> str:
    text = re.sub(r"^(гор\.|г\.|с\.|село\.|дер\.|д\.)\s*", "", text, flags=re.IGNORECASE)
    return re.sub(r"(\s)(гор\.|г\.|с\.|село\.|дер\.|д\.)\s*", r"\1", text, flags=re.IGNORECASE)


def format_address(text: str) -> str:
    text = remove_city_prefix(text)
    text = re.sub(r"^(ул\.)\s*", "st. ", text, flags=re.IGNORECASE)
    text = re.sub(r"(\s)(ул\.)\s*", r"\1st. ", text, flags=re.IGNORECASE)
    text = re.sub(r"^(просп\.)\s*", "ave. ", text, flags=re.IGNORECASE)
    text = re.sub(r"(\s)(просп\.)\s*", r"\1ave. ", text, flags=re.IGNORECASE)
    text = re.sub(r"^(пер\.)\s*", "lane. ", text, flags=re.IGNORECASE)
    text = re.sub(r"(\s)(пер\.)\s*", r"\1lane. ", text, flags=re.IGNORECASE)
    text = re.sub(r"^(кв\.)\s*", "apt. ", text, flags=re.IGNORECASE)
    text = re.sub(r"(\s)(кв\.)\s*", r"\1apt. ", text, flags=re.IGNORECASE)
    return translit(text).strip()


def format_place_name(text: str) -> str:
    normalized_name = normalize_name(text)
    for k, v in REGIONS_TRANSLATIONS.items():
        if k in normalized_name:
            return v.title()
    text = remove_city_prefix(text)
    return translit(text).strip()


IND_PLACES_TRANSLATIONS = {
    "ДЕЛИ": "DELHI",
    "НЬЮ ДЕЛИ": "NEW DELHI",
    "ДЖАЙПУР": "JAIPUR",
    "ВАРАНАСИ": "VARANASI",
    "БЕНАРЕС": "VARANASI",
    "РИШИКЕШ": "RISHIKESH",
    "МУМБАИ": "MUMBAI",
    "МУМБАЙ": "MUMBAI",
    "БОМБЕЙ": "MUMBAI",
    "ПЕНДЖАБ": "PUNJAB",
    "КАЛЬКУТТА": "KOLKATA",
    "БЕНГАЛУРУ": "BANGALORE",
    "БАНГАЛОР": "BANGALORE",
    "МАДРАС": "CHENNAI",
    "ЧЕННАЙ": "CHENNAI",
    "КОЧИН": "KOCHI",
    "ОРИССА": "ODISHA",
    "ПОНДИШЕРРИ": "PONDICHERRY",
    "ЗАПАДНАЯ БЕНГАЛИЯ": "WEST BENGAL",
}

def format_ind_places(text: str) -> str:
    text = normalize_name(text)
    for k, v in IND_PLACES_TRANSLATIONS.items():
        text = text.replace(k, v)
    return translit(text).strip().title()


