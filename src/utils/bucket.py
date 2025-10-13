import re

BUCKETS = [
    (200, 500, "500"),             # 300
    (500, 1_000, "1 тыс"),         # 500
    (1_000, 2_000, "2 тыс"),       # 1k
    (2_000, 3_000, "3 тыс"),       # 1k
    (3_000, 5_000, "5 тыс"),       # 2k
    (5_000, 7_000, "7 тыс"),       # 2k
    (7_000, 10_000, "10 тыс"),     # 3k
    (10_000, 15_000, "15 тыс"),    # 5k
    (15_000, 20_000, "20 тыс"),    # 5k
    (20_000, 30_000, "30 тыс"),    # 10k
    (30_000, 40_000, "40 тыс"),    # 10k
    (40_000, 60_000, "60 тыс"),    # 20k
    (60_000, 80_000, "80 тыс"),    # 20k
    (80_000, 120_000, "120 тыс"),  # 40k
    (120_000, 160_000, "160 тыс"), # 40k
    (160_000, 220_000, "220 тыс"), # 60k
    (220_000, 280_000, "280 тыс"), # 60k
    (280_000, 360_000, "360 тыс"), # 80k
    (360_000, 440_000, "440 тыс"), # 80k
]

def bucket_numbers(text: str) -> str:
    """
    Replaces numbers in text with buckets according to rules:
    - Floats untouched
    - 1-2 digit integers untouched
    - ≥3 digit integers replaced with bucket labels
    - Numbers preceded by '#' are ignored
    - Numbers followed by '%' are ignored
    """
    def replacer(match: re.Match) -> str:
        num_str = match.group(0)
        # Skip floats
        if '.' in num_str:
            return num_str
        n = int(num_str)
        # Skip small out-of-bucket numbers
        if n < BUCKETS[0][0]:
            return num_str
        # Find bucket
        for lower, upper, label in BUCKETS:
            if lower <= n <= upper:
                return label
        return ">440 тыс"

    text = re.sub(r"(?<!#)\b\d+\b(?!%)", replacer, text)
    return text
