from flask import Blueprint, jsonify

bp = Blueprint('test', __name__)

@bp.route('/api/test')
def test():
    return jsonify(message='Hello from Flask backend')
