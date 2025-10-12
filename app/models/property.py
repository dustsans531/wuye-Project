from datetime import datetime
from .. import db

class Property(db.Model):
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(64))
    district = db.Column(db.String(64))
    zip_code = db.Column(db.String(20))
    property_type = db.Column(db.String(50))  # 小区、写字楼、商场等
    total_buildings = db.Column(db.Integer)
    total_units = db.Column(db.Integer)
    management_fee_rate = db.Column(db.Float)
    contact_person = db.Column(db.String(64))
    contact_phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    
    # 关系
    owners = db.relationship('Owner', backref='property', lazy='dynamic')
    maintenance_records = db.relationship('Maintenance', backref='property', lazy='dynamic')
    announcements = db.relationship('Announcement', backref='property', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'district': self.district,
            'zip_code': self.zip_code,
            'property_type': self.property_type,
            'total_buildings': self.total_buildings,
            'total_units': self.total_units,
            'management_fee_rate': self.management_fee_rate,
            'contact_person': self.contact_person,
            'contact_phone': self.contact_phone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'active': self.active
        }
    
    def __repr__(self):
        return '<Property {}>'.format(self.name)