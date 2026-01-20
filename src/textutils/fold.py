import re

def fold_shortcuts(text: str) -> str:
    text = re.sub(
        r"""
        (\d+)     # integer number
        \s*       # optional space
        тр\.?     # 'тр.'
        (?=\W|$)  # followed by non-word or end
        """,
        r"\1 тыс. ₽",
        text,
        flags=re.IGNORECASE | re.VERBOSE,
    )
    return text

def fold_numbers(text: str) -> str:
    pattern = r"\b\d{1,3}(?:[.,`' ]\d{3})+\b"
    text = re.sub(pattern, lambda m: "".join(c for c in m.group(0) if c.isdigit()), text)
    text = re.sub(r"(?<=00)\s+[-–]\s+(?=\d)", "–", text)
    return text

def fold_scale_units(text: str) -> str:
    pattern = r"""
    (\d+(?:[.,]\d+)?)       # first number
    (?:
        \s*(?:[-–—~]|до)\s* # optional range separator
        (\d+(?:[.,]\d+)?)   # second number
    )?
    \s*                     # optional spaces
    тыс(?:ячи?|\.|\b)       # 'тыс', 'тысячи', 'тыс.' or boundary
    """

    def replacer(match: re.Match) -> str:
        num1 = float(match.group(1).replace(',', '.')) * 1000
        num2 = match.group(2)
        if num2:
            num2 = float(num2.replace(',', '.')) * 1000
            return f"{int(num1)}–{int(num2)}"
        return str(int(num1))

    return re.sub(pattern, replacer, text, flags=re.IGNORECASE | re.VERBOSE)

def fold_currencies(text: str) -> str:
    # capture integer then currency, unified approach and verbose regexes
    text = re.sub(
        r"""
        (\d+)                             # integer number
        \s*                               # optional space
        (?:рублей|руб|р|rub)\.?           # р, руб, рублей, rub + optional dot
        (?=\W|$)                          # followed by non-word or end
        """,
        r"\1 ₽",
        text,
        flags=re.IGNORECASE | re.VERBOSE,
    )
    return text
