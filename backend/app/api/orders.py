from . import orders_bp
from flask import request, jsonify, current_app
from app import db
from app.models import Order, OrderItem, MenuItem, OrderStatus, Role
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request, get_jwt


@orders_bp.route('/', methods=['POST'])
def create_order():
    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except:
        pass

    data = request.get_json()
    items_data = data.get('items', [])
    table_number = data.get('table_number')
    branch_id = data.get('branch_id') # Should come from frontend context or kiosk config
    
    if not items_data:
        return jsonify({"message": "Items required"}), 400
        
    # Create Order
    import random
    order_num = str(random.randint(100, 999)) # Simple override for uniqueness probability
    
    order = Order(
        user_id=user_id, 
        table_number=table_number,
        branch_id=branch_id,
        status=OrderStatus.PENDING,
        total_amount=0,
        order_number=order_num # Assign a number
    )
    db.session.add(order)
    
    total = 0
    
    for item_data in items_data:
        menu_item_id = item_data.get('menu_item_id')
        qty = item_data.get('quantity', 1)
        
        menu_item = MenuItem.query.get(menu_item_id)
        if not menu_item or not menu_item.is_available:
            return jsonify({"message": f"Item {menu_item_id} unavailable"}), 400
            
        # Calculate price including modifiers (simplified for now)
        base_price = float(menu_item.price)
        # TODO: Process modifiers from item_data['modifiers']
        
        item_total = base_price * qty
        
        order_item = OrderItem(
            order=order,
            menu_item_id=menu_item.id,
            menu_item_name=menu_item.name,
            quantity=qty,
            unit_price=base_price,
            total_price=item_total,
            modifiers_snapshot=[] # placeholder
        )
        db.session.add(order_item)
        total += item_total
    
    order.total_amount = total
    db.session.commit()
    

    # Notify Kitchen
    from ..extensions import socketio
    if socketio:
        socketio.emit('kitchen_update', {"action": "new_order", "order_id": order.id}, to="kitchen_updates")
    
    return jsonify({"message": "Order placed", "order_id": order.id, "order_number": order.order_number}), 201


@orders_bp.route('/', methods=['GET'])
# @jwt_required() # Optional: Secure this in prod
def list_orders():
    # Simple list all for KDS
    # In prod, filter by branch, date, active status
    orders = Order.query.order_by(Order.created_at.desc()).limit(50).all()
    output = []
    for order in orders:
        output.append({
            "id": order.id,
            "order_number": order.order_number,
            "table_number": order.table_number,
            "status": order.status.value,
            "total": float(order.total_amount),
            "items": [
                {
                    "menu_item_name": item.menu_item_name,
                    "quantity": item.quantity
                } for item in order.items
            ],
            "created_at": order.created_at.isoformat()
        })
    return jsonify(output), 200


@orders_bp.route('/<int:id>', methods=['GET'])
def get_order_status(id):
    order = Order.query.get_or_404(id)
    return jsonify({
        "id": order.id,
        "status": order.status.value,
        "items": [
            {
                "name": item.menu_item_name, 
                "quantity": item.quantity,
                "total": float(item.total_price)
            } 
            for item in order.items
        ],
        "total": float(order.total_amount)
    }), 200

@orders_bp.route('/<int:id>/status', methods=['PUT'])
@jwt_required()
def update_status(id):
    claims = get_jwt()
    if claims.get('role') not in ['admin', 'manager', 'kitchen']:
         return jsonify({"message": "Unauthorized"}), 403

    order = Order.query.get_or_404(id)
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status:
        try:
            # Use Enum
            status_enum = OrderStatus(new_status)
            
            # Strict Transition
            order.transition_to(status_enum)
            

            # Emit Socket Event
            from ..extensions import socketio
            if socketio:
                # Notify user specific room
                socketio.emit('order_update', {"status": order.status.value, "order_id": order.id}, to=f"order_{order.id}")
                # Notify kitchen
                socketio.emit('kitchen_update', {"action": "update", "order_id": order.id, "status": order.status.value}, to="kitchen_updates")

            
        except ValueError as e:
             return jsonify({"message": str(e)}), 400
        
    return jsonify({"message": "Status updated", "status": order.status.value}), 200
