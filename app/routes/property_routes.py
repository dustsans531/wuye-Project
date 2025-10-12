from flask import jsonify, request
from .. import db
from ..models.property import Property
from . import api_bp

@api_bp.route('/properties', methods=['GET'])
def get_properties():
    properties = Property.query.all()
    return jsonify([property.to_dict() for property in properties])

@api_bp.route('/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    property = Property.query.get_or_404(property_id)
    return jsonify(property.to_dict())

@api_bp.route('/properties', methods=['POST'])
def create_property():
    data = request.get_json() or {}
    
    # 检查必要字段
    if 'name' not in data or 'address' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # 创建新物业
    property = Property()
    property.name = data['name']
    property.address = data['address']
    
    # 设置可选字段
    if 'city' in data:
        property.city = data['city']
    if 'district' in data:
        property.district = data['district']
    if 'zip_code' in data:
        property.zip_code = data['zip_code']
    if 'property_type' in data:
        property.property_type = data['property_type']
    if 'total_buildings' in data:
        property.total_buildings = data['total_buildings']
    if 'total_units' in data:
        property.total_units = data['total_units']
    if 'management_fee_rate' in data:
        property.management_fee_rate = data['management_fee_rate']
    if 'contact_person' in data:
        property.contact_person = data['contact_person']
    if 'contact_phone' in data:
        property.contact_phone = data['contact_phone']
    
    db.session.add(property)
    db.session.commit()
    
    return jsonify(property.to_dict()), 201

@api_bp.route('/properties/<int:property_id>', methods=['PUT'])
def update_property(property_id):
    property = Property.query.get_or_404(property_id)
    data = request.get_json() or {}
    
    # 更新字段
    if 'name' in data:
        property.name = data['name']
    if 'address' in data:
        property.address = data['address']
    if 'city' in data:
        property.city = data['city']
    if 'district' in data:
        property.district = data['district']
    if 'zip_code' in data:
        property.zip_code = data['zip_code']
    if 'property_type' in data:
        property.property_type = data['property_type']
    if 'total_buildings' in data:
        property.total_buildings = data['total_buildings']
    if 'total_units' in data:
        property.total_units = data['total_units']
    if 'management_fee_rate' in data:
        property.management_fee_rate = data['management_fee_rate']
    if 'contact_person' in data:
        property.contact_person = data['contact_person']
    if 'contact_phone' in data:
        property.contact_phone = data['contact_phone']
    if 'active' in data:
        property.active = data['active']
    
    db.session.commit()
    
    return jsonify(property.to_dict())

@api_bp.route('/properties/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    property = Property.query.get_or_404(property_id)
    # 软删除，设置为非活动状态
    property.active = False
    db.session.commit()
    
    return jsonify({'message': 'Property deactivated'}), 200