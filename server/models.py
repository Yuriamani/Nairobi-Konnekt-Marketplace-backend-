from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.postgresql import JSONB
from . import db
from datetime import datetime, timezone

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    # id = db.Column(db.String(50), primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Changed from String to Integer
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float)
    images = db.Column(JSONB)  # Store as JSONB array
    rating = db.Column(db.Float)
    review_count = db.Column(db.Integer)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    category = db.Column(db.String(50))
    sub_category = db.Column(db.String(50))
    tags = db.Column(JSONB)  # JSONB array
    stock = db.Column(db.Integer)
    features = db.Column(JSONB)  # Optional
    created_at = db.Column(db.DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),  index=True)  # Alternative cursor
    specifications = db.Column(JSONB)  # Optional key-value pairs
    is_featured = db.Column(db.Boolean, default=False)
    is_new_arrival = db.Column(db.Boolean, default=False)
    is_best_seller = db.Column(db.Boolean, default=False)

    vendor = db.relationship('Vendor', back_populates='products')
    serialize_rules = ('-vendor.products',)

class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'

    # id = db.Column(db.String(50), primary_key=True, autoincrement=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Changed from String to Integer
    name = db.Column(db.String(100), nullable=False)
    # Add more vendor fields later (email, location, etc.)

    products = db.relationship('Product', back_populates='vendor', cascade="all, delete-orphan")
    serialize_rules = ('-products.vendor',)