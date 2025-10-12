from flask import jsonify, request
from datetime import datetime
from .. import db
from ..models.announcement import Announcement
from . import api_bp

@api_bp.route('/announcements', methods=['GET'])
def get_announcements():
    announcements = Announcement.query.all()
    return jsonify([announcement.to_dict() for announcement in announcements])

@api_bp.route('/announcements/<int:announcement_id>', methods=['GET'])
def get_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    return jsonify(announcement.to_dict())

@api_bp.route('/announcements', methods=['POST'])
def create_announcement():
    data = request.get_json() or {}
    
    # 检查必要字段
    if 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # 创建新公告
    announcement = Announcement()
    announcement.title = data['title']
    announcement.content = data['content']
    
    # 设置可选字段
    if 'publish_date' in data:
        announcement.publish_date = datetime.strptime(data['publish_date'], '%Y-%m-%dT%H:%M:%S')
    if 'expire_date' in data:
        announcement.expire_date = datetime.strptime(data['expire_date'], '%Y-%m-%dT%H:%M:%S')
    if 'is_published' in data:
        announcement.is_published = data['is_published']
    if 'created_by' in data:
        announcement.created_by = data['created_by']
    if 'property_id' in data:
        announcement.property_id = data['property_id']
    
    db.session.add(announcement)
    db.session.commit()
    
    return jsonify(announcement.to_dict()), 201

@api_bp.route('/announcements/<int:announcement_id>', methods=['PUT'])
def update_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    data = request.get_json() or {}
    
    # 更新字段
    if 'title' in data:
        announcement.title = data['title']
    if 'content' in data:
        announcement.content = data['content']
    if 'publish_date' in data:
        announcement.publish_date = datetime.strptime(data['publish_date'], '%Y-%m-%dT%H:%M:%S')
    if 'expire_date' in data:
        announcement.expire_date = datetime.strptime(data['expire_date'], '%Y-%m-%dT%H:%M:%S')
    if 'is_published' in data:
        announcement.is_published = data['is_published']
    if 'created_by' in data:
        announcement.created_by = data['created_by']
    if 'property_id' in data:
        announcement.property_id = data['property_id']
    
    db.session.commit()
    
    return jsonify(announcement.to_dict())

@api_bp.route('/announcements/<int:announcement_id>', methods=['DELETE'])
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    db.session.delete(announcement)
    db.session.commit()
    
    return jsonify({'message': 'Announcement deleted'}), 204