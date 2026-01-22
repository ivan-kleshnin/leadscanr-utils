import re

URL = re.compile(
    r"""
    (?:                                   # Entire URL
      https?://[^\s'">]+(?<!\))           # Option 1: http(s):// ... but not ending with ')'
    | www\.[^\s'">]+(?<!\))               # Option 2: www....  but not ending with ')'
    |                                     # Option 3:
      (?:[a-z0-9-]+\.)+                   #   Subdomain(s)
      (?:com|org|net|io|me|co|dev|ai|be)  #   Whitelist TLDs
      (?:/[^\s'">]*)?(?<!\))              #   Optional path  
    )
    """,
    flags=re.VERBOSE | re.IGNORECASE,
)
EMAIL = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", flags=re.IGNORECASE)
MENTION = re.compile(r"@[A-Za-z0-9_]+")
PHONE = re.compile(
    r"""
    (?<!\w) # Negative lookbehind to prevent partial matches
    (?:
      # Option 1: Must start with a '+'
      \+\d{1,3}(?:[\s-]?\(?\d{2,4}\)?[\s-]?)*\d{2,4}(?:[\s-]?\d{2,4}){1,3}

    | # Option 2: Must contain an opening parenthesis '('
      (?:\d{1,3}[\s-]?)?\(\d{2,4}\)[\s-]?\d{2,4}(?:[\s-]?\d{2,4}){1,3}

    | # Option 3: Russian mobile starting with 8 followed by 10 digits
      8[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}
    )
    (?!\w) # Negative lookahead to prevent partial matches
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
    text = EMAIL.sub("[EMAIL]", text)
    text = URL.sub("[URL]", text)
    text = MENTION.sub("[MENTION]", text)
    text = PHONE.sub("[PHONE]", text)
    text = re.sub(r"(?<=ИНН: )(\d+)", "[ID]", text, flags=re.IGNORECASE)
    return text
