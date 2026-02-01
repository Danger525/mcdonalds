from . import menu_bp
from flask import request, jsonify
from app import db, cache
from app.models import MenuItem, Category
from app.utils.decorators import admin_required
from flask_jwt_extended import jwt_required

@menu_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)
def get_menu():
    items = MenuItem.query.filter_by(is_available=True).all()
    output = []
    
    # Optimize: Pre-fetch categories if possible, or caching handles it.
    # For now, simplistic loop is fine for N < 1000 items.
    
    for item in items:
        cat = Category.query.get(item.category_id)
        
        # Modifiers group logic could be added here
        
        output.append({
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": float(item.price), # Decimal to float
            "category": cat.name if cat else "Uncategorized",
            "image_url": item.image_url,
            "calories": item.calories
        })
    return jsonify(output), 200

@menu_bp.route('/', methods=['POST'])
@admin_required
def add_menu_item():
    data = request.get_json()
    
    # Category handling
    category = Category.query.filter_by(name=data['category']).first()
    if not category:
        category = Category(name=data['category'])
        db.session.add(category)
        db.session.commit()
    
    new_item = MenuItem(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        category_id=category.id,
        image_url=data.get('image_url', ''),
        # calories=data.get('calories')
    )
    
    db.session.add(new_item)
    db.session.commit()
    cache.clear()
    
    return jsonify({"message": "Menu item added"}), 201


@menu_bp.route('/<int:item_id>', methods=['PUT'])
@admin_required
def update_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    data = request.get_json()
    
    if 'name' in data:
        item.name = data['name']
    if 'description' in data:
        item.description = data['description']
    if 'price' in data:
        item.price = data['price']
    if 'image_url' in data:
        item.image_url = data['image_url']
    if 'is_available' in data:
        item.is_available = data['is_available']
        
    if 'category' in data:
        category = Category.query.filter_by(name=data['category']).first()
        if not category:
            category = Category(name=data['category'])
            db.session.add(category)
            db.session.commit()
        item.category_id = category.id
        
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Menu item updated"}), 200

@menu_bp.route('/<int:item_id>', methods=['DELETE'])
@admin_required
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    # Optional: Soft delete instead? 
    # item.is_available = False
    
    db.session.delete(item)
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Menu item deleted"}), 200

