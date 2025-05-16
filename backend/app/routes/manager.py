from flask import Blueprint, request, jsonify
from models import db, Employee, Manager, Accounting

manager_bp = Blueprint('manager', __name__)

@manager_bp.route('/employees', methods=['GET'])
def list_employees():
    employees = Employee.query.all()
    return jsonify([{
        "ssn": e.ssn,
        "name": e.name,
        "email": e.email,
        "salary": float(e.salary)
    } for e in employees])

@manager_bp.route('/employee', methods=['POST'])
def add_employee():
    data = request.json
    employee = Employee(
        ssn=data['ssn'],
        name=data['name'],
        email=data['email'],
        salary=data['salary']
    )
    db.session.add(employee)
    db.session.commit()
    
    return jsonify({"message": "Employee added."}), 201
