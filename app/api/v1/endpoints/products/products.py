from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional
from app.schemas.products.cable import CableProduct, CableProductListResponse, CableProductUnit


router = APIRouter(prefix="/products", tags=["Products"])


# Мок-данные кабельной продукции
MOCK_PRODUCTS = [
    {
        "id": 1,
        "name": "Кабель ВВГНГ(А)-LS 3х1,5",
        "description": "Кабель силовой медный, не распространяющий горение",
        "price": 45.50,  # цена за метр
        "stock_quantity": 1500,
        "unit": CableProductUnit.METERS,
        "pack_size": 150,
        "min_order_quantity": 150,  # минимально упаковка
        "category": "Силовые кабели",
        "brand": "Энергокабель",
        "specifications": {
            "сечение": "1.5 мм²",
            "количество_жил": 3,
            "напряжение": "0.66 кВ",
            "температура_эксплуатации": "-50°C до +70°C"
        }
    },
    {
        "id": 2,
        "name": "Кабель ВВГНГ(А)-LS 3х2,5",
        "description": "Кабель силовой для стационарной прокладки",
        "price": 68.90,
        "stock_quantity": 1200,
        "unit": CableProductUnit.METERS,
        "pack_size": 150,
        "min_order_quantity": 150,
        "category": "Силовые кабели",
        "brand": "Энергокабель",
        "specifications": {
            "сечение": "2.5 мм²",
            "количество_жил": 3,
            "напряжение": "1 кВ",
            "температура_эксплуатации": "-50°C до +70°C"
        }
    },
    {
        "id": 3,
        "name": "Кабель АВВГ 4х6",
        "description": "Кабель алюминиевый силовой",
        "price": 120.75,
        "stock_quantity": 900,
        "unit": CableProductUnit.METERS,
        "pack_size": 150,
        "min_order_quantity": 150,
        "category": "Алюминиевые кабели",
        "brand": "Кабельный завод",
        "specifications": {
            "сечение": "6 мм²",
            "количество_жил": 4,
            "напряжение": "1 кВ",
            "материал_жилы": "алюминий"
        }
    }
]


@router.get("", response_model=CableProductListResponse)
async def get_products(
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1, le=100),
        category: Optional[str] = None,
        search: Optional[str] = None
):
    """Получить список товаров с пагинацией и фильтрацией"""

    # Фильтрация
    filtered_products = MOCK_PRODUCTS

    if category:
        filtered_products = [p for p in filtered_products if p["category"] == category]

    if search:
        search_lower = search.lower()
        filtered_products = [
            p for p in filtered_products
            if search_lower in p["name"].lower() or
               (p["description"] and search_lower in p["description"].lower())
        ]

    # Пагинация
    total = len(filtered_products)
    start = (page - 1) * limit
    end = start + limit
    paginated_products = filtered_products[start:end]

    return {
        "products": paginated_products,
        "total": total,
        "page": page,
        "limit": limit
    }


@router.get("/{product_id}", response_model=CableProduct)
async def get_product(product_id: int):
    """Получить информацию о конкретном товаре"""

    product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return product


@router.get("/categories/list")
async def get_categories():
    """Получить список всех категорий"""

    categories = list(set(product["category"] for product in MOCK_PRODUCTS))
    return {"categories": categories}