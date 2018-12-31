from typing import Dict
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "items": [i.to_dict() for i in self.items.all()]
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by(cls, name) -> "StoreModel":
        return cls.query.filter_by(name=name).first()
