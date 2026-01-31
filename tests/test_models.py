import pytest
from models import User, Product, validate_data, create_model

class TestUserModel:
    @pytest.mark.parametrize("name, email, expected", [
        ("Alice", "alice@example.com", True),
        ("Bob", "bob@example.com", True),
        ("", "invalid@example.com", False),
        ("John", "", False),
    ])
    def test_valid_user(self, name, email, expected):
        if expected:
            User(name=name, email=email)
        else:
            with pytest.raises(ValueError):
                User(name=name, email=email)

    def test_missing_required_field(self):
        with pytest.raises(ValueError):
            User(name="Alice")

    def test_invalid_type_for_name(self):
        with pytest.raises(ValueError):
            User(name=123, email="alice@example.com")

    def test_extra_fields(self):
        with pytest.raises(ValueError):
            User(name="Alice", email="alice@example.com", age=30)

class TestProductModel:
    @pytest.mark.parametrize("name, price, category, expected", [
        ("Laptop", 999.99, "Electronics", True),
        ("Phone", -100.00, "Electronics", False),
        ("Tablet", 299.99, "Invalid", False),
        ("Monitor", 149.99, "Electronics", True),
    ])
    def test_product_validation(self, name, price, category, expected):
        if expected:
            Product(name=name, price=price, category=category)
        else:
            with pytest.raises(ValueError):
                Product(name=name, price=price, category=category)

    def test_missing_name_field(self):
        with pytest.raises(ValueError):
            Product(price=999.99, category="Electronics")

    def test_invalid_category(self):
        with pytest.raises(ValueError):
            Product(name="Laptop", price=999.99, category="InvalidCategory")

    def test_negative_price(self):
        with pytest.raises(ValueError):
            Product(name="Laptop", price=-99.99, category="Electronics")

class TestValidationUtils:
    @pytest.mark.parametrize("data, expected", [
        ({"name": "Product A", "price": 10.99, "category": "Electronics"}, True),
        ({"name": "", "price": -5.99, "category": "Invalid"}, False),
        ({"name": "Product B", "price": 15.50, "category": "Books"}, True),
        ({"name": "Product C", "price": 0.00, "category": "Electronics"}, False),
    ])
    def test_validate_data(self, data, expected):
        if expected:
            assert validate_data(data)
        else:
            with pytest.raises(ValueError):
                validate_data(data)

    def test_create_model_error(self):
        with pytest.raises(ValueError):
            create_model("InvalidModel", name="Test")

    def test_custom_error_messages(self):
        data = {"name": "Test", "price": -10.99, "category": "Invalid"}
        with pytest.raises(ValueError) as exc_info:
            validate_data(data)
        assert "Price must be positive" in str(exc_info.value)
        assert "Category must be one of" in str(exc_info.value)

    def test_invalid_data_type(self):
        with pytest.raises(ValueError):
            validate_data(123)