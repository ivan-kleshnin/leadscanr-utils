# Informal tests to check the function's behavior
from textutils.mask import mask_contacts

tests = [
    # Positive tests for phone numbers
    ("+7-920-123-45-67", "[PHONE]"),
    ("Мой номер: 8 (920) 123-45-67", "Мой номер: [PHONE]"),
    ("Звоните +1 123 456 7890", "Звоните [PHONE]"),
    ("Телефон (495)123-45-67", "Телефон [PHONE]"),
    ("Мобильный: 8 999 123 45 67", "Мобильный: [PHONE]"),

    # Negative tests to ensure normal numbers are not captured
    ("Потратил на обед 150.000 рублей", "Потратил на обед 150.000 рублей"),
    ("Цена товара 85000 рублей", "Цена товара 85000 рублей"),
    ("Номер рейса 1234567890", "Номер рейса 1234567890"),
    ("Посмотрите на странице 250", "Посмотрите на странице 250"),
    ("Код доступа: 12345", "Код доступа: 12345"),
    ("Сумма: 1234.56", "Сумма: 1234.56"),
    ("Мы продали 500 тыс. единиц.", "Мы продали 500 тыс. единиц."),

    # Test with mixed content
    ("Email: user@example.com, URL: www.example.com", "Email: [EMAIL], URL: [URL]"),
    ("Набери меня на +7(920)123-45-67, или напиши @john_smith", "Набери меня на [PHONE], или напиши [MENTION]"),

]

print("Running tests for mask_contacts function:")
print("-" * 40)
for inp, expected in tests:
    out = mask_contacts(inp)
    print(f"'{inp}' → '{out}' | {'✅' if out == expected else '❌'}")
print("-" * 40)
