import pytest
from utils import validate_email, is_palindrome, format_currency, trim_whitespace, sanitize_string, StringValidator

@pytest.fixture
def string_validator():
    return StringValidator()

class TestStringValidation:
    def test_validate_email_valid(self):
        assert validate_email("test@example.com")

    def test_validate_email_invalid(self):
        assert not validate_email("invalid-email")

    def test_validate_email_empty_string(self):
        assert not validate_email("")

    def test_validate_email_none(self):
        assert not validate_email(None)

    def test_is_palindrome_palindrome(self):
        assert is_palindrome("madam")

    def test_is_palindrome_non_palindrome(self):
        assert not is_palindrome("hello")

    def test_is_palindrome_single_char(self):
        assert is_palindrome("a")

    def test_is_palindrome_whitespace(self):
        assert is_palindrome("  ")

    def test_trim_whitespace_leading_trailing(self):
        assert trim_whitespace("  hello  ") == "hello"

    def test_trim_whitespace_all_spaces(self):
        assert trim_whitespace("    ") == ""

    def test_trim_whitespace_empty_string(self):
        assert trim_whitespace("") == ""

    def test_sanitize_string_special_characters(self):
        assert sanitize_string("Hello!@#") == "Hello"

    def test_sanitize_string_mixed(self):
        assert sanitize_string("abc123!@#") == "abc123"

    def test_sanitize_string_empty(self):
        assert sanitize_string("") == ""

    def test_sanitize_string_all_special(self):
        assert sanitize_string("!@#$%^") == ""

class TestStringFormatting:
    def test_format_currency_positive(self):
        assert format_currency(100, "USD") == "$100.00"

    def test_format_currency_negative(self):
        assert format_currency(-50, "EUR") == "-€50.00"

    def test_format_currency_zero(self):
        assert format_currency(0, "GBP") == "£0.00"

    def test_format_currency_decimal(self):
        assert format_currency(1234.56, "JPY") == "¥1,234.56"

    def test_format_currency_invalid_value(self):
        with pytest.raises(ValueError):
            format_currency("invalid", "USD")

    def test_format_currency_default_currency(self):
        assert format_currency(100) == "$100.00"

class TestStringValidatorClass:
    def test_string_validator_is_valid(self, string_validator):
        assert string_validator.is_valid("validstring") is True
        assert string_validator.is_valid("invalid") is False

    def test_string_validator_type_error(self, string_validator):
        with pytest.raises(TypeError):
            string_validator.is_valid(123)

    def test_string_validator_length_constraints(self, string_validator):
        assert string_validator.is_valid("short") is False
        assert string_validator.is_valid("long" * 20) is False

    def test_string_validator_custom_length(self, string_validator):
        validator = StringValidator(min_length=3, max_length=5)
        assert validator.is_valid("abc") is True
        assert validator.is_valid("abcd") is True
        assert validator.is_valid("abcde") is False

    def test_string_validator_min_length(self, string_validator):
        validator = StringValidator(min_length=5)
        assert validator.is_valid("abc") is False
        assert validator.is_valid("abcde") is True

    def test_string_validator_max_length(self, string_validator):
        validator = StringValidator(max_length=5)
        assert validator.is_valid("abcde") is True
        assert validator.is_valid("abcdef") is False

    def test_string_validator_invalid_input_type(self, string_validator):
        with pytest.raises(TypeError):
            string_validator.is_valid(123)