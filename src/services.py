import logging
from pydantic import BaseModel, ValidationError
from typing import List, Dict, Optional
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DietaryRestriction(BaseModel):
    """Model representing dietary restrictions."""
    restriction: str
    severity: int

class UserPreferences(BaseModel):
    """Model representing user preferences for recipe planning."""
    dietary_restrictions: List[DietaryRestriction]
    preferred_cuisines: List[str]
    meal_types: List[str]
    max_calories: int
    min_protein: float
    max_fat: float

class RecipeService:
    """Service layer for recipe recommendation logic."""
    
    def __init__(self):
        """Initialize recipe service with empty recipe database."""
        self.logger = logging.getLogger(__name__)
        self.recipes = self._load_sample_recipes()
    
    def _load_sample_recipes(self) -> List[Dict]:
        """Load sample recipes for demonstration purposes."""
        return [
            {"id": str(uuid.uuid4()), "name": "Grilled Salmon", "cuisine": "Western", "calories": 400, "protein": 35, "fat": 15},
            {"id": str(uuid.uuid4()), "name": "Vegetable Stir Fry", "cuisine": "Asian", "calories": 300, "protein": 15, "fat": 10},
            {"id": str(uuid.uuid4()), "name": "Quinoa Salad", "cuisine": "Mediterranean", "calories": 350, "protein": 20, "fat": 12}
        ]
    
    def find_matching_recipes(self, preferences: UserPreferences) -> List[Dict]:
        """
        Find recipes matching user preferences.
        
        Args:
            preferences: UserPreferences object containing dietary restrictions and preferences
            
        Returns:
            List of matching recipes
        """
        try:
            self.logger.info("Finding recipes matching preferences: %s", preferences)
            matching_recipes = []
            
            for recipe in self.recipes:
                # Check dietary restrictions
                if any(dr.restriction in recipe.get("name", "").lower() for dr in preferences.dietary_restrictions):
                    continue
                
                # Check cuisine preferences
                if not any(cuisine in recipe["cuisine"].lower() for cuisine in preferences.preferred_cuisines):
                    continue
                
                # Check meal type
                if not any(meal in recipe["name"].lower() for meal in preferences.meal_types):
                    continue
                
                # Check nutritional constraints
                if recipe["calories"] > preferences.max_calories:
                    continue
                
                if recipe["protein"] < preferences.min_protein:
                    continue
                
                if recipe["fat"] > preferences.max_fat:
                    continue
                
                matching_recipes.append(recipe)
            
            return matching_recipes
        
        except Exception as e:
            self.logger.error("Error finding recipes: %s", str(e))
            return []

class GroceryService:
    """Service layer for generating grocery lists."""
    
    def __init__(self):
        """Initialize grocery service with empty grocery database."""
        self.logger = logging.getLogger(__name__)
        self.grocery_items = self._load_sample_grocery_items()
    
    def _load_sample_grocery_items(self) -> List[Dict]:
        """Load sample grocery items for demonstration purposes."""
        return [
            {"item": "Salmon", "quantity": "1 kg", "category": "Protein"},
            {"item": "Mixed Vegetables", "quantity": "500g", "category": "Vegetables"},
            {"item": "Quinoa", "quantity": "500g", "category": "Grains"}
        ]
    
    def generate_grocery_list(self, recipes: List[Dict]) -> List[Dict]:
        """
        Generate a grocery list from a list of recipes.
        
        Args:
            recipes: List of recipe dictionaries
            
        Returns:
            List of grocery items needed for the recipes
        """
        try:
            self.logger.info("Generating grocery list for %d recipes", len(recipes))
            grocery_list = []
            
            for recipe in recipes:
                for item in self.grocery_items:
                    if item["category"] in recipe["name"].lower():
                        grocery_list.append(item)
            
            return grocery_list
        
        except Exception as e:
            self.logger.error("Error generating grocery list: %s", str(e))
            return []

def validate_preferences(raw_data: Dict) -> UserPreferences:
    """
    Validate and parse user preferences from raw input.
    
    Args:
        raw_data: Dictionary containing raw preference data
        
    Returns:
        Validated UserPreferences object
        
    Raises:
        ValueError: If input data is invalid
    """
    try:
        return UserPreferences(**raw_data)
    except ValidationError as e:
        logger.error("Validation error in preferences: %s", e)
        raise ValueError("Invalid preferences data") from e