from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_plain = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="customer")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    name = Column(String(120), nullable=False)
    description = Column(Text)

    category = relationship("Category", back_populates="products")
    varieties = relationship("ProductVariety", back_populates="product", cascade="all, delete-orphan")


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    varieties = relationship("ProductVariety", back_populates="material")


class ProductVariety(Base):
    __tablename__ = "product_varieties"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False, index=True)
    display_name = Column(String(160), nullable=False)
    min_price = Column(Float)
    max_price = Column(Float)
    recommendation_score = Column(Float, default=0)

    product = relationship("Product", back_populates="varieties")
    material = relationship("Material", back_populates="varieties")
    features = relationship("VarietyFeature", back_populates="variety", cascade="all, delete-orphan")
    inventory_rows = relationship("ShopInventory", back_populates="variety", cascade="all, delete-orphan")


class VarietyFeature(Base):
    __tablename__ = "variety_features"

    id = Column(Integer, primary_key=True, index=True)
    variety_id = Column(Integer, ForeignKey("product_varieties.id"), nullable=False, index=True)
    feature_type = Column(String(20), nullable=False)
    feature_text = Column(Text, nullable=False)

    variety = relationship("ProductVariety", back_populates="features")


class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(String(160), nullable=False)
    address_line = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    google_maps_url = Column(Text)
    phone = Column(String(30))
    rating = Column(Float)
    is_active = Column(Boolean, nullable=False, default=True)

    inventory = relationship("ShopInventory", back_populates="shop", cascade="all, delete-orphan")


class ShopInventory(Base):
    __tablename__ = "shop_inventory"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False, index=True)
    variety_id = Column(Integer, ForeignKey("product_varieties.id"), nullable=False, index=True)
    price = Column(Float)
    in_stock = Column(Boolean, nullable=False, default=True)
    stock_qty = Column(Integer)

    shop = relationship("Shop", back_populates="inventory")
    variety = relationship("ProductVariety", back_populates="inventory_rows")
