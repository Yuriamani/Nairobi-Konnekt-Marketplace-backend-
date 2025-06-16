from flask import Blueprint, request
from server import db
from .models import Product
from flask_restful import Api, Resource

products = Blueprint("products", __name__)
api_rest = Api(products)

class Products(Resource):
    def get(self):
        products = Product.query.all()
        return [product.to_dict() for product in products], 200

    def post(self):
        data = request.json
        required_fields = ['name', 'price',]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return {"error": f"Missing required fields: {missing_fields}"}, 400
        product = Product(vendor_id=data['vendor_id'], name=data['name'], description=data.get('description'), price=data['price'], category=data['category'], stock_quantity=data.get('stock_quantity'), image_url=data['image_url'], is_active=data.get('is_active'))
        db.session.add(product)
        db.session.commit()
        return product.to_dict(), 201

class Products(Resource):
    def get(self):
        # Parse query params
        limit = min(int(request.args.get('limit', 10)), 50)  # Cap limit to 50
        cursor = request.args.get('cursor', None, type=int)  # Cursor is the last seen ID
        category = request.args.get('category', None)         # Filter by category
        
        # Base query (ordered by cursor field)
        query = Product.query.order_by(Product.id.asc())

        # Apply category filter (if provided)
        if category:
            query = query.filter(Product.category == category)
        
        # Apply cursor filter (fetch items AFTER the cursor)
        if cursor:
            query = query.filter(Product.id > cursor)
        
        # Fetch results
        products = query.limit(limit).all()
        
        # Determine next cursor (last item's ID in this batch)
        next_cursor = products[-1].id if products else None
        
        return {
            'items': [p.to_dict() for p in products],
            'next_cursor': next_cursor , # Pass this to the frontend
            'category': category
        }    
    
    
class ProductResource(Resource):
    def get(self, id):
        if id is None:
            return {'error': 'Missing product ID'}, 400

        product = Product.query.get(id)
        if product is None:
            return {'error': 'Product not found'}, 404
        return product.to_dict(), 200
    
    def patch(self, id):
        data = request.json
        if id is None:
            return {'error': 'Missing product ID'}, 400

        product = Product.query.get(id)
        if product is None:
            return {'error': 'Product not found'}, 404

        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']
        if 'category' in data:
            product.category = data['category']
        if 'stock_quantity' in data:
            product.stock_quantity = data['stock_quantity']
        if 'image_url' in data:
            product.image_url = data['image_url']
        if 'is_active' in data:
            product.is_active = data['is_active']
        if 'created_at' in data:
            product.created_at = data['created_at']    

        db.session.commit()
        return product.to_dict(), 200

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
api_rest.add_resource(Products, "/products")