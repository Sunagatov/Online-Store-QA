from data.text_review import (
    text_review_750_char,
    text_review_1500_char,
    text_review_1499_char,
    text_review_with_digits,
    text_review_with_extended_latin_letters,
    text_review_with_allowed_symbols,
    text_review_with_emojy,
    text_review_1_char,
    text_review_2_char,
)

reviews = [
    {"text_review": text_review_750_char, "rating": 5},
    {"text_review": text_review_1500_char, "rating": 4},
    {"text_review": text_review_1499_char, "rating": 3},
    {"text_review": text_review_2_char, "rating": 2},
    {"text_review": text_review_1_char, "rating": 1},
    {"text_review": text_review_with_emojy, "rating": 2},
    {"text_review": text_review_with_allowed_symbols, "rating": 1},
    {"text_review": text_review_with_extended_latin_letters, "rating": 5},
    {"text_review": text_review_with_digits, "rating": 5},
    {
        "text_review": "So happy with this purchase, it was perfect in every way.",
        "rating": 5,
    },
]
