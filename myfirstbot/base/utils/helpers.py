def esc_spec_chars(string: str, spec_chars: tuple[str, ...] = ("%", "_")) -> str:
    return "".join([f"\\{c}" if c in spec_chars else c for c in string])