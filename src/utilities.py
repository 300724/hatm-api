def calculate_pages(x: int) -> tuple[int]:
    return x * 20 + 1, (x + 1) * 20


def juz_name(x: int) -> str:
    return f"Juz {x + 1}" if x < 30 else "Du'a"
