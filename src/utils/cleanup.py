import emoji
import re
import regex

ALNUM = re.compile(r"\w")
NBRSPACE = re.compile(r"\u00A0+")
WHITESPACES = re.compile(r"[ \t]{3,}")
INTRA_SPACE = re.compile(r"(?<=\S)[ \t]{2,}(?=\S)")
NEWLINES = re.compile(r"\n{3,}")
SYMBOL_REPLACEMENTS = [
    # ("_", "__"),
    ("*", "**"),
    ("=", "=="),
    ("-", "--")
]

def denoise(text: str) -> str:
    """
    1. Collapse repeated decorative sequences (-- --, ** **, == ==) into their double form
    2. Collapse 3+ symbols to their double form
    3. Remove trailing whitespace (leading is preserved)
    4. Collapse internal whitespace between tokens to single space
    5. Unify leading whitespace to 2 spaces
    """
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        if ALNUM.search(line):
            for symbol, replacement in SYMBOL_REPLACEMENTS:
                line = re.sub(rf"{re.escape(symbol)}{{3,}}", replacement, line)
            clean_lines.append(line.rstrip())
        else:
            clean_lines.append("")
    return "\n".join(clean_lines)

def clean_text(text: str) -> str:
    """
    1. Denoise emojis
    2. Replace NBR space with normal space
    3. Denoise decorators and whitespace
    4. Collapse 3+ newlines into 2 newlines
    5. Strip text-level leading/trailing spaces
    """
    if not text.strip():
        return ""
    text = clean_emojis(text)
    text = NBRSPACE.sub(" ", text)
    text = denoise(text)
    text = WHITESPACES.sub("  ", text)
    text = INTRA_SPACE.sub(" ", text)
    text = NEWLINES.sub("\n\n", text)
    text = text.strip()
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
