from datetime import datetime
from .. import db

class Maintenance(db.Model):
    __tablename__ = 'maintenance'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_date = db.Column(db.DateTime)
    completion_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, cancelled
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, emergency
    cost = db.Column(db.Float)
    notes = db.Column(db.Text)
    
    # 外键
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # 关系
    # 可以根据需要添加与其他模型的关系
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'request_date': self.request_date.isoformat(),
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'status': self.status,
            'priority': self.priority,
            'cost': self.cost,
            'notes': self.notes,
            'owner_id': self.owner_id,
            'property_id': self.property_id,
            'assigned_to': self.assigned_to
        }
    
    def __repr__(self):
        return '<Maintenance #{}>'.format(self.id)