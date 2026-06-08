from app.extensions import db

class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Person {self.name}>'

class TomatoVariety(db.Model):
    __tablename__ = 'tomato_variety'
    __table_args__ = (
        db.UniqueConstraint('name', 'owner_id', name='uq_tomato_variety_name_owner'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(100), nullable=True)
    size = db.Column(db.String(100), nullable=True)
    origin = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    fallback_image_url = db.Column(db.String(255), nullable=True)
    
    # New fields for attribution and stock tracking
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)
    in_stock = db.Column(db.Boolean, default=True, nullable=False, server_default='1')

    # Relationships
    owner = db.relationship('Person', backref=db.backref('varieties', lazy=True))

    def __repr__(self):
        return f'<TomatoVariety {self.name}>'


