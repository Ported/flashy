"""Parse spoken numbers to integers."""

import re

# Word to number mappings
ONES = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
}

TENS = {
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}

# Commonly confused number pairs (teens vs tens)
FUZZY_PAIRS = frozenset([
    (13, 30),  # thirteen / thirty
    (14, 40),  # fourteen / forty
    (15, 50),  # fifteen / fifty
    (16, 60),  # sixteen / sixty
    (17, 70),  # seventeen / seventy
    (18, 80),  # eighteen / eighty
    (19, 90),  # nineteen / ninety
])

# Give up phrases (include variants without apostrophes)
GIVE_UP_PHRASES = frozenset(
    [
        "give up",
        "skip",
        "pass",
        "i don t know",
        "i dont know",
        "next",
        "i give up",
    ]
)


def parse_spoken_number(text: str) -> int | None:
    """Parse a spoken number string to an integer.

    Handles:
    - Single digits: "five" -> 5
    - Teens: "thirteen" -> 13
    - Tens: "twenty" -> 20
    - Compound: "twenty three" -> 23
    - Hundreds: "one hundred" -> 100, "one hundred twenty three" -> 123
    - Raw digits: "42" -> 42

    Returns None if no valid number found.
    """
    if not text:
        return None

    # Normalize: lowercase, strip extra whitespace/punctuation
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)  # Replace punctuation with space
    text = re.sub(r"\s+", " ", text).strip()  # Normalize whitespace

    # Try parsing as raw integer first (Vosk sometimes outputs digits)
    try:
        return int(text)
    except ValueError:
        pass

    # Try to find a number in the text
    words = text.split()

    # Try parsing the full phrase, then progressively shorter suffixes
    # This handles cases like "the answer is twenty three"
    for start in range(len(words)):
        result = _parse_number_words(words[start:])
        if result is not None:
            return result

    return None


def _parse_number_words(words: list[str]) -> int | None:
    """Parse a list of words as a number."""
    if not words:
        return None

    total = 0
    current = 0
    found_number = False

    i = 0
    while i < len(words):
        word = words[i]

        if word in ONES:
            current += ONES[word]
            found_number = True
        elif word in TENS:
            current += TENS[word]
            found_number = True
        elif word == "hundred":
            if current == 0:
                current = 1
            current *= 100
            found_number = True
        elif word == "and":
            # Skip "and" (e.g., "one hundred and twenty")
            pass
        else:
            # Unknown word - if we found a number, stop here
            if found_number:
                break
            # Otherwise, this isn't a number phrase
            return None

        i += 1

    if found_number:
        return total + current
    return None


def is_give_up(text: str) -> bool:
    """Check if the text is a give-up phrase."""
    if not text:
        return False

    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)  # Replace punctuation with space
    text = re.sub(r"\s+", " ", text).strip()  # Normalize whitespace

    return text in GIVE_UP_PHRASES


def is_fuzzy_match(recognized: int | None, expected: int) -> bool:
    """Check if recognized number is a fuzzy match for expected.

    Accepts commonly confused pairs like fifteen/fifty.
    """
    if recognized is None:
        return False

    if recognized == expected:
        return True

    # Check if they're a confused pair
    pair = (min(recognized, expected), max(recognized, expected))
    return pair in FUZZY_PAIRS
