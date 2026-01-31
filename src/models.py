import logging
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, root_validator

logging.basicConfig(level=logging.INFO)

class DietaryRestriction(Enum):
    """Enum representing common dietary restrictions."""
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    KOSHER = "kosher"
    HALAL = "halal"
    DIABETIC_FRIENDLY = "diabetic_friendly"
    LOW_SODIUM = "low_sodium"

class UserPreferences(BaseModel):
    """Model representing user preferences for recipe planning."""
    dietary_restrictions: List[str] = Field(default=[])
    preferred_cuisines: List[str] = Field(default=[])
    allergies: List[str] = Field(default=[])
    is_allergic_to_nuts: bool = Field(default=False)
    max_calories_per_meal: Optional[int] = Field(default=None)
    preferred_meal_types: List[str] = Field(default=[])

    @root_validator
    def validate_dietary_restrictions(cls, values):
        """Validate that dietary restrictions are valid enum values."""
        for restriction in values.get('dietary_restrictions', []):
            if restriction not in [e.value for e in DietaryRestriction]:
                raise ValueError(f"Invalid dietary restriction: {restriction}")
        return values

class Meal(BaseModel):
    """Model representing a single meal in the meal plan."""
    name: str = Field(...)
    description: str = Field(...)
    ingredients: List[str] = Field(default=[])
    calories: Optional[int] = Field(default=None)
    nutrients: Dict[str, float] = Field(default={})

class MealPlan(BaseModel):
    """Model representing a meal plan for a specific date."""
    date: str = Field(...)
    meals: List[Meal] = Field(default=[])
    total_calories: Optional[int] = Field(default=None)
    nutrients: Dict[str, float] = Field(default={})

    class Config:
        arbitrary_types_allowed = True

class GroceryItem(BaseModel):
    """Model representing a grocery item for shopping."""
    name: str = Field(...)
    quantity: float = Field(ge=0.0)
    unit: str = Field(default="unit")
    category: str = Field(default="unknown")

def generate_grocery_list(meal_plans: List[MealPlan]) -> List[GroceryItem]:
    """Generate a grocery list from a list of meal plans."""
    grocery_items = []
    try:
        for plan in meal_plans:
            for meal in plan.meals:
                for ingredient in meal.ingredients:
                    grocery_items.append(GroceryItem(name=ingredient, quantity=1.0, unit="unit", category="ingredient"))
        unique_items = {}
        for item in grocery_items:
            key = (item.name, item.unit)
            if key in unique_items:
                unique_items[key].quantity += item.quantity
            else:
                unique_items[key] = item
        grocery_items = list(unique_items.values())
        logging.info("Generated grocery list with %d items", len(grocery_items))
        return grocery_items
    except Exception as e:
        logging.error("Error generating grocery list: %s", str(e))
        raise

def validate_user_preferences(preferences: UserPreferences) -> bool:
    """Validate user preferences against dietary restrictions."""
    try:
        for restriction in preferences.dietary_restrictions:
            if restriction not in [e.value for e in DietaryRestriction]:
                return False
        for allergy in preferences.allergies:
            if not allergy.isalpha():
                return False
        logging.info("User preferences validated successfully")
        return True
    except Exception as e:
        logging.error("Error validating user preferences: %s", str(e))
        raise