from flask import Blueprint, request, jsonify
from app.models import Employee
from app import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    employee = Employee(**data)
    db.session.add(employee)
    db.session.commit()
    return jsonify({'message': 'Employee registered successfully'})