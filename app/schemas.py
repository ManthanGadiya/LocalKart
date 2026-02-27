from pydantic import BaseModel


class CategoryOut(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


class ProductOut(BaseModel):
    id: int
    category_id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


class VarietyFeatureOut(BaseModel):
    feature_type: str
    feature_text: str

    class Config:
        from_attributes = True


class ProductVarietyOut(BaseModel):
    id: int
    product_id: int
    material: str
    display_name: str
    min_price: float | None = None
    max_price: float | None = None
    recommendation_score: float | None = None
    features: list[VarietyFeatureOut]


class ShopNearbyOut(BaseModel):
    id: int
    shop_name: str
    address_line: str
    city: str
    latitude: float
    longitude: float
    distance_km: float
    rating: float | None = None
    phone: str | None = None
    maps_url: str | None = None
