from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class CableProductUnit(str, Enum):
    METERS = "meters"
    DRUM = "drums"  # барабаны
    COILS = "coils"  # бухты


class CableProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    unit: CableProductUnit
    pack_size: Optional[int] = None  # Размер упаковки (150 метров)
    min_order_quantity: int = 1  # Минимальное количество для заказа


class CableProduct(CableProductBase):
    id: int
    category: str
    brand: Optional[str] = None
    specifications: Optional[dict] = None  # Технические характеристики

    class Config:
        from_attributes = True


class CableProductListResponse(BaseModel):
    products: List[CableProduct]
    total: int
    page: int
    limit: int