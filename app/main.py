import hashlib
from math import asin, cos, radians, sin, sqrt
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.database import Base, SessionLocal, engine
from app.models import Category, Product, ProductVariety, ShopInventory, User
from app.seed import seed_if_empty

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
static_dir = frontend_dir / "static"


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    radius = 6371.0
    d_lat = radians(lat2 - lat1)
    d_lng = radians(lng2 - lng1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng / 2) ** 2
    return 2 * radius * asin(sqrt(a))


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()


def page_response(filename: str):
    return send_from_directory(frontend_dir, filename)


def parse_float_arg(name: str, *, minimum: float | None = None, maximum: float | None = None, default=None) -> float:
    raw_value = request.args.get(name, default)
    if raw_value is None:
        abort(400, description=f"Missing required query parameter: {name}")
    try:
        value = float(raw_value)
    except (TypeError, ValueError):
        abort(400, description=f"Invalid value for {name}")
    if minimum is not None and value < minimum:
        abort(400, description=f"{name} must be >= {minimum}")
    if maximum is not None and value > maximum:
        abort(400, description=f"{name} must be <= {maximum}")
    return value


def parse_int_arg(name: str) -> int | None:
    raw_value = request.args.get(name)
    if raw_value in (None, ""):
        return None
    try:
        return int(raw_value)
    except ValueError:
        abort(400, description=f"Invalid value for {name}")


def parse_json_body() -> dict:
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Expected JSON request body")
    return data


def normalize_email(value: str) -> str:
    return value.strip().lower()


def derive_full_name(email: str) -> str:
    local_part = email.split("@", 1)[0]
    cleaned = local_part.replace(".", " ").replace("_", " ").replace("-", " ").strip()
    return " ".join(part.capitalize() for part in cleaned.split()) or "LocalKart User"


