from ninja import Schema
from .models import VariantType
from decimal import Decimal
from enum import Enum

class VariantRead(Schema):
    sku: str
    description: str
    type: VariantType
    price: Decimal
    stock: int
    production_days: int
    is_customizable: bool

class ProductRead(Schema):
    store: int
    name: str
    description: str
    image: str
    is_active: bool
    variants: list[VariantRead]

class ProductOrdering(str, Enum):
    PRICE_ASC = "price"
    PRICE_DESC = "-price"
    NAME_ASC = "name"
    NAME_DESC = "-name"

class ProductFilter(Schema):
    ordering: ProductOrdering | None = None
    min_price: Decimal | None = None
    max_price: Decimal | None = None