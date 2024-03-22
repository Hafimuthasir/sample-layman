from mongoengine import Document, StringField, FloatField, IntField, ReferenceField
from app.models import User

class Car(Document):
    make = StringField(required=True)
    model = StringField(required=True)
    engine_capacity = FloatField(required=True)
    power = IntField(required=True)
    torque = IntField(required=True)
    user = ReferenceField(User, required=True)