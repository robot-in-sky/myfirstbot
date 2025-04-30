from core.services.utils.translate import format_address, format_ind_places, format_place_name, translit


def format_value(value: str, formatter: str | None = None) -> str:
    match formatter:
        case "text_ru":
            return translit(value)
        case "address_ru":
            return format_address(value)
        case "place_ru":
            return format_place_name(value)
        case "places_ind":
            return format_ind_places(value)
    return value
