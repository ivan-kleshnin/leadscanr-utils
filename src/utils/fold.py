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
    (?:от\s+)?              # optional 'от ' at the start
    (\d+)                   # first integer number
    (?:                     # optional range separator
        \s*(?:[-–—~]|до)\s* # separator: -, –, —, ~ or 'до'
        (\d+)               # second integer number
    )?
    \s*                     # optional spaces
    тыс(?:ячи?|\.|\b)       # 'тыс', 'тысячи', 'тыс.' or boundary
    """

    def replacer(match) -> str:
        num1_str = match.group(1)
        num2_str = match.group(2)
        num1 = int(float(num1_str.replace(',', '.')) * 1000)
        if num2_str:
            num2 = int(float(num2_str.replace(',', '.')) * 1000)
            return f"{num1}–{num2}"
        else:
            return str(num1)

    return re.sub(pattern, replacer, text, flags=re.IGNORECASE | re.VERBOSE)

def fold_currencies(text: str) -> str:
    # capture integer then currency, unified approach and verbose regexes
    text = re.sub(
        r"""
        (\d+)                             # integer number
        \s*                               # optional space
        (?:р|руб|рублей|rub)\.?           # р, руб, рублей, rub + optional dot
        (?=\W|$)                          # followed by non-word or end
        """,
        r"\1 ₽",
        text,
        flags=re.IGNORECASE | re.VERBOSE,
    )
    return text
