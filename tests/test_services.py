import pytest
from services import process_data, validate_data, DataProcessor, DataValidator

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

@pytest.fixture
def invalid_data():
    return "not a list"

@pytest.fixture
def empty_data():
    return []

@pytest.fixture
def non_integer_data():
    return [1, "a", 3]

@pytest.fixture
def nested_data():
    return [[1, 2], [3, 4]]

@pytest.fixture
def large_data():
    return list(range(1000))

class TestDataValidation:
    @pytest.mark.parametrize("data, expected", [
        ([1, 2, 3], True),
        ([1, "a"], False),
        ([], False),
        (None, False),
        ({}, False),
        ([1, 2, 3, 4], True)
    ])
    def test_validate_data_returns_expected(self, data, expected):
        result = validate_data(data)
        assert result == expected

    @pytest.mark.parametrize("data, expected_exception", [
        ("invalid", ValueError),
        ([1, "a"], ValueError),
        (None, ValueError),
        ({}, ValueError),
        ([], ValueError),
        (nested_data, ValueError)
    ])
    def test_validate_data_raises_exceptions(self, data, expected_exception):
        with pytest.raises(expected_exception):
            validate_data(data)

    def test_data_validator_valid_data(self):
        validator = DataValidator()
        assert validator.validate([1, 2, 3]) is None

    @pytest.mark.parametrize("data, expected_exception", [
        ("invalid", ValueError),
        ([1, "a"], ValueError),
        (None, ValueError),
        ({}, ValueError),
        ([], ValueError),
        (nested_data, ValueError)
    ])
    def test_data_validator_raises_exceptions(self, data, expected_exception):
        validator = DataValidator()
        with pytest.raises(expected_exception):
            validator.validate(data)

class TestDataProcessing:
    def test_process_data_valid_data(self, sample_data):
        result = process_data(sample_data)
        assert result == 15

    def test_process_data_invalid_data(self, invalid_data):
        with pytest.raises(ValueError):
            process_data(invalid_data)

    def test_data_processor_valid_data(self, sample_data):
        processor = DataProcessor()
        result = processor.process(sample_data)
        assert result == 15

    def test_data_processor_invalid_data(self, invalid_data):
        processor = DataProcessor()
        with pytest.raises(ValueError):
            processor.process(invalid_data)

    @pytest.mark.parametrize("data, expected", [
        ([1, 2, 3], 6),
        ([], 0),
        ([100], 100),
        (large_data, sum(range(1000)))
    ])
    def test_process_data_edge_cases(self, data, expected):
        result = process_data(data)
        assert result == expected

class TestErrorHandling:
    def test_validate_data_non_list_input(self, invalid_data):
        with pytest.raises(ValueError):
            validate_data(invalid_data)

    def test_validate_data_non_integer_elements(self, non_integer_data):
        with pytest.raises(ValueError):
            validate_data(non_integer_data)

    def test_process_data_non_list_input(self, invalid_data):
        with pytest.raises(ValueError):
            process_data(invalid_data)

    def test_process_data_non_integer_elements(self, non_integer_data):
        with pytest.raises(ValueError):
            process_data(non_integer_data)

    def test_data_processor_non_list_input(self, invalid_data):
        processor = DataProcessor()
        with pytest.raises(ValueError):
            processor.process(invalid_data)

    def test_data_processor_non_integer_elements(self, non_integer_data):
        processor = DataProcessor()
        with pytest.raises(ValueError):
            processor.process(non_integer_data)

    def test_data_validator_non_list_input(self, invalid_data):
        validator = DataValidator()
        with pytest.raises(ValueError):
            validator.validate(invalid_data)

    def test_data_validator_non_integer_elements(self, non_integer_data):
        validator = DataValidator()
        with pytest.raises(ValueError):
            validator.validate(non_integer_data)