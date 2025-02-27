import re
from typing import Any


def cut_string(string: str, limit: int = 10) -> str:
    if 1 < limit < len(string):
        return f"{string[:limit-1]}…"
    return string


def remove_emojis(string: str) -> str:
    pattern = re.compile(
        pattern="["
            u"\U0001F600-\U0001F64F"  # emoticons  # noqa: UP025
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs  # noqa: UP025
            u"\U0001F680-\U0001F6FF"  # transport & map symbols  # noqa: UP025
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)  # noqa: UP025
            "]+",
        flags=re.UNICODE,
    )
    return pattern.sub(r"", string)


def sub_dict_by_prefix(data: dict[str, Any], prefix: str) -> dict[str, Any]:
    return {k.replace(prefix, "", 1): v for k, v in data.items() if k.startswith(prefix)}


def remove_keys_by_prefix(data: dict[str, Any], prefix: str) -> dict[str, Any]:
    return {k: v for k, v in data.items() if not k.startswith(prefix)}


def get_key_by_value(mapping: dict[Any, Any], value: str, default: str | None = None) -> Any:
    try:
        return next(filter(lambda i: i[1] == value, mapping.items()))[0]
    except StopIteration:
        return default
