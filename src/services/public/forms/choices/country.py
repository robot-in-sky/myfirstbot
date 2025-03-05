from src.entities.visas import Country

COUNTRY_FEATURED = [Country.RUS, Country.KAZ,
                    Country.BLR]

COUNTRY_FEATURED2 = [Country.IND, Country.NPL,
                     Country.THA, Country.VNM,
                     Country.TUR, Country.EGY,
                     Country.LKA]

COUNTRY_ALL = [
    Country.AUS,  # Австралия
    Country.AUT,  # Австрия
    Country.AZE,  # Азербайджан
    Country.ALB,  # Албания
    Country.DZA,  # Алжир
    Country.AIA,  # Ангилья
    Country.AGO,  # Ангола
    Country.AND,  # Андорра
    Country.ATG,  # Антигуа и Барбуда
    Country.ARG,  # Аргентина
    Country.ARM,  # Армения
    Country.ABW,  # Аруба
    Country.AFG,  # Афганистан
    Country.BHS,  # Багамские Острова
    Country.BGD,  # Бангладеш
    Country.BRB,  # Барбадос
    Country.BLZ,  # Белиз
    Country.BLR,  # Беларусь
    Country.BEL,  # Бельгия
    Country.BEN,  # Бенин
    Country.BGR,  # Болгария
    Country.BOL,  # Боливия
    Country.BIH,  # Босния и Герцеговина
    Country.BWA,  # Ботсвана
    Country.BRA,  # Бразилия
    Country.BRN,  # Бруней
    Country.BDI,  # Бурунди
    Country.BTN,  # Бутан
    Country.VUT,  # Вануату
    Country.VAT,  # Ватикан
    Country.GBR,  # Великобритания
    Country.HUN,  # Венгрия
    Country.VEN,  # Венесуэла
    Country.TLS,  # Восточный Тимор
    Country.VNM,  # Вьетнам
    Country.GAB,  # Габон
    Country.HTI,  # Гаити
    Country.GUY,  # Гайана
    Country.GMB,  # Гамбия
    Country.GHA,  # Гана
    Country.GTM,  # Гватемала
    Country.GIN,  # Гвинея
    Country.DEU,  # Германия
    Country.GGY,  # Гернси
    Country.GIB,  # Гибралтар
    Country.HND,  # Гондурас
    Country.HKG,  # Гонконг
    Country.GRD,  # Гренада
    Country.GRC,  # Греция
    Country.GEO,  # Грузия
    Country.DNK,  # Дания
    Country.JEY,  # Джерси
    Country.DJI,  # Джибути
    Country.DMA,  # Доминика
    Country.DOM,  # Доминиканская Республика
    Country.EGY,  # Египет
    Country.ZMB,  # Замбия
    Country.ZWE,  # Зимбабве
    Country.ISR,  # Израиль
    Country.IND,  # Индия
    Country.IDN,  # Индонезия
    Country.JOR,  # Иордания
    Country.IRN,  # Иран
    Country.IRL,  # Ирландия
    Country.ISL,  # Исландия
    Country.ESP,  # Испания
    Country.ITA,  # Италия
    Country.YEM,  # Йемен
    Country.CPV,  # Кабо-Верде
    Country.KAZ,  # Казахстан
    Country.CYM,  # Острова Кайман
    Country.KHM,  # Камбоджа
    Country.CMR,  # Камерун
    Country.CAN,  # Канада
    Country.QAT,  # Катар
    Country.KEN,  # Кения
    Country.CYP,  # Кипр
    Country.KGZ,  # Кыргызстан
    Country.KIR,  # Кирибати
    Country.TWN,  # Тайвань
    Country.PRK,  # КНДР
    Country.CHN,  # Китай
    Country.COL,  # Колумбия
    Country.COM,  # Коморы
    Country.CRI,  # Коста-Рика
    Country.CIV,  # Кот-д’Ивуар
    Country.CUB,  # Куба
    Country.KWT,  # Кувейт
    Country.CUW,  # Кюрасао
    Country.LAO,  # Лаос
    Country.LVA,  # Латвия
    Country.LSO,  # Лесото
    Country.LBR,  # Либерия
    Country.LBN,  # Ливан
    Country.LBY,  # Ливия
    Country.LTU,  # Литва
    Country.LIE,  # Лихтенштейн
    Country.LUX,  # Люксембург
    Country.MUS,  # Маврикий
    Country.MDG,  # Мадагаскар
    Country.MAC,  # Макао
    Country.MKD,  # Северная Македония
    Country.MWI,  # Малави
    Country.MYS,  # Малайзия
    Country.MLI,  # Мали
    Country.MDV,  # Мальдивы
    Country.MLT,  # Мальта
    Country.MAR,  # Марокко
    Country.MHL,  # Маршалловы Острова
    Country.MEX,  # Мексика
    Country.FSM,  # Микронезия
    Country.MOZ,  # Мозамбик
    Country.MDA,  # Молдова
    Country.MCO,  # Монако
    Country.MNG,  # Монголия
    Country.MSR,  # Монтсеррат
    Country.MMR,  # Мьянма
    Country.NAM,  # Намибия
    Country.NRU,  # Науру
    Country.NPL,  # Непал
    Country.NER,  # Нигер
    Country.NLD,  # Нидерланды
    Country.NIC,  # Никарагуа
    Country.NIU,  # Ниуэ
    Country.NZL,  # Новая Зеландия
    Country.NOR,  # Норвегия
    Country.ARE,  # ОАЭ
    Country.OMN,  # Оман
    Country.IMN,  # Остров Мэн
    Country.COK,  # Острова Кука
    Country.PAK,  # Пакистан
    Country.PLW,  # Палау
    Country.PSE,  # Государство Палестина
    Country.PAN,  # Панама
    Country.PNG,  # Папуа — Новая Гвинея
    Country.PRY,  # Парагвай
    Country.PER,  # Перу
    Country.POL,  # Польша
    Country.PRT,  # Португалия
    Country.KOR,  # Республика Корея
    Country.RUS,  # Россия
    Country.RWA,  # Руанда
    Country.ROU,  # Румыния
    Country.SLV,  # Сальвадор
    Country.WSM,  # Самоа
    Country.SMR,  # Сан-Марино
    Country.SAU,  # Саудовская Аравия
    Country.SYC,  # Сейшельские Острова
    Country.SEN,  # Сенегал
    Country.VCT,  # Сент-Винсент и Гренадины
    Country.KNA,  # Сент-Китс и Невис
    Country.LCA,  # Сент-Люсия
    Country.SRB,  # Сербия
    Country.SGP,  # Сингапур
    Country.SYR,  # Сирия
    Country.SVK,  # Словакия
    Country.SVN,  # Словения
    Country.SLB,  # Соломоновы Острова
    Country.SOM,  # Сомали
    Country.SDN,  # Судан
    Country.SUR,  # Суринам
    Country.USA,  # США
    Country.SLE,  # Сьерра-Леоне
    Country.TJK,  # Таджикистан
    Country.THA,  # Таиланд
    Country.TZA,  # Танзания
    Country.TCA,  # Теркс и Кайкос
    Country.TGO,  # Того
    Country.TON,  # Тонга
    Country.TTO,  # Тринидад и Тобаго
    Country.TUV,  # Тувалу
    Country.TUN,  # Тунис
    Country.TKM,  # Туркменистан
    Country.TUR,  # Турция
    Country.UGA,  # Уганда
    Country.UZB,  # Узбекистан
    Country.UKR,  # Украина
    Country.URY,  # Уругвай
    Country.FJI,  # Фиджи
    Country.PHL,  # Филиппины
    Country.FIN,  # Финляндия
    Country.FRA,  # Франция
    Country.HRV,  # Хорватия
    Country.MNE,  # Черногория
    Country.CZE,  # Чехия
    Country.CHL,  # Чили
    Country.CHE,  # Швейцария
    Country.SWE,  # Швеция
    Country.LKA,  # Шри-Ланка
    Country.ECU,  # Эквадор
    Country.GNQ,  # Экваториальная Гвинея
    Country.ERI,  # Эритрея
    Country.SWZ,  # Эсватини
    Country.EST,  # Эстония
    Country.ETH,  # Эфиопия
    Country.ZAF,  # ЮАР
    Country.JAM,  # Ямайка
    Country.JPN,  # Япония
]

