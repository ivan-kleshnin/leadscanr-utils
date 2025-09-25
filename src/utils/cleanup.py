import emoji
import re
import regex

SPACES = re.compile(r"[ \u00A0]+")
NEWLINES = re.compile(r"\n{3,}")
NL_SPACES_NL = re.compile(r" ?\n ?")

def clean_text(text: str) -> str:
    """
    1. Replace all emojis with spaces.
    2. Remove spaces around newlines.
    3. Collapse 2+ spaces into 1 space.
    4. Collapse 3+ newlines into 2 newlines.
    5. Strip leading/trailing spaces.
    """
    if not text:
        return ""
    text = clean_emojis(text)
    text = SPACES.sub(" ", text)
    text = NL_SPACES_NL.sub("\n", text)
    text = NEWLINES.sub(r"\n\n", text)
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
        stripped = line.lstrip()
        if not stripped:
            result_lines.append("")
            continue
        if starts_with_emoji_cluster(stripped):
            content = emoji.replace_emoji(stripped, "").strip()
            if content:
                line = "- " + content
            else:
                line = ""
        else:
            line = emoji.replace_emoji(stripped, " ").strip()
        result_lines.append(line)
    return "\n".join(result_lines)
