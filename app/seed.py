import hashlib

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app import models


def ensure_seed_users(db: Session) -> None:
    seed_users = [
        ("Anish Patil", "anish@example.com", "anish123"),
        ("Riya Sharma", "riya@example.com", "riya123"),
        ("Aman Gupta", "aman@example.com", "aman123"),
        ("Neha Kulkarni", "neha@example.com", "neha123"),
        ("Rahul Joshi", "rahul@example.com", "rahul123"),
    ]
    try:
        existing_emails = {u.email for u in db.query(models.User).all()}
    except OperationalError:
        # Auto-heal old table shape by recreating users table with latest columns.
        models.User.__table__.drop(bind=db.bind, checkfirst=True)
        models.User.__table__.create(bind=db.bind, checkfirst=True)
        db.commit()
        existing_emails = set()
    created = False
    for full_name, email, plain_password in seed_users:
        if email in existing_emails:
            continue
        db.add(
            models.User(
                full_name=full_name,
                email=email,
                password_plain=plain_password,
                password_hash=hashlib.sha256(plain_password.encode("utf-8")).hexdigest(),
                role="customer",
            )
        )
        created = True
    if created:
        db.commit()


def seed_if_empty(db: Session) -> None:
    ensure_seed_users(db)

    existing = {
        "users": db.query(models.User).count(),
        "categories": db.query(models.Category).count(),
        "products": db.query(models.Product).count(),
        "materials": db.query(models.Material).count(),
        "varieties": db.query(models.ProductVariety).count(),
        "features": db.query(models.VarietyFeature).count(),
        "shops": db.query(models.Shop).count(),
        "inventory": db.query(models.ShopInventory).count(),
    }
    if (
        existing["users"] >= 5
        and existing["categories"] >= 12
        and existing["products"] >= 40
        and existing["materials"] >= 12
        and existing["varieties"] >= 180
        and existing["features"] >= 360
        and existing["shops"] >= 80
        and existing["inventory"] >= 320
    ):
        return

    db.query(models.ShopInventory).delete()
    db.query(models.VarietyFeature).delete()
    db.query(models.ProductVariety).delete()
    db.query(models.Shop).delete()
    db.query(models.Product).delete()
    db.query(models.Material).delete()
    db.query(models.Category).delete()
    db.commit()

    category_defs = [
        ("Utensils", "Kitchen cookware"),
        ("Electronics", "Home electronics"),
        ("Furniture", "Home furniture"),
        ("Groceries", "Daily grocery needs"),
        ("Cleaning", "Cleaning essentials"),
        ("Storage", "Containers and organizers"),
        ("Appliances", "Small home appliances"),
        ("Bathroom", "Bathroom products"),
        ("Dining", "Dining and serveware"),
        ("Outdoor", "Outdoor utility items"),
        ("Kids", "Kids household items"),
        ("Tools", "Basic utility tools"),
    ]
    categories = [models.Category(name=n, description=d) for n, d in category_defs]
    db.add_all(categories)

    material_defs = [
        ("Triply", "Durable and even heating"),
        ("Non-stick", "Easy cleaning"),
        ("Aluminium", "Budget friendly"),
        ("Stainless Steel", "Rust resistant"),
        ("Cast Iron", "High heat retention"),
        ("Copper", "Fast heat conduction"),
        ("Glass", "Food-safe transparent"),
        ("Ceramic", "Non-reactive surface"),
        ("Plastic", "Lightweight utility"),
        ("Wood", "Natural finish"),
        ("Silicone", "Flexible and safe grip"),
        ("Carbon Steel", "Strong and quick heating"),
    ]
    materials = [models.Material(name=n, description=d) for n, d in material_defs]
    db.add_all(materials)
    db.flush()

    utensil_names = [
        "Kadhai",
        "Frying Pan",
        "Tawa",
        "Cooker",
        "Saucepan",
        "Milk Pot",
        "Stock Pot",
        "Steamer",
        "Idli Stand",
        "Dosa Tawa",
        "Grill Pan",
        "Handi",
        "Wok",
        "Skillet",
        "Roti Tawa",
        "Pressure Pan",
    ]
    other_product_names = {
        "Electronics": ["Mixer", "Induction Plate", "Toaster", "Blender"],
        "Furniture": ["Dining Chair", "Kitchen Stool", "Utility Rack", "Cupboard"],
        "Groceries": ["Rice Bin", "Flour Box", "Spice Box", "Oil Can"],
        "Cleaning": ["Floor Wiper", "Scrub Brush", "Mop Set", "Cleaning Caddy"],
        "Storage": ["Storage Jar", "Lunch Box", "Container Set", "Spice Rack"],
        "Appliances": ["Electric Kettle", "Air Fryer", "Rice Cooker", "Sandwich Maker"],
        "Bathroom": ["Bucket", "Mug", "Soap Holder", "Towel Rack"],
        "Dining": ["Serving Bowl", "Dinner Plate", "Glass Set", "Cutlery Stand"],
        "Outdoor": ["Water Can", "Camping Pot", "Portable Stove", "Utility Knife"],
        "Kids": ["Kids Bottle", "Snack Box", "Mini Plate", "Sipper"],
        "Tools": ["Hammer", "Screwdriver Set", "Pliers", "Measuring Tape"],
    }

    products = []
    for c in categories:
        names = utensil_names if c.name == "Utensils" else other_product_names.get(c.name, [])
        for name in names:
            products.append(
                models.Product(
                    category=c,
                    name=name,
                    description=f"{name} - {c.name} product",
                )
            )
    db.add_all(products)
    db.flush()

    pro_by_material = {
        "Triply": "Even heat distribution and high durability",
        "Non-stick": "Low oil cooking and easy cleaning",
        "Aluminium": "Lightweight and affordable",
        "Stainless Steel": "Rust resistant and long lasting",
        "Cast Iron": "Excellent heat retention",
        "Copper": "Fast heating response",
        "Glass": "Visible cooking and non-reactive",
        "Ceramic": "Food-safe and premium finish",
        "Plastic": "Light and economical",
        "Wood": "Natural look and sturdy grip",
        "Silicone": "Heat resistant with flexible handling",
        "Carbon Steel": "Strong body with fast heating",
    }
    con_by_material = {
        "Triply": "Usually more expensive than basic options",
        "Non-stick": "Coating needs careful handling",
        "Aluminium": "Can dent over long rough use",
        "Stainless Steel": "Can stick without proper preheating",
        "Cast Iron": "Heavier to handle daily",
        "Copper": "Needs regular maintenance for shine",
        "Glass": "Can break with sudden impact",
        "Ceramic": "Premium variants can be costly",
        "Plastic": "Not suitable for high-heat cooking",
        "Wood": "Needs dry storage to avoid moisture damage",
        "Silicone": "Limited for direct flame use",
        "Carbon Steel": "Needs seasoning for best performance",
    }

    varieties = []
    for i, p in enumerate(products):
        # 4 unique materials for each product.
        material_indices = [(i + j) % len(materials) for j in range(4)]
        for j, m_idx in enumerate(material_indices):
            material = materials[m_idx]
            base = 250 + (i * 37) + (j * 120)
            varieties.append(
                models.ProductVariety(
                    product=p,
                    material=material,
                    display_name=f"{material.name} {p.name}",
                    min_price=base,
                    max_price=base + 900 + (j * 80),
                    recommendation_score=round(6.2 + ((i + j) % 35) * 0.1, 2),
                )
            )
    db.add_all(varieties)
    db.flush()

    features = []
    for v in varieties:
        features.append(
            models.VarietyFeature(
                variety=v,
                feature_type="pro",
                feature_text=pro_by_material.get(v.material.name, "Good for regular use"),
            )
        )
        features.append(
            models.VarietyFeature(
                variety=v,
                feature_type="con",
                feature_text=con_by_material.get(v.material.name, "May need careful maintenance"),
            )
        )
        features.append(
            models.VarietyFeature(
                variety=v,
                feature_type="general",
                feature_text=f"Best for {v.product.name} use in regular home cooking",
            )
        )
    db.add_all(features)

    location_clusters = [
        ("Pune", 18.5204, 73.8567, ["Shivaji Nagar", "Kothrud", "Baner", "Aundh", "Hadapsar", "Wakad", "Viman Nagar", "Kharadi", "Karve Road", "FC Road"]),
        ("Mumbai", 19.0760, 72.8777, ["Dadar", "Andheri", "Borivali", "Ghatkopar", "Bandra", "Powai", "Chembur", "Kurla", "Thane West", "Malad"]),
        ("Nashik", 20.0110, 73.7903, ["College Road", "Gangapur Road", "Canada Corner", "CIDCO", "Panchavati", "Indira Nagar", "Satpur", "Pathardi", "Dwarka", "Makhmalabad"]),
        ("Nagpur", 21.1458, 79.0882, ["Sitabuldi", "Dharampeth", "Manish Nagar", "Sadar", "Mahal", "Wardhaman Nagar", "Pratap Nagar", "Nandanvan", "Trimurti Nagar", "Ramdaspeth"]),
        ("Bengaluru", 12.9716, 77.5946, ["Indiranagar", "Whitefield", "Jayanagar", "HSR Layout", "Koramangala", "Rajajinagar", "Malleshwaram", "Marathahalli", "Yelahanka", "Hebbal"]),
        ("Hyderabad", 17.3850, 78.4867, ["Banjara Hills", "Kukatpally", "Madhapur", "Gachibowli", "Ameerpet", "Begumpet", "Secunderabad", "LB Nagar", "Kondapur", "Uppal"]),
        ("Delhi", 28.6139, 77.2090, ["Karol Bagh", "Lajpat Nagar", "Dwarka", "Rohini", "Pitampura", "Saket", "Janakpuri", "Rajouri Garden", "Mayur Vihar", "Connaught Place"]),
        ("Ahmedabad", 23.0225, 72.5714, ["Navrangpura", "Maninagar", "Satellite", "Bopal", "Naranpura", "Vastrapur", "Paldi", "Gota", "Chandkheda", "Thaltej"]),
    ]

    shops = []
    shop_counter = 1
    for city, lat_base, lng_base, areas in location_clusters:
        for i, area in enumerate(areas):
            lat = lat_base + ((i % 5) - 2) * 0.01
            lng = lng_base + ((i % 4) - 1.5) * 0.012
            shops.append(
                models.Shop(
                    shop_name=f"LocalKart {city} Store {shop_counter}",
                    address_line=f"{area}, {city}",
                    city=city,
                    latitude=round(lat, 6),
                    longitude=round(lng, 6),
                    google_maps_url=f"https://maps.google.com/?q={round(lat, 6)},{round(lng, 6)}",
                    phone=f"+91-90000{10000 + shop_counter}",
                    rating=round(3.9 + (shop_counter % 11) * 0.1, 1),
                )
            )
            shop_counter += 1
    db.add_all(shops)
    db.flush()

    inventory = []
    for i, s in enumerate(shops):
        for j in range(4):
            v = varieties[(i * 7 + j * 13) % len(varieties)]
            inventory.append(
                models.ShopInventory(
                    shop=s,
                    variety=v,
                    price=round((v.min_price or 300) + 100 + (j * 55), 2),
                    in_stock=((i + j) % 5 != 0),
                    stock_qty=3 + ((i + j) % 22),
                )
            )
    db.add_all(inventory)
    db.commit()