def create_app() -> Flask:
    app = Flask(__name__, static_folder=str(static_dir), static_url_path="/static")

    CORS(
        app,
        supports_credentials=True,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:63342",
                    "http://127.0.0.1:63342",
                    "http://localhost:5500",
                    "http://127.0.0.1:5500",
                    "http://localhost:8000",
                    "http://127.0.0.1:8000",
                ]
            }
        },
    )

    init_database()

    @app.get("/")
    def login_page():
        return page_response("index.html")

    @app.get("/index.html")
    def login_page_html():
        return page_response("index.html")

    @app.get("/home")
    def home_page():
        return page_response("home.html")

    @app.get("/home.html")
    def home_page_html():
        return page_response("home.html")

    @app.get("/select")
    def select_page():
        return page_response("select.html")

    @app.get("/select.html")
    def select_page_html():
        return page_response("select.html")

    @app.get("/materials")
    def materials_page():
        return page_response("materials.html")

    @app.get("/materials.html")
    def materials_page_html():
        return page_response("materials.html")

    @app.get("/nearby")
    def nearby_page():
        return page_response("nearby.html")

    @app.get("/nearby.html")
    def nearby_page_html():
        return page_response("nearby.html")

    @app.get("/about")
    def about_page():
        return page_response("about.html")

    @app.get("/about.html")
    def about_page_html():
        return page_response("about.html")

    @app.get("/discover")
    def backward_discover():
        return page_response("select.html")

    @app.get("/shops")
    def backward_shops():
        return page_response("nearby.html")

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/api/signup")
    def signup():
        data = parse_json_body()
        email = normalize_email(str(data.get("email", "")))
        password = str(data.get("password", "")).strip()
        full_name = str(data.get("full_name", "")).strip() or derive_full_name(email)

        if "@" not in email or "." not in email.split("@", 1)[-1]:
            return jsonify({"message": "Enter a valid email address."}), 400
        if len(password) < 4:
            return jsonify({"message": "Password must be at least 4 characters."}), 400

        db = SessionLocal()
        try:
            existing = db.query(User).filter(User.email == email).first()
            if existing:
                return jsonify({"message": "Email already registered."}), 409

            user = User(
                full_name=full_name,
                email=email,
                password_plain=password,
                password_hash=hashlib.sha256(password.encode("utf-8")).hexdigest(),
                role="customer",
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return (
                jsonify(
                    {
                        "message": "Sign up successful.",
                        "user": {
                            "id": user.id,
                            "full_name": user.full_name,
                            "email": user.email,
                            "role": user.role,
                        },
                    }
                ),
                201,
            )
        except IntegrityError:
            db.rollback()
            return jsonify({"message": "Email already registered."}), 409
        finally:
            db.close()

    @app.post("/api/login")
    def login():
        data = parse_json_body()
        email = normalize_email(str(data.get("email", "")))
        password = str(data.get("password", "")).strip()

        if not email or not password:
            return jsonify({"message": "Email and password are required."}), 400

        db = SessionLocal()
        try:
            password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
            user = db.query(User).filter(User.email == email, User.password_hash == password_hash).first()
            if not user:
                return jsonify({"message": "Invalid email or password."}), 401
            return jsonify(
                {
                    "message": "Login successful.",
                    "user": {
                        "id": user.id,
                        "full_name": user.full_name,
                        "email": user.email,
                        "role": user.role,
                    },
                }
            )
        finally:
            db.close()

    @app.get("/api/categories")
    def list_categories():
        db = SessionLocal()
        try:
            rows = db.query(Category).order_by(Category.name.asc()).all()
            return jsonify(
                [
                    {
                        "id": row.id,
                        "name": row.name,
                        "description": row.description,
                    }
                    for row in rows
                ]
            )
        finally:
            db.close()

    @app.get("/api/products")
    def list_products():
        category_id = parse_int_arg("category_id")
        db = SessionLocal()
        try:
            query = db.query(Product)
            if category_id is not None:
                query = query.filter(Product.category_id == category_id)
            rows = query.order_by(Product.name.asc()).all()
            return jsonify(
                [
                    {
                        "id": row.id,
                        "category_id": row.category_id,
                        "name": row.name,
                        "description": row.description,
                    }
                    for row in rows
                ]
            )
        finally:
            db.close()

    @app.get("/api/products/<int:product_id>/varieties")
    def list_varieties(product_id: int):
        db = SessionLocal()
        try:
            rows = (
                db.query(ProductVariety)
                .options(joinedload(ProductVariety.material), joinedload(ProductVariety.features))
                .filter(ProductVariety.product_id == product_id)
                .order_by(ProductVariety.recommendation_score.desc())
                .all()
            )
            payload = [
                {
                    "id": row.id,
                    "product_id": row.product_id,
                    "material": row.material.name,
                    "display_name": row.display_name,
                    "min_price": row.min_price,
                    "max_price": row.max_price,
                    "recommendation_score": row.recommendation_score,
                    "features": [
                        {
                            "feature_type": feature.feature_type,
                            "feature_text": feature.feature_text,
                        }
                        for feature in row.features
                    ],
                }
                for row in rows
            ]
            return jsonify(payload)
        finally:
            db.close()

    @app.get("/api/shops/nearby")
    def nearby_shops():
        lat = parse_float_arg("lat", minimum=-90, maximum=90)
        lng = parse_float_arg("lng", minimum=-180, maximum=180)
        radius_km = parse_float_arg("radius_km", minimum=0.000001, maximum=100, default=10)
        product_id = parse_int_arg("product_id")

        db = SessionLocal()
        try:
            query = db.query(ShopInventory).options(joinedload(ShopInventory.shop), joinedload(ShopInventory.variety))
            if product_id is not None:
                query = query.join(ShopInventory.variety).filter(ProductVariety.product_id == product_id)

            result = []
            seen = set()
            for item in query.all():
                shop = item.shop
                if not shop or not shop.is_active or shop.id in seen:
                    continue
                distance = haversine_km(lat, lng, shop.latitude, shop.longitude)
                if distance <= radius_km:
                    seen.add(shop.id)
                    result.append(
                        {
                            "id": shop.id,
                            "shop_name": shop.shop_name,
                            "address_line": shop.address_line,
                            "city": shop.city,
                            "latitude": shop.latitude,
                            "longitude": shop.longitude,
                            "distance_km": round(distance, 2),
                            "rating": shop.rating,
                            "phone": shop.phone,
                            "maps_url": shop.google_maps_url,
                        }
                    )

            result.sort(key=lambda row: row["distance_km"])
            return jsonify(result)
        finally:
            db.close()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
