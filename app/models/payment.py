from datetime import datetime
from .. import db

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    payment_type = db.Column(db.String(50), nullable=False)  # 物业费、水电费、维修费等
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date)
    payment_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='unpaid')  # unpaid, paid, partial, overdue
    payment_method = db.Column(db.String(50))  # 微信支付、支付宝、现金、银行转账等
    transaction_id = db.Column(db.String(100))
    notes = db.Column(db.Text)
    
    # 外键
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))
    
    # 关系
    # 可以根据需要添加与其他模型的关系
    
    def to_dict(self):
        return {
            'id': self.id,
            'payment_type': self.payment_type,
            'amount': self.amount,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'status': self.status,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'notes': self.notes,
            'owner_id': self.owner_id,
            'property_id': self.property_id
        }
    
    def __repr__(self):
        return '<Payment #{}>'.format(self.id)