from server import db
from server.models import Product, Vendor
from app import app
from faker import Faker
import random

fake = Faker()

with app.app_context():

    print("Deleting data...")
    Product.query.delete()
    Vendor.query.delete()
    print("Data deleted.")

    print("Seeding data...")   

 # Create 10 vendors with Faker
    vendors = []
    
    for _ in range(10):
        vendor = Vendor(
            name=fake.company(),
        )
        vendors.append(vendor)
    
    db.session.add_all(vendors)
    db.session.commit()
 
    # Create 50 products with Faker
    products = []
    product_categories = {
    "electronics": [
        "smartphones-accessories",
        "laptops-computers",
        "headphones-audio",
        "cameras-photography"
    ],
    "fashion": [
        "mens-clothing",
        "womens-clothing",
        "shoes",
        "accessories-bags-watches"
    ],
    "home-kitchen": [
        "furniture",
        "kitchen-appliances",
        "home-decor",
        "bedding-bath"
    ],
    "beauty-personal-care": [
        "skincare",
        "makeup",
        "haircare",
        "fragrances"
    ],
    "books": [
        "fiction",
        "non-fiction",
        "childrens-books",
        "educational-textbooks"
    ],
    "toys-games": [
        "action-figures-dolls",
        "board-games",
        "outdoor-toys",
        "puzzles-learning"
    ],
    "sports-outdoors": [
        "fitness-equipment",
        "outdoor-sports",
        "cycling",
        "team-sports"
    ],
    "automotive": [
        "car-parts-accessories",
        "car-electronics",
        "tools-maintenance",
        "motorcycle-gear"
    ],
    "grocery": [
        "snacks-beverages",
        "baking-cooking",
        "canned-packaged-foods",
        "dairy-frozen"
    ],
    "health-household": [
        "vitamins-supplements",
        "medical-supplies",
        "household-cleaning",
        "personal-hygiene"
    ],
    "industrial-scientific": [
        "tools-machinery",
        "safety-equipment",
        "lab-supplies",
        "electrical-components"
    ]
}
    
    for _ in range(50):
        vendor = fake.random_element(elements=vendors)
        category = random.choice(list(product_categories.keys()))
        sub_category = random.choice(product_categories[category])
        # Generate random product data
        price = round(random.uniform(10, 1000), 2)
        original_price = price * round(random.uniform(1.1, 1.5), 2) if random.random() > 0.3 else None
        product = Product(
            name=fake.catch_phrase(),
            description=fake.paragraph(),
            price=price,
            original_price=original_price,
            images=[fake.image_url() for _ in range(random.randint(1, 5))],
            rating=round(random.uniform(1, 5), 1),
            review_count=random.randint(0, 500),
            vendor_id=vendor.id,
            category=category,
            sub_category=sub_category,
            tags=[fake.word() for _ in range(random.randint(1, 5))],
            stock=random.randint(0, 100),
            features=[f"Feature {i+1}" for i in range(random.randint(1, 5))] if random.random() > 0.5 else None,
            specifications={"Weight": f"{random.randint(1, 10)} kg", "Color": fake.color_name()} if random.random() > 0.5 else None,
            is_featured=random.random() > 0.7,
            is_new_arrival=random.random() > 0.7,
            is_best_seller=random.random() > 0.7
        )
        products.append(product)
    
    db.session.add_all(products)
    db.session.commit()
    
    print(f"Database seeded")

    
