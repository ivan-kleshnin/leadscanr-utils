import re

def fold_numbers(text: str) -> str:
    def replacer(match):
        return match.group(0).replace(".", "").replace(",", "").replace(" ", "")
    pattern = r"\b\d{1,3}([., ]\d{3})+\b"
    return re.sub(pattern, replacer, text)

def fold_scale_units(text: str) -> str:
    pattern = r"(\d+[,.]?\d*)(?:\s*[-–—~]\s*(\d+[,.]?\d*))?\s+тыс\.?"

    def replacer(match) -> str:
        num1_str = match.group(1)
        num2_str = match.group(2)
        num1 = int(float(num1_str.replace(',', '.')) * 1000)
        if num2_str:
            num2 = int(float(num2_str.replace(',', '.')) * 1000)
            return f"{num1}-{num2}"
        else:
            return str(num1)

    return re.sub(pattern, replacer, text, flags=re.IGNORECASE)

def fold_currencies(text: str) -> str:
    return text.replace("рублей", "₽")
