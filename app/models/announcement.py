from datetime import datetime
from .. import db

class Announcement(db.Model):
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    expire_date = db.Column(db.DateTime)
    is_published = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # 外键
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    
    # 关系
    # 可以根据需要添加与其他模型的关系
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'publish_date': self.publish_date.isoformat() if self.publish_date else None,
            'expire_date': self.expire_date.isoformat() if self.expire_date else None,
            'is_published': self.is_published,
            'created_by': self.created_by,
            'property_id': self.property_id
        }
    
    def __repr__(self):
        return '<Announcement {}>'.format(self.title)