from flask import jsonify, request
from datetime import datetime
from .. import db
from ..models.payment import Payment
from . import api_bp

@api_bp.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    return jsonify([payment.to_dict() for payment in payments])

@api_bp.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify(payment.to_dict())

@api_bp.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json() or {}
    
    # 检查必要字段
    if 'payment_type' not in data or 'amount' not in data or 'owner_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # 创建新支付记录
    payment = Payment()
    payment.payment_type = data['payment_type']
    payment.amount = data['amount']
    payment.owner_id = data['owner_id']
    
    # 设置可选字段
    if 'due_date' in data:
        payment.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
    if 'payment_date' in data:
        payment.payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%dT%H:%M:%S')
    if 'status' in data:
        payment.status = data['status']
    if 'payment_method' in data:
        payment.payment_method = data['payment_method']
    if 'transaction_id' in data:
        payment.transaction_id = data['transaction_id']
    if 'notes' in data:
        payment.notes = data['notes']
    if 'property_id' in data:
        payment.property_id = data['property_id']
    
    db.session.add(payment)
    db.session.commit()
    
    return jsonify(payment.to_dict()), 201

@api_bp.route('/payments/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    data = request.get_json() or {}
    
    # 更新字段
    if 'payment_type' in data:
        payment.payment_type = data['payment_type']
    if 'amount' in data:
        payment.amount = data['amount']
    if 'due_date' in data:
        payment.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
    if 'payment_date' in data:
        payment.payment_date = datetime.strptime(data['payment_date'], '%Y-%m-%dT%H:%M:%S')
    if 'status' in data:
        payment.status = data['status']
    if 'payment_method' in data:
        payment.payment_method = data['payment_method']
    if 'transaction_id' in data:
        payment.transaction_id = data['transaction_id']
    if 'notes' in data:
        payment.notes = data['notes']
    if 'property_id' in data:
        payment.property_id = data['property_id']
    
    db.session.commit()
    
    return jsonify(payment.to_dict())

@api_bp.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    
    return jsonify({'message': 'Payment record deleted'}), 204