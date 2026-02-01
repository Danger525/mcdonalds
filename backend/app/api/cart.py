from flask import Blueprint, request, jsonify
from app.extensions import cache
import uuid

cart_bp = Blueprint('cart', __name__)

# Helper to get cart key
def get_cart_key():
    # Use user ID if authenticated, else session ID/device ID from header
    # For demo, we'll try 'X-Session-ID' or generate one
    session_id = request.headers.get('X-Session-ID')
    if not session_id:
        return None # Require session ID for guest carts
    return f"cart:{session_id}"

@cart_bp.route('/', methods=['GET'])
def get_cart():
    key = get_cart_key()
    if not key:
        return jsonify({"message": "X-Session-ID header required"}), 400
        
    cart_data = cache.get(key)
    if not cart_data:
        return jsonify({"items": [], "total": 0}), 200
        
    return jsonify(cart_data), 200

@cart_bp.route('/items', methods=['POST'])
def add_item():
    key = get_cart_key()
    if not key:
        return jsonify({"message": "X-Session-ID header required"}), 400
        
    data = request.get_json()
    item_id = data.get('menu_item_id')
    qty = data.get('quantity', 1)
    
    # Simple Cart Structure: {'items': [{'id': 1, 'qty': 2, ...}], 'total': 0}
    cart = cache.get(key) or {'items': [], 'total': 0}
    
    # Check if item exists in cart
    existing = next((i for i in cart['items'] if i['id'] == item_id), None)
    if existing:
        existing['qty'] += qty
    else:
        # Fetch item details (snapshot)
        from app.models import MenuItem
        menu_item = MenuItem.query.get(item_id)
        if not menu_item:
             return jsonify({"message": "Item not found"}), 404
             
        cart['items'].append({
            'id': menu_item.id,
            'name': menu_item.name,
            'price': float(menu_item.price),
            'qty': qty
        })
    
    # Recalculate total
    cart['total'] = sum(i['price'] * i['qty'] for i in cart['items'])
    
    # Save back to Redis (TTL 24h)
    cache.set(key, cart, timeout=86400)
    
    return jsonify(cart), 200

@cart_bp.route('/', methods=['DELETE'])
def clear_cart():
    key = get_cart_key()
    if key:
        cache.delete(key)
    return jsonify({"message": "Cart cleared"}), 200
