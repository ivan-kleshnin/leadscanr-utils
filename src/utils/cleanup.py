import re
import regex
import demoji

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
    m = regex.match(r"\X", text) # Match first grapheme cluster
    if not m:
        return False
    cluster = m.group(0)
    return bool(demoji.findall(cluster))

def clean_emojis(text: str) -> str:
    result_lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped and starts_with_emoji_cluster(stripped):
            content = demoji.replace(stripped, "").strip()
            if content:  # only add bullet if text remains
                line = "- " + content
            else:
                line = ""  # skip empty/decorative line
        else:
            line = demoji.replace(stripped, " ").strip()
        result_lines.append(line)
    return "\n".join(result_lines)
