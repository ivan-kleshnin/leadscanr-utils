import re

BUCKETS = [
    (0, 500, "[<500]"),
    (500, 1_000, "[<1K]"),
    (1_000, 2_000, "[<2K]"),
    (2_000, 3_000, "[<3K]"),
    (3_000, 5_000, "[<5K]"),
    (5_000, 7_000, "[<7K]"),
    (7_000, 10_000, "[<10K]"),
    (10_000, 15_000, "[<15K]"),
    (15_000, 20_000, "[<20K]"),
    (20_000, 30_000, "[<30K]"),
    (30_000, 40_000, "[<40K]"),
    (40_000, 60_000, "[<60K]"),
    (60_000, 80_000, "[<80K]"),
    (80_000, 110_000, "[<110K]"),
    (110_000, 140_000, "[<140K]"),
    (140_000, 180_000, "[<180K]"),
    (180_000, 220_000, "[<220K]"),
]

def bucket_numbers(text: str) -> str:
    """
    Replaces numbers in text with buckets according to rules:
    - Floats untouched
    - 1-2 digit integers untouched
    - ≥3 digit integers replaced with bucket labels
    """
    def replacer(match: re.Match) -> str:
        num_str = match.group(0)
        # Skip floats
        if '.' in num_str:
            return num_str
        n = int(num_str)
        # Skip 1-2 digit numbers
        if n < 100:
            return num_str
        # Find bucket
        for lower, upper, label in BUCKETS:
            if lower <= n < upper:
                return label
        return "[>220K]"

    return re.sub(r"\b\d+\b", replacer, text)
