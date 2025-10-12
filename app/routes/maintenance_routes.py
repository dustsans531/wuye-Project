from flask import jsonify, request
from datetime import datetime
from .. import db
from ..models.maintenance import Maintenance
from . import api_bp

@api_bp.route('/maintenance', methods=['GET'])
def get_maintenance_records():
    maintenance_records = Maintenance.query.all()
    return jsonify([record.to_dict() for record in maintenance_records])

@api_bp.route('/maintenance/<int:record_id>', methods=['GET'])
def get_maintenance_record(record_id):
    record = Maintenance.query.get_or_404(record_id)
    return jsonify(record.to_dict())

@api_bp.route('/maintenance', methods=['POST'])
def create_maintenance_record():
    data = request.get_json() or {}
    
    # 检查必要字段
    if 'title' not in data or 'owner_id' not in data or 'property_id' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # 创建新维修请求
    record = Maintenance()
    record.title = data['title']
    record.owner_id = data['owner_id']
    record.property_id = data['property_id']
    
    # 设置可选字段
    if 'description' in data:
        record.description = data['description']
    if 'scheduled_date' in data:
        record.scheduled_date = datetime.strptime(data['scheduled_date'], '%Y-%m-%dT%H:%M:%S')
    if 'status' in data:
        record.status = data['status']
    if 'priority' in data:
        record.priority = data['priority']
    if 'cost' in data:
        record.cost = data['cost']
    if 'notes' in data:
        record.notes = data['notes']
    if 'assigned_to' in data:
        record.assigned_to = data['assigned_to']
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify(record.to_dict()), 201

@api_bp.route('/maintenance/<int:record_id>', methods=['PUT'])
def update_maintenance_record(record_id):
    record = Maintenance.query.get_or_404(record_id)
    data = request.get_json() or {}
    
    # 更新字段
    if 'title' in data:
        record.title = data['title']
    if 'description' in data:
        record.description = data['description']
    if 'scheduled_date' in data:
        record.scheduled_date = datetime.strptime(data['scheduled_date'], '%Y-%m-%dT%H:%M:%S')
    if 'completion_date' in data:
        record.completion_date = datetime.strptime(data['completion_date'], '%Y-%m-%dT%H:%M:%S')
    if 'status' in data:
        record.status = data['status']
    if 'priority' in data:
        record.priority = data['priority']
    if 'cost' in data:
        record.cost = data['cost']
    if 'notes' in data:
        record.notes = data['notes']
    if 'assigned_to' in data:
        record.assigned_to = data['assigned_to']
    
    db.session.commit()
    
    return jsonify(record.to_dict())

@api_bp.route('/maintenance/<int:record_id>', methods=['DELETE'])
def delete_maintenance_record(record_id):
    record = Maintenance.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    
    return jsonify({'message': 'Maintenance record deleted'}), 204