COUNTRY_IND = [
    Country.AFG,  # AFGHANISTAN
    Country.ALB,  # ALBANIA
    Country.AND,  # ANDORRA
    Country.AGO,  # ANGOLA
    Country.AIA,  # ANGUILLA
    Country.ATG,  # ANTIGUA AND BARBUDA
    Country.ARG,  # ARGENTINA
    Country.ARM,  # ARMENIA
    Country.ABW,  # ARUBA
    Country.AUS,  # AUSTRALIA
    Country.AUT,  # AUSTRIA
    Country.AZE,  # AZERBAIJAN
    Country.BHS,  # BAHAMAS
    Country.BRB,  # BARBADOS
    Country.BLR,  # BELARUS
    Country.BEL,  # BELGIUM
    Country.BLZ,  # BELIZE
    Country.BEN,  # BENIN
    Country.BOL,  # BOLIVIA
    Country.BIH,  # BOSNIA AND HERZEGOVINA
    Country.BWA,  # BOTSWANA
    Country.BRA,  # BRAZIL
    Country.BRN,  # BRUNEI
    Country.BGR,  # BULGARIA
    Country.BDI,  # BURUNDI
    Country.KHM,  # CAMBODIA
    Country.CMR,  # CAMEROON
    Country.CAN,  # CANADA
    Country.CPV,  # CAPE VERDE
    Country.CYM,  # CAYMAN ISLANDS
    Country.CHL,  # CHILE
    Country.CHN,  # CHINA - CHINA
    Country.HKG,  # CHINA - SAR HONGKONG
    Country.MAC,  # CHINA - SAR MACAU
    Country.COL,  # COLOMBIA
    Country.COM,  # COMOROS
    Country.COK,  # COOK ISLANDS
    Country.CRI,  # COSTA RICA
    Country.CIV,  # COTE D\'IVOIRE
    Country.HRV,  # CROATIA
    Country.CUB,  # CUBA
    Country.CYP,  # CYPRUS
    Country.CZE,  # CZECH REPUBLIC
    Country.DNK,  # DENMARK
    Country.DJI,  # DJIBOUTI
    Country.DMA,  # DOMINICA
    Country.DOM,  # DOMINICAN REPUBLIC
    Country.TLS,  # EAST TIMOR (DEMOCRATIC REPUBLIC OF)
    Country.ECU,  # ECUADOR
    Country.SLV,  # EL SALVADOR
    Country.GNQ,  # EQUATORIAL GUINEA
    Country.ERI,  # ERITREA
    Country.EST,  # ESTONIA
    Country.SWZ,  # ESWATINI
    Country.FJI,  # FIJI
    Country.FIN,  # FINLAND
    Country.FRA,  # FRANCE
    Country.GAB,  # GABON
    Country.GMB,  # GAMBIA
    Country.GEO,  # GEORGIA
    Country.DEU,  # GERMANY
    Country.GHA,  # GHANA
    Country.GIB,  # GIBRALTAR
    Country.GRC,  # GREECE
    Country.GRD,  # GRENADA
    Country.GTM,  # GUATEMALA
    Country.GGY,  # GUERNSEY
    Country.GIN,  # GUINEA
    Country.GUY,  # GUYANA
    Country.HTI,  # HAITI
    Country.HND,  # HONDURAS
    Country.HUN,  # HUNGARY
    Country.ISL,  # ICELAND
    Country.IDN,  # INDONESIA
    Country.IRL,  # IRELAND
    Country.IMN,  # ISLE OF MAN
    Country.ISR,  # ISRAEL
    Country.ITA,  # ITALY
    Country.JAM,  # JAMAICA
    Country.JPN,  # JAPAN
    Country.JEY,  # JERSEY
    Country.JOR,  # JORDAN
    Country.KAZ,  # KAZAKHSTAN
    Country.KEN,  # KENYA
    Country.KIR,  # KIRIBATI
    Country.KGZ,  # KYRGYZSTAN
    Country.LAO,  # LAOS
    Country.LVA,  # LATVIA
    Country.LSO,  # LESOTHO
    Country.LBR,  # LIBERIA
    Country.LIE,  # LIECHTENSTEIN
    Country.LTU,  # LITHUANIA
    Country.LUX,  # LUXEMBOURG
    Country.MDG,  # MADAGASCAR
    Country.MWI,  # MALAWI
    Country.MYS,  # MALAYSIA
    Country.MLI,  # MALI
    Country.MLT,  # MALTA
    Country.MHL,  # MARSHALL ISLANDS
    Country.MUS,  # MAURITIUS
    Country.MEX,  # MEXICO
    Country.FSM,  # MICRONESIA (FEDERATED STATES OF)
    Country.MDA,  # MOLDOVA
    Country.MCO,  # MONACO
    Country.MNG,  # MONGOLIA
    Country.MNE,  # MONTENEGRO
    Country.MSR,  # MONTSERRAT
    Country.MAR,  # MOROCCO
    Country.MOZ,  # MOZAMBIQUE
    Country.MMR,  # MYANMAR
    Country.NAM,  # NAMIBIA
    Country.NRU,  # NAURU
    Country.NLD,  # NETHERLANDS
    Country.NZL,  # NEW ZEALAND
    Country.NIC,  # NICARAGUA
    Country.NER,  # NIGER
    Country.NIU,  # NIUE ISLAND
    Country.NOR,  # NORWAY
    Country.OMN,  # OMAN
    Country.PLW,  # PALAU
    Country.PSE,  # PALESTINE
    Country.PAN,  # PANAMA
    Country.PNG,  # PAPUA NEW GUINEA
    Country.PRY,  # PARAGUAY
    Country.PER,  # PERU
    Country.PHL,  # PHILIPPINES
    Country.POL,  # POLAND
    Country.PRT,  # PORTUGAL
    Country.KOR,  # REPUBLIC OF KOREA
    Country.MKD,  # REPUBLIC OF NORTH MACEDONIA
    Country.ROU,  # ROMANIA
    Country.RUS,  # RUSSIAN FEDERATION
    Country.RWA,  # RWANDA
    Country.KNA,  # SAINT KITTS AND NEVIS
    Country.LCA,  # SAINT LUCIA
    Country.VCT,  # SAINT VINCENT AND THE GRENADINES
    Country.SMR,  # SAN MARINO
    Country.SAU,  # SAUDI ARABIA
    Country.SEN,  # SENEGAL
    Country.SRB,  # SERBIA
    Country.SYC,  # SEYCHELLES
    Country.SLE,  # SIERRA LEONE
    Country.SGP,  # SINGAPORE
    Country.SVK,  # SLOVAKIA
    Country.SVN,  # SLOVENIA
    Country.SLB,  # SOLOMON ISLANDS
    Country.ZAF,  # SOUTH AFRICA
    Country.ESP,  # SPAIN
    Country.LKA,  # SRI LANKA
    Country.SUR,  # SURINAME
    Country.SWE,  # SWEDEN
    Country.CHE,  # SWITZERLAND
    Country.TWN,  # TAIWAN
    Country.TJK,  # TAJIKISTAN
    Country.TZA,  # TANZANIA
    Country.THA,  # THAILAND
    Country.TGO,  # TOGO
    Country.TON,  # TONGA
    Country.TTO,  # TRINIDAD AND TOBAGO
    Country.TCA,  # TURKS AND CAICOS ISLANDS
    Country.TUV,  # TUVALU
    Country.UGA,  # UGANDA
    Country.UKR,  # UKRAINE
    Country.ARE,  # UNITED ARAB EMIRATES
    Country.GBR,  # UNITED KINGDOM
    Country.USA,  # UNITED STATES OF AMERICA
    Country.URY,  # URUGUAY
    Country.UZB,  # UZBEKISTAN
    Country.VUT,  # VANUATU
    Country.VAT,  # VATICAN CITY STATE (HOLY SEE)
    Country.VEN,  # VENEZUELA
    Country.VNM,  # VIETNAM
    Country.WSM,  # WEST SAMOA
    Country.ZMB,  # ZAMBIA
    Country.ZWE,  # ZIMBABWE
]

