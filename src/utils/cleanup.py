import emoji
import re
import regex

ALNUM = re.compile(r"[а-яa-z0-9]", flags=re.IGNORECASE)
NBRSPACE = re.compile(r"\u00A0+")
MDASH = re.compile(r"—")
INIT_SPACE = re.compile(r"^[ \t]{3,}", flags=re.MULTILINE)
TRAIL_SPACE = re.compile(r"[ \t]+$", flags=re.MULTILINE)
INTRA_SPACE = re.compile(r"(?<=\S)[ \t]{2,}(?=\S)", flags=re.MULTILINE)
NEWLINES = re.compile(r"\n{3,}")
BULLET = re.compile(r"^[-–◦•·*+][ \t]+", flags=re.MULTILINE)
ASTERISKS = re.compile(r"(?:\*{2,}|={2,}|-{2,}|_{2,})", flags=re.VERBOSE)

def denoise(text: str) -> str:
    # 1. Replace NBRSPACE with normal space
    text = NBRSPACE.sub(" ", text)
    # 2. Replace MDASH with normal NDASH
    text = MDASH.sub("–", text)
    # 3. Replace common decorative chars
    text = ASTERISKS.sub("", text)
    # 4. Unify bullets
    text = BULLET.sub("- ", text)
    # 5. Unify secondary whitespace cases
    text = re.sub(r"(?<=\d)р\b", " р", text)
    text = re.sub(r"(?<=\d)(₽|\$|€)", r" \1", text)
    text = re.sub(r"(?<=\d)м2\b", " м2", text)
    # 6. Collapse common "от NUM до NUM" cases
    text = re.sub(r"\bот\s+(\d+)\d\s+до\s+(\d+)", r"\1–\2", text, flags=re.IGNORECASE)
    # 7. Drop empty lines and rtrim the rest
    lines = text.splitlines()
    return "\n".join(
        line.rstrip() if ALNUM.search(line) else ""
        for line in lines
    )

def normalize_whitespace(text: str) -> str:
    """
    1. Denoise emojis
    2. Replace NBR space with normal space
    3. Denoise decorators and whitespace
    4. Collapse 3+ newlines into 2 newlines
    5. Strip text-level leading/trailing spaces
    """
    if not text.strip():
        return ""
    text = INIT_SPACE.sub("  ", text)
    text = INTRA_SPACE.sub(" ", text)
    text = TRAIL_SPACE.sub("", text)
    text = NEWLINES.sub("\n\n", text)
    text = text.strip(" \t\n\r\f\v-–")
    return text

def starts_with_emoji_cluster(text: str) -> bool:
    """
    Checks if the first grapheme cluster contains at least one emoji.
    💻 → 1 codepoint, 1 grapheme cluster
    ⚡️ → 2 codepoints (⚡ + variation selector 16), 1 grapheme cluster
    👩‍💻 → 3 codepoints (👩 + ZWJ + 💻), 1 grapheme cluster
    á  → 2 codepoints (a + combining accent), 1 grapheme cluster
    grapheme cluster
    codepoint ~= character
    """
    stripped = text.lstrip()
    if not stripped:
        return False
    m = regex.match(r"\X", stripped) # captures a grapheme (one or more "codepoints")
    if not m:
        return False
    cluster = m.group(0)
    return (
        emoji.is_emoji(cluster) or
        any(emoji.is_emoji(codepoint) for codepoint in cluster) # iterates over "codepoints"
    )

def clean_emojis(text: str) -> str:
    result_lines = []
    for line in text.splitlines():
        lline = line.lstrip()
        if starts_with_emoji_cluster(lline):
            content = emoji.replace_emoji(lline, "")
            if content:
                line = "- " + content
            else:
                line = ""
        else:
            line = emoji.replace_emoji(line, " ")
        result_lines.append(line)
    return "\n".join(result_lines)
