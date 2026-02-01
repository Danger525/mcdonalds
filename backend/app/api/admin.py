from . import admin_bp
from flask import request, jsonify
from app import db
from app.models import Order, User, MenuItem
from app.utils.decorators import admin_required, staff_required
from sqlalchemy import func

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    total_orders = Order.query.count()
    total_sales = db.session.query(func.sum(Order.total_amount)).scalar() or 0
    active_orders = Order.query.filter(Order.status.in_(['pending', 'preparing'])).count()
    
    return jsonify({
        "total_orders": total_orders,
        "total_sales": total_sales,
        "active_orders": active_orders
    }), 200

@admin_bp.route('/orders', methods=['GET'])
@staff_required
def list_orders():
    status = request.args.get('status')
    query = Order.query
    if status:
        query = query.filter_by(status=status)
        
    orders = query.order_by(Order.created_at.desc()).all()
    
    output = []
    for o in orders:
        output.append({
            "id": o.id,
            "table": o.table_number,
            "status": o.status.value,
            "total": o.total_amount,
            "created_at": o.created_at.isoformat(),
            "items_count": len(o.items)
        })
    return jsonify(output), 200

@admin_bp.route('/qr/<int:table_num>')
def generate_qr(table_num):
    # Publicly accessible to allow embedding in images easily, or secure if needed.
    # For kiosk mode, public is fine.
    import qrcode
    from flask import send_file
    from io import BytesIO
    
    # URL to the menu with table param
    # Dynamic host? For now assume localhost or use request.host_url
    url = f"{request.host_url}?table={table_num}"
    
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png')
