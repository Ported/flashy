"""Parse spoken numbers to integers."""

import re

# Word to number mappings
ONES = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "to": 2,  # speech recognition often outputs "to" for "two"
    "too": 2,  # speech recognition often outputs "too" for "two"
    "three": 3,
    "free": 3,  # often misheard as "three"
    "four": 4,
    "for": 4,  # speech recognition often outputs "for" for "four"
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "ate": 8,  # speech recognition often outputs "ate" for "eight"
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
FUZZY_PAIRS = frozenset(
    [
        (13, 30),  # thirteen / thirty
        (14, 40),  # fourteen / forty
        (15, 50),  # fifteen / fifty
        (16, 60),  # sixteen / sixty
        (17, 70),  # seventeen / seventy
        (18, 80),  # eighteen / eighty
        (19, 90),  # nineteen / ninety
    ]
)

# Digits that are commonly confused by speech recognition
# three (3) is often heard as four (4)
CONFUSED_DIGITS = {3: 4, 4: 3}

# Word-level confusions that cause structural changes
# "three" is often heard as "forty" (e.g., "three hundred" -> "forty hundred")
# This maps (recognized, expected) pairs that should be considered equivalent
CONFUSED_WORD_REPLACEMENTS = [
    (40, 3),  # "forty" misheard for "three"
]

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
    is_negative = False

    i = 0
    while i < len(words):
        word = words[i]

        if word in ("minus", "negative") and not found_number:
            is_negative = True
        elif word in ONES:
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
        result = total + current
        return -result if is_negative else result
    return None


def is_give_up(text: str) -> bool:
    """Check if the text is a give-up phrase."""
    if not text:
        return False

    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)  # Replace punctuation with space
    text = re.sub(r"\s+", " ", text).strip()  # Normalize whitespace

    return text in GIVE_UP_PHRASES


def _differs_by_confused_digit(recognized: int, expected: int) -> bool:
    """Check if two numbers differ only by a single confused digit swap.

    For example, 43 vs 44 (three heard as four), or 73 vs 74.
    """
    rec_str = str(recognized)
    exp_str = str(expected)

    if len(rec_str) != len(exp_str):
        return False

    diff_count = 0
    for r, e in zip(rec_str, exp_str, strict=True):
        if r != e:
            diff_count += 1
            if diff_count > 1:
                return False
            # Check if this is a confused digit pair
            r_digit, e_digit = int(r), int(e)
            if CONFUSED_DIGITS.get(e_digit) != r_digit:
                return False

    return diff_count == 1


def _matches_with_word_replacement(recognized: int, expected: int) -> bool:
    """Check if recognized matches expected after applying word-level replacements.

    Handles cases like "three hundred forty two" -> "forty hundred forty two"
    where "three" (3) was heard as "forty" (40).
    """
    for confused_val, correct_val in CONFUSED_WORD_REPLACEMENTS:
        # Try replacing the confused value with the correct value in recognized
        # e.g., 4042 with (40->3) replacement: 4042 -> 342
        rec_str = str(recognized)
        confused_str = str(confused_val)
        correct_str = str(correct_val)

        # Try replacing first occurrence
        if confused_str in rec_str:
            fixed = rec_str.replace(confused_str, correct_str, 1)
            try:
                if int(fixed) == expected:
                    return True
            except ValueError:
                pass

    return False


def is_fuzzy_match(recognized: int | None, expected: int) -> bool:
    """Check if recognized number is a fuzzy match for expected.

    Accepts commonly confused pairs like fifteen/fifty,
    numbers that differ by confused digits (e.g., 43 vs 44 for three/four),
    and word-level confusions (e.g., 4042 vs 342 for "forty" misheard as "three").
    """
    if recognized is None:
        return False

    if recognized == expected:
        return True

    # Check if they're a confused pair (teens vs tens)
    pair = (min(recognized, expected), max(recognized, expected))
    if pair in FUZZY_PAIRS:
        return True

    # Check if they differ by a confused digit (e.g., three/four)
    if _differs_by_confused_digit(recognized, expected):
        return True

    # Check for word-level replacements (e.g., "three" -> "forty")
    return _matches_with_word_replacement(recognized, expected)
