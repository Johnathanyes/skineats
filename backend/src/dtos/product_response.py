from sqlmodel import SQLModel
from typing import Optional, List, Dict, Any
from decimal import Decimal
from datetime import datetime

class ProductResponse(SQLModel):
    barcode: str
    product_name: str
    brand: Optional[str]
    categories: Optional[List[str]]
    kcalories_100g: Optional[Decimal]
    protein_100g: Optional[Decimal]
    carbs_100g: Optional[Decimal]
    sugar_100g: Optional[Decimal]
    fiber_100g: Optional[Decimal]
    fat_100g: Optional[Decimal]
    saturated_fat_100g: Optional[Decimal]
    sodium_100g: Optional[Decimal]

    skin_score: Optional[int]
    skin_score_breakdown: Optional[List[Dict[str, Any]]]

    ingredient_list: Optional[List[Dict[str, str]]]
    nova_group: Optional[int]

    allergen_tags: Optional[List[str]]
    labels_tag: Optional[List[str]]

    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime


