PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_plain TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'customer'
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    UNIQUE (category_id, name),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS product_varieties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    display_name TEXT NOT NULL,
    min_price REAL,
    max_price REAL,
    recommendation_score REAL DEFAULT 0,
    UNIQUE (product_id, material_id),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS variety_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    variety_id INTEGER NOT NULL,
    feature_type TEXT NOT NULL CHECK (feature_type IN ('pro', 'con', 'general')),
    feature_text TEXT NOT NULL,
    FOREIGN KEY (variety_id) REFERENCES product_varieties(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_name TEXT NOT NULL,
    address_line TEXT NOT NULL,
    city TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    google_maps_url TEXT,
    phone TEXT,
    rating REAL CHECK (rating IS NULL OR (rating >= 0 AND rating <= 5)),
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1))
);

CREATE TABLE IF NOT EXISTS shop_inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id INTEGER NOT NULL,
    variety_id INTEGER NOT NULL,
    price REAL,
    in_stock INTEGER NOT NULL DEFAULT 1 CHECK (in_stock IN (0, 1)),
    stock_qty INTEGER CHECK (stock_qty IS NULL OR stock_qty >= 0),
    UNIQUE (shop_id, variety_id),
    FOREIGN KEY (shop_id) REFERENCES shops(id) ON DELETE CASCADE,
    FOREIGN KEY (variety_id) REFERENCES product_varieties(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_product_varieties_product_id ON product_varieties(product_id);
CREATE INDEX IF NOT EXISTS idx_variety_features_variety_id ON variety_features(variety_id);
CREATE INDEX IF NOT EXISTS idx_shops_latitude ON shops(latitude);
CREATE INDEX IF NOT EXISTS idx_shops_longitude ON shops(longitude);
CREATE INDEX IF NOT EXISTS idx_shop_inventory_shop_id ON shop_inventory(shop_id);
CREATE INDEX IF NOT EXISTS idx_shop_inventory_variety_id ON shop_inventory(variety_id);
