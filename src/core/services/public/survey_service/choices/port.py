from enum import StrEnum, auto


class PortInd(StrEnum):
    I022 = auto()  # AHMEDABAD AIRPORT
    I032 = auto()  # AMRITSAR AIRPORT
    I096 = auto()  # BAGDOGRA AIRPORT
    I085 = auto()  # BENGALURU AIRPORT
    I084 = auto()  # BHUBANESHWAR AIRPORT
    I010 = auto()  # CALICUT AIRPORT
    I005 = auto()  # CHANDIGARH AIRPORT
    I008 = auto()  # CHENNAI AIRPORT
    I208 = auto()  # CHENNAI SEAPORT
    I024 = auto()  # COCHIN AIRPORT
    I224 = auto()  # COCHIN SEAPORT
    I094 = auto()  # COIMBATORE AIRPORT
    I004 = auto()  # DELHI AIRPORT
    I012 = auto()  # GAYA AIRPORT
    I033 = auto()  # GOA AIRPORT(DABOLIM)
    I034 = auto()  # GOA AIRPORT (MOPA)
    I283 = auto()  # GOA SEAPORT
    I019 = auto()  # GUWAHATI AIRPORT
    I041 = auto()  # HYDERABAD AIRPORT
    I017 = auto()  # INDORE AIRPORT
    I006 = auto()  # JAIPUR AIRPORT
    I030 = auto()  # KANNUR AIRPORT
    I002 = auto()  # KOLKATA AIRPORT
    I021 = auto()  # LUCKNOW AIRPORT
    I015 = auto()  # MADURAI AIRPORT
    I092 = auto()  # MANGALORE AIRPORT
    I293 = auto()  # MANGALORE SEAPORT
    I001 = auto()  # MUMBAI AIRPORT
    I201 = auto()  # MUMBAI SEAPORT
    I016 = auto()  # NAGPUR AIRPORT
    I077 = auto()  # PORTBLAIR AIRPORT
    I277 = auto()  # PORT BLAIR SEAPORT
    I026 = auto()  # PUNE AIRPORT
    I003 = auto()  # TIRUCHIRAPALLI AIRPORT
    I023 = auto()  # TRIVANDRUM AIRPORT
    I007 = auto()  # VARANASI AIRPORT
    I025 = auto()  # VISHAKHAPATNAM AIRPORT


PORT_IND_ALL = list(PortInd)

PORT_IND_FEATURED = [PortInd.I033,
                     PortInd.I034,
                     PortInd.I004,
                     PortInd.I001]

PORT_IND_OUTPUT = {
    PortInd.I022: "Аэропорт Ахмедабад",
    PortInd.I032: "Аэропорт Амритсар",
    PortInd.I096: "Аэропорт Багдогра",
    PortInd.I085: "Аэропорт Бенгалуру",
    PortInd.I084: "Аэропорт Бхубанешвар",
    PortInd.I010: "Аэропорт Каликут",
    PortInd.I005: "Аэропорт Чандигарх",
    PortInd.I008: "Аэропорт Ченнай",
    PortInd.I208: "Морской Порт Ченнай",
    PortInd.I024: "Аэропорт Кочин",
    PortInd.I224: "Морской Порт Кочин",
    PortInd.I094: "Аэропорт Коимбаторе",
    PortInd.I004: "Аэропорт Дели",
    PortInd.I012: "Аэропорт Гайя",
    PortInd.I033: "Аэропорт Гоа (Даболим)",
    PortInd.I034: "Аэропорт Гоа (Мопа)",
    PortInd.I283: "Морской Порт Гоа",
    PortInd.I019: "Аэропорт Гувахати",
    PortInd.I041: "Аэропорт Хайдерабад",
    PortInd.I017: "Аэропорт Индор",
    PortInd.I006: "Аэропорт Джайпур",
    PortInd.I030: "Аэропорт Каннур",
    PortInd.I002: "Аэропорт Колката",
    PortInd.I021: "Аэропорт Удачноу",
    PortInd.I015: "Аэропорт Мадурай",
    PortInd.I092: "Аэропорт Мангалор",
    PortInd.I293: "Морской Порт Мангалор",
    PortInd.I001: "Аэропорт Мумбаи",
    PortInd.I201: "Морской Порт Мумбаи",
    PortInd.I016: "Аэропорт Нагпур",
    PortInd.I077: "Аэропорт Портблейр",
    PortInd.I277: "Морской Порт Портблейр",
    PortInd.I026: "Аэропорт Пуна",
    PortInd.I003: "Аэропорт Тиручирапалли",
    PortInd.I023: "Аэропорт Тривандрум",
    PortInd.I007: "Аэропорт Варанаси",
    PortInd.I025: "Аэропорт Вишакхапатнам",
}
