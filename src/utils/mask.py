import re

URL = re.compile(r"(https?://\S+|www\.\S+)", flags=re.IGNORECASE)
EMAIL = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", flags=re.IGNORECASE)
MENTION = re.compile(r"@[A-Za-z0-9_]+")
PHONE = re.compile(
    r"""
    (?<![\d\w])                 # Negative lookbehind to prevent partial matches
    (?:                         # Non-capturing group for the whole number
      \+?\d{1,3}                # Optional country code (+7)
      (?:[\s.-]?\(?\d{2,4}\)?[\s.-]?) # Optional area code
      \d{2,4}                   # First part of the main number
      (?:[\s.-]?\d{2,3}){2,4}   # Flexible, repeated groups of digits
    )
    (?![\d\w])                  # Negative lookahead to prevent partial matches
    """,
    flags=re.VERBOSE | re.IGNORECASE,
)

def mask_contacts(text: str) -> str:
    """
    Replace contact info in text with placeholders for LLM performance and security:
    - URL -> [URL]
    - Email -> [EMAIL]
    - @mention -> [MENTION]
    - Phone number -> [PHONE]
    """
    if not text:
        return ""
    text = URL.sub("[URL]", text)
    text = EMAIL.sub("[EMAIL]", text)
    text = MENTION.sub("[MENTION]", text)
    text = PHONE.sub("[PHONE]", text)
    return text
