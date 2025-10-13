from .bucket import bucket_numbers
from .cleanup import clean_emojis, denoise, normalize_whitespace
from .fold import fold_currencies, fold_numbers, fold_scale_units, fold_shortcuts
from .mask import mask_contacts

def process(text: str) -> str:
    text = clean_emojis(text)
    text = denoise(text)
    text = mask_contacts(text)
    text = fold_shortcuts(text)
    text = fold_numbers(text)
    text = fold_scale_units(text)
    text = fold_currencies(text)
    text = normalize_whitespace(text)
    return text

# Note: number bucketing is destructive so better applied separately
