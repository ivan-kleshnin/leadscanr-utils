import re
from .bucket import bucket_numbers
from .cleanup import denoise, normalize_whitespace, clean_unicode
from .fold import fold_currencies, fold_numbers, fold_scale_units, fold_shortcuts
from .mask import mask_contacts

def preprocess(text: str) -> str:
    text = denoise(text)
    ################################################################################################
    # UNGROUPED STUFF YET
    # Unify secondary whitespace cases
    text = re.sub(r"(?<=\d)р\b", " р", text)
    text = re.sub(r"(?<=\d)(₽|\$|€)", r" \1", text)
    text = re.sub(r"(?<=\d)м2\b", " м2", text)
    # Collapse common "от NUM до NUM" cases
    text = re.sub(r"\bот\s+(\d+)\d\s+до\s+(\d+)", r"\1–\2", text, flags=re.IGNORECASE)
    ################################################################################################
    text = mask_contacts(text)
    text = fold_shortcuts(text)
    text = fold_numbers(text)
    text = fold_scale_units(text)
    text = fold_currencies(text)
    text = normalize_whitespace(text)
    return text

# Information-destructive steps are applied separately:
# - diacritics removal
# - number bucketing
# - etc
# Note: contact masking is also destrucrive, should be moved outside!
