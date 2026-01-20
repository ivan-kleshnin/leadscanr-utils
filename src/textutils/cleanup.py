import unicodedata
import re
import regex

ALNUM = re.compile(r"[а-яa-z0-9]", flags=re.IGNORECASE)
NBRSPACE = re.compile(r"\u00A0+")
MDASH = re.compile(r"—")
INIT_SPACE = re.compile(r"^[ \t]{3,}", flags=re.MULTILINE)
TRAIL_SPACE = re.compile(r"[ \t]+$", flags=re.MULTILINE)
INTRA_SPACE = re.compile(r"(?<=\S)[ \t]{2,}(?=\S)", flags=re.MULTILINE)
NEWLINES = re.compile(r"\n{3,}")
BULLET = re.compile(r"^\s+[-–◦•·*+](?=[\s\w])", flags=re.MULTILINE)
ASTERISKS = re.compile(r"(?:\*{2,}|={2,}|-{2,}|_{2,})", flags=re.VERBOSE)

def normalize_whitespace(text: str) -> str:
    """
    1. Denoise emojis
    2. Replace NBR space with normal space
    3. Denoise decorators and whitespace
    4. Collapse 3+ newlines into 2 newlines
    5. Strip text-level leading/trailing spaces
    """
    if not text.strip(" \t\n\r\f\v-–,./;'[]{}()_=+!@#$%^&*~\\"):
        return ""
    text = INIT_SPACE.sub("  ", text)
    text = INTRA_SPACE.sub(" ", text)
    text = TRAIL_SPACE.sub("", text)
    text = NEWLINES.sub("\n\n", text)
    text = "\n".join(
        line.rstrip() for line in text.splitlines()
    )
    return text.strip(" \t\n\r\f\v-–=*")

def is_symbol_like(cluster: str) -> bool:
    if len(cluster) > 1:
        # Is a multi-codepoint cluster
        # (note: this check will trigger on Vietnamese, etc, more intelligent solution TBD)
        return True
    if unicodedata.category(cluster) in {"So", "Sm", "Sc", "Sk"}:
        # Is a single-codepoint cluster from a "symbol-like" category
        return True
    return False

def get_leading_cluster(text: str) -> str | None:
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
        return None
    m = regex.match(r"\X", stripped) # captures a grapheme (one or more "codepoints")
    if not m:
        return None
    cluster = m.group(0)
    if is_symbol_like(cluster):
        return cluster
    return None

def normalize_leading_emojis(text: str) -> str:
    in_lines = text.splitlines()
    leading_clusters: list[str | None] = [
        get_leading_cluster(line) for line in in_lines
    ]
    out_lines: list[str] = []
    for i, line in enumerate(in_lines):
        leading_cluster = leading_clusters[i]
        if not leading_cluster:
            # No leading emoji, nothing to do
            out_lines.append(line)
            continue
        line = line.strip()
        # print(">>>", repr(line))
        prev_same = i > 0 and leading_clusters[i - 1] == leading_cluster
        next_same = i < len(in_lines) - 1 and leading_clusters[i + 1] == leading_cluster
        content = line.lstrip()[len(leading_cluster):]
        if prev_same or next_same:
            # Bullet-like emoji, replace with hyphen
            out_lines.append(f"- {content.rstrip()}" if content.rstrip() else "")
        else:
            # Other emoji, drop it
            out_lines.append(content.strip())
    return "\n".join(out_lines)

def clean_unicode(text: str) -> str:
    text = normalize_leading_emojis(text)
    text = regex.sub(r"\X", lambda m: " " if is_symbol_like(m.group(0)) else m.group(0), text)
    return text

def denoise(text: str) -> str:
    """
    Unify local mess so other algorithms can be simplified
    """
    # Handle Unicode
    text = clean_unicode(text)
    # Normalize linebreaks
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Replace NBRSPACE with normal space
    text = NBRSPACE.sub(" ", text)
    # Replace MDASH with normal NDASH
    text = MDASH.sub("–", text)
    # Replace common decorative chars
    text = ASTERISKS.sub("", text)
    # Remove zero-width "non-joiner" and zero-width "joiner"
    text = re.sub(r"[\u200C\u200D]", "", text)
    # Replace zero-width spaces with normal ones
    text = re.compile(r"[\u200B]").sub(" ", text)
    # Replace zero-width linebreaks with normal ones
    text = re.compile(r"[\u2028\u2029]").sub("\n", text)
    # Unify bullets
    text = BULLET.sub("-", text)
    return text
