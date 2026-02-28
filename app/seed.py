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
        and existing["shops"] >= 130
        and existing["inventory"] >= 520
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
        ("Cast Iron", "High heat retention"),
        ("Triply Steel", "Even heating with layered durability"),
        ("Non-stick", "Easy cleaning and low oil cooking"),
        ("Hard Anodized", "Tough, scratch-resistant surface"),
        ("Clay", "Traditional, slow and even heat"),
        ("Steel", "Durable and long lasting"),
        ("Ceramic", "Non-reactive and food-safe"),
        ("Aluminium", "Lightweight and affordable"),
        ("Glass", "Food-safe and transparent"),
        ("Plastic", "Lightweight utility"),
        ("Wood", "Natural finish"),
        ("Marble", "Heavy and stable surface"),
        ("Brass", "Classic, sturdy material"),
        ("Silicone", "Heat resistant and flexible"),
        ("Clay Coating", "Clay coated for healthier cooking"),
        ("Black Finish", "Matte black coated surface"),
        ("Honeycomb", "Textured surface for better sear"),
        ("Multipurpose", "Versatile use-case build"),
        ("Normal", "Standard basic build"),
    ]
    materials = [models.Material(name=n, description=d) for n, d in material_defs]
    db.add_all(materials)
    db.flush()

    utensil_names = [
        "Kadhai",
        "Frypan",
        "Saucepan",
        "Grill Pan",
        "Tawa",
        "Tasla",
        "Casserole / Handi",
        "Cooker",
        "Appam Patra",
        "Multipurpose Pan",
        "Stock Pot",
        "Roasting Pan",
        "Baking Tray / Sheet",
        "Steamer / Puttu Maker",
        "Idli Stand",
        "Chakla",
        "Belan",
    ]
    other_product_names = {
        "Appliances": ["Electric Kettle"],
        "Dining": ["Mixing Bowl", "Serving Bowl / Handi"],
        "Groceries": ["Spice Box"],
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
        "Cast Iron": "Excellent heat retention",
        "Triply Steel": "Even heat distribution and high durability",
        "Non-stick": "Low oil cooking and easy cleaning",
        "Hard Anodized": "Scratch resistant and durable surface",
        "Clay": "Slow, even cooking with natural feel",
        "Steel": "Rust resistant and long lasting",
        "Ceramic": "Food-safe and premium finish",
        "Aluminium": "Lightweight and affordable",
        "Glass": "Visible cooking and non-reactive",
        "Plastic": "Light and economical",
        "Wood": "Natural look and sturdy grip",
        "Marble": "Very stable surface with good grip",
        "Brass": "Sturdy material with traditional appeal",
        "Silicone": "Heat resistant with flexible handling",
        "Clay Coating": "Healthier cooking surface with clay layer",
        "Black Finish": "Attractive matte finish",
        "Honeycomb": "Better sear and reduced sticking",
        "Multipurpose": "Versatile for different use cases",
        "Normal": "Standard build for everyday use",
    }
    con_by_material = {
        "Cast Iron": "Heavier to handle daily",
        "Triply Steel": "Usually more expensive than basic options",
        "Non-stick": "Coating needs careful handling",
        "Hard Anodized": "Can be costlier than basic pans",
        "Clay": "Requires careful handling to avoid cracks",
        "Steel": "Can stick without proper preheating",
        "Ceramic": "Premium variants can be costly",
        "Aluminium": "Can dent over long rough use",
        "Glass": "Can break with sudden impact",
        "Plastic": "Not suitable for high-heat cooking",
        "Wood": "Needs dry storage to avoid moisture damage",
        "Marble": "Heavy to move frequently",
        "Brass": "Needs regular polishing",
        "Silicone": "Limited for direct flame use",
        "Clay Coating": "Coating needs gentle care",
        "Black Finish": "Finish can fade with rough scrubbing",
        "Honeycomb": "Still needs proper cleaning after searing",
        "Multipurpose": "May not excel in a single task",
        "Normal": "Basic build without premium features",
    }

    materials_by_name = {m.name: m for m in materials}
    product_materials = {
        "Kadhai": ["Cast Iron", "Triply Steel", "Non-stick", "Hard Anodized"],
        "Frypan": [
            "Aluminium",
            "Ceramic",
            "Honeycomb",
            "Cast Iron",
            "Triply Steel",
            "Non-stick",
            "Hard Anodized",
            "Clay",
        ],
        "Saucepan": ["Steel", "Non-stick", "Ceramic"],
        "Grill Pan": ["Cast Iron", "Ceramic", "Non-stick"],
        "Tawa": ["Cast Iron", "Non-stick", "Steel", "Ceramic"],
        "Tasla": ["Aluminium", "Steel", "Non-stick"],
        "Casserole / Handi": ["Steel", "Ceramic", "Clay", "Non-stick"],
        "Cooker": ["Steel", "Clay Coating", "Hard Anodized", "Black Finish"],
        "Appam Patra": ["Cast Iron", "Non-stick"],
        "Multipurpose Pan": ["Non-stick"],
        "Stock Pot": ["Steel", "Aluminium", "Ceramic"],
        "Roasting Pan": ["Steel", "Non-stick", "Ceramic"],
        "Baking Tray / Sheet": ["Aluminium", "Non-stick", "Silicone"],
        "Electric Kettle": ["Multipurpose", "Normal"],
        "Steamer / Puttu Maker": ["Steel", "Aluminium"],
        "Idli Stand": ["Steel", "Aluminium", "Non-stick"],
        "Mixing Bowl": ["Steel", "Glass", "Ceramic", "Plastic"],
        "Serving Bowl / Handi": ["Clay", "Ceramic", "Steel"],
        "Chakla": ["Wood", "Marble"],
        "Belan": ["Wood", "Steel"],
        "Spice Box": ["Steel", "Brass"],
    }

    varieties = []
    for i, p in enumerate(products):
        mat_names = product_materials.get(p.name, [])
        if not mat_names:
            continue
        for j, mat_name in enumerate(mat_names):
            material = materials_by_name.get(mat_name)
            if material is None:
                continue
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
        (
            "Pune",
            18.5204,
            73.8567,
            [
                "Shivaji Nagar", "Kothrud", "Baner", "Aundh", "Hadapsar", "Wakad", "Viman Nagar", "Kharadi",
                "Karve Road", "FC Road", "Deccan", "Pashan", "Bavdhan", "Warje", "Erandwane", "Camp",
                "Koregaon Park", "Mundhwa", "Magarpatta", "Kalyani Nagar", "Ravet", "Pimple Saudagar",
                "Hinjewadi", "Balewadi", "Sus", "NIBM", "Kondhwa", "Bibwewadi", "Dhankawadi", "Katrap",
                "Swargate", "Sadashiv Peth", "Narhe", "Dhayari", "Sinhagad Road", "Nigdi", "Akurdi",
                "Chinchwad", "Bhosari", "Yerawada"
            ],
        ),
        (
            "Mumbai",
            19.0760,
            72.8777,
            [
                "Dadar", "Andheri", "Borivali", "Ghatkopar", "Bandra", "Powai", "Chembur", "Kurla",
                "Thane West", "Malad", "Santacruz", "Vile Parle", "Jogeshwari", "Goregaon", "Kandivali",
                "Byculla", "Parel", "Worli", "Lower Parel", "Sion", "Matunga", "Colaba", "Cuffe Parade",
                "Mulund", "Bhandup", "Kanjurmarg", "Mira Road", "Dahisar", "Bhayandar", "Navi Mumbai"
            ],
        ),
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
