from flask import Blueprint, request
from flask_restful import Api, Resource
from server import db
from ..models import Product, Vendor
from sqlalchemy import func

main = Blueprint('main', __name__)
api_rest = Api(main)

class Home(Resource):
    def get(self):
        return {'msg': 'E-commerce Flask Backend'}, 200

class Products(Resource):
    def get(self):
        # Parse query params
        limit = min(int(request.args.get('limit', 10)), 50)  # Cap limit to 50
        cursor = request.args.get('cursor', None, type=int)  # Cursor is the last seen ID
        category = request.args.get('category', None)
        section = request.args.get('section', None)
        search = request.args.get('search', default=None)
        
        # Base query (ordered by cursor field)
        query = Product.query.order_by(Product.id.asc())

        # Apply category filter (if provided)
        if category:
            query = query.filter(Product.category == category)

                # Validate parameters and filter by section
        if section:
            if section not in ['featured', 'new-arrivals', 'best-sellers']:
                return {'error': 'Invalid section'}, 400
            if section == 'featured':
                query = query.filter(Product.is_featured == True)
            elif section == 'new-arrivals':
                query = query.filter(Product.is_new_arrival == True)
            elif section == 'best-sellers':
                query = query.filter(Product.is_best_seller == True)    

        if search:
            query = query.filter(
                Product.name.ilike(f'%{search}%') | 
                Product.description.ilike(f'%{search}%')
                # For JSON array fields
                # func.jsonb_array_elements_text(Product.tags).ilike(f'%{search}%')
            )      
        
        # Apply cursor filter (fetch items AFTER the cursor)
        if cursor:
            query = query.filter(Product.id > cursor)
        
        # Fetch results
        products = query.limit(limit).all()
        
        # Determine next cursor (last item's ID in this batch)
        next_cursor = products[-1].id if products else None
        
        return {
            'items': [p.to_dict() for p in products],
            'next_cursor': next_cursor,  # Pass this to the frontend
            'category': category,
            'section': section
        }

    def post(self):
        data = request.json
        # Required fields validation
        required_fields = ['name', 'price', 'vendor_id', 'category']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return {"error": f"Missing required fields: {missing_fields}"}, 400
        try:
            # Check if vendor exists
            vendor = Vendor.query.get(data['vendor_id'])
            if not vendor:
                return {"error": "Vendor not found"}, 404
            
            # Create product with relationship
            product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price']),
            original_price=float(data.get('original_price', data['price'])),
            images=data.get('images', []),
            rating=float(data.get('rating', 0)),
            review_count=int(data.get('review_count', 0)),
            vendor_id=data['vendor_id'],
            category=data['category'],
            sub_category=data.get('sub_category', ''),
            tags=data.get('tags', []),
            stock=int(data.get('stock', 0)),
            features=data.get('features', {}),
            specifications=data.get('specifications', {}),
            is_featured=bool(data.get('is_featured', False)),
            is_new_arrival=bool(data.get('is_new_arrival', False)),
            is_best_seller=bool(data.get('is_best_seller', False))
        )
            db.session.add(product)
            db.session.commit()
            return product.to_dict(), 201  
        except ValueError as e:
            return {"error": f"Invalid data format: {str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": f"Server error: {str(e)}"}, 500  
    
class ProductCategory(Resource):
    def get(self):
        categories = db.session.query(Product.category.distinct()).all()
        return {'categories': [c[0] for c in categories if c[0]]  # Flatten and filter None
        }     
        
class ProductSectionsOverview(Resource):
    def get(self):
        # Get a small preview of each section (no pagination)
        featured = Product.query.filter(Product.is_featured == True).limit(5).all()
        new_arrivals = Product.query.filter(Product.is_new_arrival == True).limit(5).all()
        best_sellers = Product.query.filter(Product.is_best_seller == True).limit(5).all()
        
        return {
            'featuredProducts': [p.to_dict() for p in featured],
            'newArrivals': [p.to_dict() for p in new_arrivals],
            'bestSellers': [p.to_dict() for p in best_sellers]
        }
    
class ProductResource(Resource):
    def get(self, id):
        if id is None:
            return {'error': 'Missing product ID'}, 400

        product = Product.query.get(id)
        if product is None:
            return {'error': 'Product not found'}, 404
        
        related_products = (
            db.session.query(Product)
            .filter(
                Product.category == product.category,
                Product.id != product.id,
            )
            .limit(6)  # Return max 6 related products
            .all()
        )
        return {
            'related_products': [p.to_dict() for p in related_products],
            'product': product.to_dict()
        }, 200
    
    def patch(self, id):
        data = request.json
        if id is None:
            return {'error': 'Missing product ID'}, 400

        product = Product.query.get(id)
        if product is None:
            return {'error': 'Product not found'}, 404
        
        # Define allowed fields with their expected types (None means nullable)
        allowed_fields = {
        'name': (str,),  # Required field (no None allowed)
        'description': (str, type(None)),
        'price': (float, int),  # Required
        'original_price': (float, int, type(None)),
        'images': (list, type(None)),  # JSON array
        'rating': (float, int, type(None)),
        'review_count': (int, type(None)),
        'vendor_id': (str,),  # Required relationship
        'category': (str,),
        'sub_category': (str, type(None)),
        'tags': (list, type(None)),  # JSON array
        'stock': (int,),
        'features': (list, dict, type(None)),  # JSON field
        'specifications': (dict, type(None)),  # JSON object
        'is_featured': (bool,),
        'is_new_arrival': (bool,),
        'is_best_seller': (bool,)
    }

        errors = {}
        for field, field_types in allowed_fields.items():
            if field in data:
                # Check if value is None or matches allowed types
                if data[field] is not None and not isinstance(data[field], field_types):
                    errors[field] = f'Expected one of: {[t.__name__ for t in field_types]}'
                    continue
                
                setattr(product, field, data[field])

        if errors:
            return {'errors': errors}, 400

        try:
            db.session.commit()
            return product.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def delete(self, id):
        if id is None:
            return {'error': 'Missing product ID'}, 400

        product = Product.query.get(id)
        if product is None:
            return {'error': 'Product not found'}, 404

        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted successfully'}, 204   

api_rest.add_resource(ProductResource, "/products/<int:id>")
api_rest.add_resource(ProductCategory, "/categories")
api_rest.add_resource(Products, "/products")  
api_rest.add_resource(ProductSectionsOverview, '/products/overview')  

api_rest.add_resource(Home, '/')

# # Get all products
# @product_bp.route('/', methods=['GET'])
# def get_products():
#     products = Product.query.all()
#     return jsonify([{
#         'id': p.id,
#         'name': p.name,
#         'price': p.price,
#         'vendor_id': p.vendor_id,
#         'category': p.category
#     } for p in products])

# # Get featured/new/best-seller products
# @product_bp.route('/featured', methods=['GET'])
# def get_featured():
#     featured = Product.query.filter_by(is_featured=True).all()
#     return jsonify([p.to_dict() for p in featured])

# # Add a new product (for vendors later)
# @product_bp.route('/', methods=['POST'])
# def add_product():
#     data = request.get_json()
#     new_product = Product(
#         id=data['id'],
#         name=data['name'],
#         price=data['price'],
#         vendor_id=data['vendor_id'],
#         # ... other fields
#     )
#     db.session.add(new_product)
#     db.session.commit()
#     return jsonify({"message": "Product added!"}), 201

