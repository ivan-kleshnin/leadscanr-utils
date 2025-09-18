import re
import demoji

SPACES = re.compile(r"[ \u00A0]+")
NEWLINES = re.compile(r"\n{3,}")
NL_SPACES_NL = re.compile(r" +\n|n +")

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
    text = demoji.replace(text, " ")
    text = SPACES.sub(" ", text)
    text = NL_SPACES_NL.sub("\n", text)
    text = NEWLINES.sub(r"\n\n", text)
    text = text.strip()
    return text
