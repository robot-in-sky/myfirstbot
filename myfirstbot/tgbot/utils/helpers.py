def cut_string(string: str, limit: int = 10) -> str:
    if 1 < limit < len(string):
        return f"{string[:limit-1]}…"
    return string
