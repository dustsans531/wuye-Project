from flask import jsonify, request
from datetime import datetime
from .. import db
from ..models.owner import Owner
from . import api_bp

@api_bp.route('/owners', methods=['GET'])
def get_owners():
    owners = Owner.query.all()
    return jsonify([owner.to_dict() for owner in owners])

@api_bp.route('/owners/<int:owner_id>', methods=['GET'])
def get_owner(owner_id):
    owner = Owner.query.get_or_404(owner_id)
    return jsonify(owner.to_dict())

@api_bp.route('/owners', methods=['POST'])
def create_owner():
    data = request.get_json() or {}
    
    # 检查必要字段
    if 'name' not in data or 'id_card' not in data or 'phone' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # 检查身份证是否已存在
    if Owner.query.filter_by(id_card=data['id_card']).first():
        return jsonify({'error': 'ID card already exists'}), 400
    
    # 创建新业主
    owner = Owner()
    owner.name = data['name']
    owner.id_card = data['id_card']
    owner.phone = data['phone']
    
    # 设置可选字段
    if 'email' in data:
        owner.email = data['email']
    if 'gender' in data:
        owner.gender = data['gender']
    if 'birth_date' in data:
        owner.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
    if 'emergency_contact' in data:
        owner.emergency_contact = data['emergency_contact']
    if 'emergency_phone' in data:
        owner.emergency_phone = data['emergency_phone']
    if 'move_in_date' in data:
        owner.move_in_date = datetime.strptime(data['move_in_date'], '%Y-%m-%d').date()
    if 'property_id' in data:
        owner.property_id = data['property_id']
    if 'unit_number' in data:
        owner.unit_number = data['unit_number']
    
    db.session.add(owner)
    db.session.commit()
    
    return jsonify(owner.to_dict()), 201

@api_bp.route('/owners/<int:owner_id>', methods=['PUT'])
def update_owner(owner_id):
    owner = Owner.query.get_or_404(owner_id)
    data = request.get_json() or {}
    
    # 更新字段
    if 'name' in data:
        owner.name = data['name']
    if 'id_card' in data and data['id_card'] != owner.id_card:
        if Owner.query.filter_by(id_card=data['id_card']).first():
            return jsonify({'error': 'ID card already exists'}), 400
        owner.id_card = data['id_card']
    if 'phone' in data:
        owner.phone = data['phone']
    if 'email' in data:
        owner.email = data['email']
    if 'gender' in data:
        owner.gender = data['gender']
    if 'birth_date' in data:
        owner.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
    if 'emergency_contact' in data:
        owner.emergency_contact = data['emergency_contact']
    if 'emergency_phone' in data:
        owner.emergency_phone = data['emergency_phone']
    if 'move_in_date' in data:
        owner.move_in_date = datetime.strptime(data['move_in_date'], '%Y-%m-%d').date()
    if 'property_id' in data:
        owner.property_id = data['property_id']
    if 'unit_number' in data:
        owner.unit_number = data['unit_number']
    
    db.session.commit()
    
    return jsonify(owner.to_dict())

@api_bp.route('/owners/<int:owner_id>', methods=['DELETE'])
def delete_owner(owner_id):
    owner = Owner.query.get_or_404(owner_id)
    db.session.delete(owner)
    db.session.commit()
    
    return jsonify({'message': 'Owner deleted'}), 204