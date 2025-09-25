import emoji
import re
import regex

NBRSPACE = re.compile(r"\u00A0+")
NEWLINES = re.compile(r"\n{3,}")
ALNUM = re.compile(r"\w")
WHITESPACE_SPLIT = re.compile(r"(\s+)")
WHITESPACE_LEADING = re.compile(r"^[ \t]+", flags=re.MULTILINE)
TOKEN_KEEP = re.compile(r"[\w\[\](){}#]")
SYMBOL_REPLACEMENTS = [
    ("_", "__"),
    ("*", "**"),
    ("=", "=="),
    ("-", "--")
]

def denoise(text: str) -> str:
    """
    Cleans decorative sequences (*, =, -) while preserving formatting:
    - Converts ***word*** → **word**
    - Converts ===word=== → ==word==
    - Converts ---word--- → --word--
    - Removes decoration-only tokens
    - Removes trailing whitespace (leading whitespace is semantic)
    - Collapses internal whitespace (between tokens)
    - Drops lines without alphanumeric characters
    """
    def clean_token(token: str) -> str:
        if TOKEN_KEEP.search(token):
            for symbol, replacement in SYMBOL_REPLACEMENTS:
                esc = re.escape(symbol)
                token = re.sub(fr"^{esc}{{3,}}", replacement, token)
                token = re.sub(fr"{esc}{{3,}}$", replacement, token)
        else:
            token = re.sub(r"[*=\-]+", "", token)
        return token

    def clean_line(line: str) -> str:
        # Capture leading spaces
        m = re.match(r"^(\s*)", line)
        leading = m.group(0) if m else ""
        # Split into tokens, collapse internal spaces
        tokens = WHITESPACE_SPLIT.split(line.lstrip())
        cleaned = " ".join(clean_token(t) for t in tokens if not t.isspace())
        return leading + cleaned.rstrip() if ALNUM.search(cleaned) else ""

    return "\n".join(clean_line(line) for line in text.splitlines())

def clean_text(text: str) -> str:
    """
    1. Replace leading emojis with "- " and other emojis with " "
    2. Denoise text
    3. Collapse 3+ newlines into 2 newlines
    4. Normalize leading whitespace to 2 spaces
    5. Strip text-level leading/trailing spaces
    """
    if not text.strip():
        return ""
    text = NBRSPACE.sub(" ", text)
    text = clean_emojis(text)
    text = denoise(text)
    text = NEWLINES.sub(r"\n\n", text)
    text = WHITESPACE_LEADING.sub("  ", text)
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
    return any(emoji.is_emoji(codepoint) for codepoint in cluster) # iterates over "codepoints"

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
