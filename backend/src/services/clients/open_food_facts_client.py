from threading import TIMEOUT_MAX
import httpx
from typing import Dict, Optional, Any
from ...config.settings import settings

class OpenFoodFactsClient:
    OPEN_FOOD_FACTS_API_URL = settings.open_food_facts_api_url
    TIMEOUT = 10.0

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=TIMEOUT)
    
    async def close(self):
        await self.client.aclose()

    async def get_product(self, barcode: str) -> Optional[Dict[str, any]]:
        try:
            url = f"{OPEN_FOOD_FACTS_API_URL}/product/{barcode}.json"
            response = await self.client.get(url)
            response.raise_for_status()

            data = response.json()

            if data.get("status") == 0:
                return None
            return self._normalize_product(data.get("product", {}), barcode)
        except httpx.HTTPError as e:
            return None
        except Exception as e:
            return None

def _normalize_product(self, raw_product: Dict[str, Any]):
    nutriments = raw_product.get("nutriments", {})
        
        # Extract nutrition data per 100g
    nutrition_data = {
            "calories_100g": nutriments.get("energy-kcal_100g", 0),
            "protein_100g": nutriments.get("proteins_100g", 0),
            "carbs_100g": nutriments.get("carbohydrates_100g", 0),
            "sugar_100g": nutriments.get("sugars_100g", 0),
            "fat_100g": nutriments.get("fat_100g", 0),
            "saturated_fat_100g": nutriments.get("saturated-fat_100g", 0),
            "fiber_100g": nutriments.get("fiber_100g", 0),
            "sodium_100g": nutriments.get("sodium_100g", 0),
            "salt_100g": nutriments.get("salt_100g", 0),
    }
        
    # Parse ingredients list
    ingredients_list = []
    ingredients_data = raw_product.get("ingredients", [])
    for ingredient in ingredients_data:
        if "text" in ingredient:
            ingredients_list.append(ingredient["text"].lower())
        elif "id" in ingredient:
            ingredients_list.append(ingredient["id"].replace("en:", "").lower())
    
    # Get allergens
    allergens = []
    allergens_tags = raw_product.get("allergens_tags", [])
    for tag in allergens_tags:
        allergen = tag.replace("en:", "").replace("-", " ")
        allergens.append(allergen)
    
    # Get categories
    categories = []
    categories_tags = raw_product.get("categories_tags", [])
    for tag in categories_tags[:5]:  # Limit to top 5 categories
        category = tag.replace("en:", "").replace("-", " ")
        categories.append(category)
    
    # Parse NOVA group (string to int)
    nova_group = None
    if raw_product.get("nova_group"):
        try:
            nova_group = int(raw_product["nova_group"])
        except (ValueError, TypeError):
            nova_group = None
    
    return {
        "barcode": raw_product.get("code"),
        "name": raw_product.get("product_name", "Unknown Product"),
        "brand": raw_product.get("brands", "").split(",")[0].strip() or None,
        "image_url": raw_product.get("image_url") or raw_product.get("image_front_url"),
        "nutrition_data": nutrition_data,
        "ingredients_text": raw_product.get("ingredients_text"),
        "ingredients_list": ingredients_list,
        "nova_group": nova_group,
        "allergens": allergens,
        "categories": categories,
    }