COUNTRY_SAARC = [Country.AFG,
                 Country.BTN,
                 Country.PAK,
                 Country.MDV,
                 Country.BGD,
                 Country.LKA,
                 Country.NPL]


# ISO 3166-2
COUNTRY_OUTPUT = {
    Country.AUS: "Австралия",
    Country.AUT: "Австрия",
    Country.AZE: "Азербайджан",
    Country.ALA: "Аландские острова",
    Country.ALB: "Албания",
    Country.DZA: "Алжир",
    Country.VIR: "Виргинские Острова (США)",
    Country.ASM: "Американское Самоа",
    Country.AIA: "Ангилья",
    Country.AGO: "Ангола",
    Country.AND: "Андорра",
    Country.ATA: "Антарктика",
    Country.ATG: "Антигуа и Барбуда",
    Country.ARG: "Аргентина",
    Country.ARM: "Армения",
    Country.ABW: "Аруба",
    Country.AFG: "Афганистан",
    Country.BHS: "Багамские Острова",
    Country.BGD: "Бангладеш",
    Country.BRB: "Барбадос",
    Country.BHR: "Бахрейн",
    Country.BLZ: "Белиз",
    Country.BLR: "Беларусь",
    Country.BEL: "Бельгия",
    Country.BEN: "Бенин",
    Country.BMU: "Бермуды",
    Country.BGR: "Болгария",
    Country.BOL: "Боливия",
    Country.BES: "Бонайре, Синт-Эстатиус и Саба",
    Country.BIH: "Босния и Герцеговина",
    Country.BWA: "Ботсвана",
    Country.BRA: "Бразилия",
    Country.IOT: "Британская Территория в Индийском Океане",
    Country.VGB: "Виргинские Острова (Великобритания)",
    Country.BRN: "Бруней",
    Country.BFA: "Буркина-Фасо",
    Country.BDI: "Бурунди",
    Country.BTN: "Бутан",
    Country.VUT: "Вануату",
    Country.VAT: "Ватикан",
    Country.GBR: "Великобритания",
    Country.HUN: "Венгрия",
    Country.VEN: "Венесуэла",
    Country.UMI: "Внешние малые острова США",
    Country.TLS: "Восточный Тимор",
    Country.VNM: "Вьетнам",
    Country.GAB: "Габон",
    Country.HTI: "Гаити",
    Country.GUY: "Гайана",
    Country.GMB: "Гамбия",
    Country.GHA: "Гана",
    Country.GLP: "Гваделупа",
    Country.GTM: "Гватемала",
    Country.GUF: "Гвиана",
    Country.GIN: "Гвинея",
    Country.GNB: "Гвинея-Бисау",
    Country.DEU: "Германия",
    Country.GGY: "Гернси",
    Country.GIB: "Гибралтар",
    Country.HND: "Гондурас",
    Country.HKG: "Гонконг",
    Country.GRD: "Гренада",
    Country.GRL: "Гренландия",
    Country.GRC: "Греция",
    Country.GEO: "Грузия",
    Country.GUM: "Гуам",
    Country.DNK: "Дания",
    Country.JEY: "Джерси",
    Country.DJI: "Джибути",
    Country.DMA: "Доминика",
    Country.DOM: "Доминиканская Республика",
    Country.COD: "ДР Конго",
    Country.EGY: "Египет",
    Country.ZMB: "Замбия",
    Country.ESH: "САДР",
    Country.ZWE: "Зимбабве",
    Country.ISR: "Израиль",
    Country.IND: "Индия",
    Country.IDN: "Индонезия",
    Country.JOR: "Иордания",
    Country.IRQ: "Ирак",
    Country.IRN: "Иран",
    Country.IRL: "Ирландия",
    Country.ISL: "Исландия",
    Country.ESP: "Испания",
    Country.ITA: "Италия",
    Country.YEM: "Йемен",
    Country.CPV: "Кабо-Верде",
    Country.KAZ: "Казахстан",
    Country.CYM: "Острова Кайман",
    Country.KHM: "Камбоджа",
    Country.CMR: "Камерун",
    Country.CAN: "Канада",
    Country.QAT: "Катар",
    Country.KEN: "Кения",
    Country.CYP: "Кипр",
    Country.KGZ: "Кыргызстан",
    Country.KIR: "Кирибати",
    Country.TWN: "Тайвань",
    Country.PRK: "КНДР",
    Country.CHN: "Китай",
    Country.CCK: "Кокосовые острова",
    Country.COL: "Колумбия",
    Country.COM: "Коморы",
    Country.CRI: "Коста-Рика",
    Country.CIV: "Кот-д’Ивуар",
    Country.CUB: "Куба",
    Country.KWT: "Кувейт",
    Country.CUW: "Кюрасао",
    Country.LAO: "Лаос",
    Country.LVA: "Латвия",
    Country.LSO: "Лесото",
    Country.LBR: "Либерия",
    Country.LBN: "Ливан",
    Country.LBY: "Ливия",
    Country.LTU: "Литва",
    Country.LIE: "Лихтенштейн",
    Country.LUX: "Люксембург",
    Country.MUS: "Маврикий",
    Country.MRT: "Мавритания",
    Country.MDG: "Мадагаскар",
    Country.MYT: "Майотта",
    Country.MAC: "Макао",
    Country.MKD: "Северная Македония",
    Country.MWI: "Малави",
    Country.MYS: "Малайзия",
    Country.MLI: "Мали",
    Country.MDV: "Мальдивы",
    Country.MLT: "Мальта",
    Country.MAR: "Марокко",
    Country.MTQ: "Мартиника",
    Country.MHL: "Маршалловы Острова",
    Country.MEX: "Мексика",
    Country.FSM: "Микронезия",
    Country.MOZ: "Мозамбик",
    Country.MDA: "Молдова",
    Country.MCO: "Монако",
    Country.MNG: "Монголия",
    Country.MSR: "Монтсеррат",
    Country.MMR: "Мьянма",
    Country.NAM: "Намибия",
    Country.NRU: "Науру",
    Country.NPL: "Непал",
    Country.NER: "Нигер",
    Country.NGA: "Нигерия",
    Country.NLD: "Нидерланды",
    Country.NIC: "Никарагуа",
    Country.NIU: "Ниуэ",
    Country.NZL: "Новая Зеландия",
    Country.NCL: "Новая Каледония",
    Country.NOR: "Норвегия",
    Country.ARE: "ОАЭ",
    Country.OMN: "Оман",
    Country.BVT: "Остров Буве",
    Country.IMN: "Остров Мэн",
    Country.COK: "Острова Кука",
    Country.NFK: "Остров Норфолк",
    Country.CXR: "Остров Рождества",
    Country.PCN: "Острова Питкэрн",
    Country.SHN: "Остров Святой Елены",
    Country.PAK: "Пакистан",
    Country.PLW: "Палау",
    Country.PSE: "Государство Палестина",
    Country.PAN: "Панама",
    Country.PNG: "Папуа — Новая Гвинея",
    Country.PRY: "Парагвай",
    Country.PER: "Перу",
    Country.POL: "Польша",
    Country.PRT: "Португалия",
    Country.PRI: "Пуэрто-Рико",
    Country.COG: "Республика Конго",
    Country.KOR: "Республика Корея",
    Country.REU: "Реюньон",
    Country.RUS: "Россия",
    Country.RWA: "Руанда",
    Country.ROU: "Румыния",
    Country.SLV: "Сальвадор",
    Country.WSM: "Самоа",
    Country.SMR: "Сан-Марино",
    Country.STP: "Сан-Томе и Принсипи",
    Country.SAU: "Саудовская Аравия",
    Country.MNP: "Северные Марианские Острова",
    Country.SYC: "Сейшельские Острова",
    Country.BLM: "Сен-Бартелеми",
    Country.MAF: "Сен-Мартен",
    Country.SPM: "Сен-Пьер и Микелон",
    Country.SEN: "Сенегал",
    Country.VCT: "Сент-Винсент и Гренадины",
    Country.KNA: "Сент-Китс и Невис",
    Country.LCA: "Сент-Люсия",
    Country.SRB: "Сербия",
    Country.SGP: "Сингапур",
    Country.SXM: "Синт-Мартен",
    Country.SYR: "Сирия",
    Country.SVK: "Словакия",
    Country.SVN: "Словения",
    Country.SLB: "Соломоновы Острова",
    Country.SOM: "Сомали",
    Country.SDN: "Судан",
    Country.SUR: "Суринам",
    Country.USA: "США",
    Country.SLE: "Сьерра-Леоне",
    Country.TJK: "Таджикистан",
    Country.THA: "Таиланд",
    Country.TZA: "Танзания",
    Country.TCA: "Теркс и Кайкос",
    Country.TGO: "Того",
    Country.TKL: "Токелау",
    Country.TON: "Тонга",
    Country.TTO: "Тринидад и Тобаго",
    Country.TUV: "Тувалу",
    Country.TUN: "Тунис",
    Country.TKM: "Туркменистан",
    Country.TUR: "Турция",
    Country.UGA: "Уганда",
    Country.UZB: "Узбекистан",
    Country.UKR: "Украина",
    Country.WLF: "Уоллис и Футуна",
    Country.URY: "Уругвай",
    Country.FRO: "Фарерские острова",
    Country.FJI: "Фиджи",
    Country.PHL: "Филиппины",
    Country.FIN: "Финляндия",
    Country.FLK: "Фолклендские острова",
    Country.FRA: "Франция",
    Country.PYF: "Французская Полинезия",
    Country.ATF: "Французские Южные и Антарктические территории",
    Country.HMD: "Херд и Макдональд",
    Country.HRV: "Хорватия",
    Country.CAF: "ЦАР",
    Country.TCD: "Чад",
    Country.MNE: "Черногория",
    Country.CZE: "Чехия",
    Country.CHL: "Чили",
    Country.CHE: "Швейцария",
    Country.SWE: "Швеция",
    Country.SJM: "Флаг Шпицбергена и Ян-Майена Шпицберген и Ян-Майен",
    Country.LKA: "Шри-Ланка",
    Country.ECU: "Эквадор",
    Country.GNQ: "Экваториальная Гвинея",
    Country.ERI: "Эритрея",
    Country.SWZ: "Эсватини",
    Country.EST: "Эстония",
    Country.ETH: "Эфиопия",
    Country.ZAF: "ЮАР",
    Country.SGS: "Южная Георгия и Южные Сандвичевы Острова",
    Country.SSD: "Южный Судан",
    Country.JAM: "Ямайка",
    Country.JPN: "Япония",
}
