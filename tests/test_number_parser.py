"""Tests for spoken number parsing."""

from flashy.core.number_parser import is_fuzzy_match, is_give_up, parse_spoken_number


class TestParseSpokenNumber:
    """Tests for parse_spoken_number function."""

    def test_single_digits(self) -> None:
        assert parse_spoken_number("zero") == 0
        assert parse_spoken_number("one") == 1
        assert parse_spoken_number("five") == 5
        assert parse_spoken_number("nine") == 9

    def test_teens(self) -> None:
        assert parse_spoken_number("ten") == 10
        assert parse_spoken_number("eleven") == 11
        assert parse_spoken_number("thirteen") == 13
        assert parse_spoken_number("nineteen") == 19

    def test_tens(self) -> None:
        assert parse_spoken_number("twenty") == 20
        assert parse_spoken_number("thirty") == 30
        assert parse_spoken_number("fifty") == 50
        assert parse_spoken_number("ninety") == 90

    def test_compound_numbers(self) -> None:
        assert parse_spoken_number("twenty one") == 21
        assert parse_spoken_number("twenty three") == 23
        assert parse_spoken_number("forty two") == 42
        assert parse_spoken_number("ninety nine") == 99

    def test_hundreds(self) -> None:
        assert parse_spoken_number("one hundred") == 100
        assert parse_spoken_number("two hundred") == 200
        assert parse_spoken_number("five hundred") == 500

    def test_hundreds_with_tens(self) -> None:
        assert parse_spoken_number("one hundred twenty") == 120
        assert parse_spoken_number("one hundred twenty three") == 123
        assert parse_spoken_number("two hundred fifty") == 250

    def test_hundreds_with_and(self) -> None:
        assert parse_spoken_number("one hundred and twenty three") == 123

    def test_raw_digits(self) -> None:
        assert parse_spoken_number("42") == 42
        assert parse_spoken_number("100") == 100
        assert parse_spoken_number("7") == 7

    def test_with_prefix_words(self) -> None:
        # Vosk might include extra words
        assert parse_spoken_number("the answer is twenty three") == 23
        assert parse_spoken_number("it's forty two") == 42

    def test_case_insensitive(self) -> None:
        assert parse_spoken_number("TWENTY") == 20
        assert parse_spoken_number("Twenty Three") == 23

    def test_extra_whitespace(self) -> None:
        assert parse_spoken_number("  twenty   three  ") == 23

    def test_with_punctuation(self) -> None:
        # Vosk output might have punctuation
        assert parse_spoken_number("twenty-three") == 23
        assert parse_spoken_number("twenty, three") == 23

    def test_empty_string(self) -> None:
        assert parse_spoken_number("") is None
        assert parse_spoken_number("   ") is None

    def test_no_number(self) -> None:
        assert parse_spoken_number("hello world") is None
        assert parse_spoken_number("the") is None

    def test_trailing_words_ignored(self) -> None:
        # Should stop at first non-number word after finding number
        assert parse_spoken_number("twenty three hello") == 23


class TestIsGiveUp:
    """Tests for is_give_up function."""

    def test_give_up_phrases(self) -> None:
        assert is_give_up("give up") is True
        assert is_give_up("skip") is True
        assert is_give_up("pass") is True
        assert is_give_up("next") is True
        assert is_give_up("i don't know") is True
        assert is_give_up("i give up") is True

    def test_case_insensitive(self) -> None:
        assert is_give_up("GIVE UP") is True
        assert is_give_up("Skip") is True

    def test_with_whitespace(self) -> None:
        assert is_give_up("  give up  ") is True

    def test_not_give_up(self) -> None:
        assert is_give_up("twenty three") is False
        assert is_give_up("hello") is False
        assert is_give_up("") is False


class TestIsFuzzyMatch:
    """Tests for is_fuzzy_match function."""

    def test_exact_match(self) -> None:
        assert is_fuzzy_match(15, 15) is True
        assert is_fuzzy_match(50, 50) is True

    def test_fuzzy_pairs(self) -> None:
        # fifteen / fifty
        assert is_fuzzy_match(15, 50) is True
        assert is_fuzzy_match(50, 15) is True
        # thirteen / thirty
        assert is_fuzzy_match(13, 30) is True
        assert is_fuzzy_match(30, 13) is True
        # eighteen / eighty
        assert is_fuzzy_match(18, 80) is True
        assert is_fuzzy_match(80, 18) is True

    def test_not_fuzzy_match(self) -> None:
        assert is_fuzzy_match(15, 16) is False
        assert is_fuzzy_match(50, 60) is False
        assert is_fuzzy_match(10, 20) is False

    def test_none_recognized(self) -> None:
        assert is_fuzzy_match(None, 15) is False
