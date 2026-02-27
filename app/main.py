from math import asin, cos, radians, sin, sqrt
from pathlib import Path

from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload

from app.database import Base, SessionLocal, engine, get_db
from app.models import Category, Product, ProductVariety, ShopInventory
from app.schemas import CategoryOut, ProductOut, ProductVarietyOut, ShopNearbyOut, VarietyFeatureOut
from app.seed import seed_if_empty

app = FastAPI(title="LocalKart API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:63342",
        "http://127.0.0.1:63342",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=frontend_dir / "static"), name="static")


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    radius = 6371.0
    d_lat = radians(lat2 - lat1)
    d_lng = radians(lng2 - lng1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng / 2) ** 2
    return 2 * radius * asin(sqrt(a))


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()


@app.get("/")
def login_page():
    return FileResponse(frontend_dir / "index.html")


@app.get("/home")
def home_page():
    return FileResponse(frontend_dir / "home.html")


@app.get("/home.html")
def home_page_html():
    return FileResponse(frontend_dir / "home.html")


@app.get("/select")
def select_page():
    return FileResponse(frontend_dir / "select.html")


@app.get("/select.html")
def select_page_html():
    return FileResponse(frontend_dir / "select.html")


@app.get("/materials")
def materials_page():
    return FileResponse(frontend_dir / "materials.html")


@app.get("/materials.html")
def materials_page_html():
    return FileResponse(frontend_dir / "materials.html")


@app.get("/nearby")
def nearby_page():
    return FileResponse(frontend_dir / "nearby.html")


@app.get("/nearby.html")
def nearby_page_html():
    return FileResponse(frontend_dir / "nearby.html")


@app.get("/about")
def about_page():
    return FileResponse(frontend_dir / "about.html")


@app.get("/about.html")
def about_page_html():
    return FileResponse(frontend_dir / "about.html")


@app.get("/discover")
def backward_discover():
    return FileResponse(frontend_dir / "select.html")


@app.get("/shops")
def backward_shops():
    return FileResponse(frontend_dir / "nearby.html")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.name.asc()).all()


@app.get("/api/products", response_model=list[ProductOut])
def list_products(category_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(Product)
    if category_id is not None:
        q = q.filter(Product.category_id == category_id)
    return q.order_by(Product.name.asc()).all()


@app.get("/api/products/{product_id}/varieties", response_model=list[ProductVarietyOut])
def list_varieties(product_id: int, db: Session = Depends(get_db)):
    rows = (
        db.query(ProductVariety)
        .options(joinedload(ProductVariety.material), joinedload(ProductVariety.features))
        .filter(ProductVariety.product_id == product_id)
        .order_by(ProductVariety.recommendation_score.desc())
        .all()
    )
    return [
        ProductVarietyOut(
            id=r.id,
            product_id=r.product_id,
            material=r.material.name,
            display_name=r.display_name,
            min_price=r.min_price,
            max_price=r.max_price,
            recommendation_score=r.recommendation_score,
            features=[VarietyFeatureOut.model_validate(f) for f in r.features],
        )
        for r in rows
    ]


@app.get("/api/shops/nearby", response_model=list[ShopNearbyOut])
def nearby_shops(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(10, gt=0, le=100),
    product_id: int | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(ShopInventory).options(joinedload(ShopInventory.shop), joinedload(ShopInventory.variety))
    if product_id is not None:
        q = q.join(ShopInventory.variety).filter(ProductVariety.product_id == product_id)

    result = []
    seen = set()
    for item in q.all():
        shop = item.shop
        if not shop or not shop.is_active or shop.id in seen:
            continue
        d = haversine_km(lat, lng, shop.latitude, shop.longitude)
        if d <= radius_km:
            seen.add(shop.id)
            result.append(
                ShopNearbyOut(
                    id=shop.id,
                    shop_name=shop.shop_name,
                    address_line=shop.address_line,
                    city=shop.city,
                    latitude=shop.latitude,
                    longitude=shop.longitude,
                    distance_km=round(d, 2),
                    rating=shop.rating,
                    phone=shop.phone,
                    maps_url=shop.google_maps_url,
                )
            )

    return sorted(result, key=lambda x: x.distance_km)
