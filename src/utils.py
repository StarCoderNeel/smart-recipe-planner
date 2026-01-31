import logging
from typing import Optional, Dict, List
from pydantic import BaseModel
import re

logger = logging.getLogger(__name__)

class DietaryRestrictions(BaseModel):
    """
    Pydantic model representing dietary restrictions for recipe planning.
    
    Attributes:
        vegetarian (bool): Whether the recipe should be vegetarian.
        gluten_free (bool): Whether the recipe should be gluten-free.
        dairy_free (bool): Whether the recipe should be dairy-free.
        nut_free (bool): Whether the recipe should be nut-free.
        soy_free (boll): Whether the recipe should be soy-free.
    """
    vegetarian: bool = False
    gluten_free: bool = False
    dairy_free: bool = False
    nut_free: bool = False
    soy_free: bool = False

    class Config:
        arbitrary_types_allowed = True

def clean_recipe_name(recipe_name: str) -> Optional[str]:
    """
    Clean and format a recipe name by removing extra spaces and converting to title case.
    
    Args:
        recipe_name (str): The original recipe name.
        
    Returns:
        Optional[str]: The cleaned recipe name, or None if input is invalid.
    """
    try:
        if not isinstance(recipe_name, str):
            logger.error("Invalid input type for recipe name")
            return None
        cleaned = recipe_name.strip().title()
        logger.debug(f"Cleaned recipe name: {cleaned}")
        return cleaned
    except Exception as e:
        logger.error(f"Error cleaning recipe name: {e}")
        return None

def format_ingredient(ingredient: str) -> Optional[str]:
    """
    Format an ingredient string to standardize quantity, unit, and item representation.
    
    Args:
        ingredient (str): The raw ingredient string.
        
    Returns:
        Optional[str]: The formatted ingredient string, or None if input is invalid.
    """
    try:
        if not isinstance(ingredient, str):
            logger.error("Invalid input type for ingredient")
            return None
        # Example: "2 cups flour" -> "2 cups of flour"
        match = re.match(r'^(\d+)\s*(\w+)\s*(\w+)$', ingredient)
        if match:
            quantity, unit, item = match.groups()
            formatted = f"{quantity} {unit} of {item}"
            logger.debug(f"Formatted ingredient: {formatted}")
            return formatted
        logger.warning(f"Could not format ingredient: {ingredient}")
        return ingredient
    except Exception as e:
        logger.error(f"Error formatting ingredient: {e}")
        return None