from datetime import datetime
from .. import db

class Owner(db.Model):
    __tablename__ = 'owners'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    id_card = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    gender = db.Column(db.String(10))
    birth_date = db.Column(db.Date)
    emergency_contact = db.Column(db.String(64))
    emergency_phone = db.Column(db.String(20))
    move_in_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 外键
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    unit_number = db.Column(db.String(20))  # 单元号
    
    # 关系
    payments = db.relationship('Payment', backref='owner', lazy='dynamic')
    maintenance_requests = db.relationship('Maintenance', backref='owner', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'id_card': self.id_card,
            'phone': self.phone,
            'email': self.email,
            'gender': self.gender,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'emergency_contact': self.emergency_contact,
            'emergency_phone': self.emergency_phone,
            'move_in_date': self.move_in_date.isoformat() if self.move_in_date else None,
            'property_id': self.property_id,
            'unit_number': self.unit_number,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return '<Owner {}>'.format(self.name)