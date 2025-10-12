from .bucket import bucket_numbers
from .cleanup import clean_text
from .fold import fold_currencies, fold_numbers, fold_scale_units
from .mask import mask_contacts

def process(text: str) -> str:
    text = mask_contacts(text)
    text = fold_currencies(text)
    text = fold_numbers(text)
    text = fold_scale_units(text)
    text = clean_text(text)
    text = bucket_numbers(text)
    return text
