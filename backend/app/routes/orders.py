from flask import Blueprint, request, jsonify
from app.models import Order, LineItem, MenuItem
from app import db
from datetime import datetime

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/', methods=['POST'])
def create_order():
    data = request.json
    order = Order(timestamp=datetime.utcnow(), payment_method=data['payment_method'])
    db.session.add(order)
    db.session.commit()

    for item in data['items']:
        line = LineItem(order_id=order.id, menu_item_id=item['menu_item_id'], quantity=item['quantity'])
        db.session.add(line)
    db.session.commit()

    return jsonify({'message': 'Order placed successfully'})
