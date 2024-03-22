from pydantic import BaseModel, constr, PositiveFloat, PositiveInt, Field
from typing import Optional, List
from bson import ObjectId

class CarSchema(BaseModel):
    make: str
    model: str
    engine_capacity: float
    power: int
    torque: int
    user: str

    class Config:
        orm_mode = True

class CarUpdateSchema(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    engine_capacity: Optional[float] = None
    power: Optional[int] = None
    torque: Optional[int] = None
    user: Optional[str] = None



# class CarCreateSchema(CarBaseSchema):
#     pass

# class CarUpdateSchema(CarBaseSchema):
#     pass
class CarGetSchema(BaseModel):
    id: Optional[str] = Field(alias='_id')
    make: str
    model: str
    engine_capacity: float
    power: int
    torque: int

    class Config:
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True

class CarInDBSchema(CarSchema):
    name: str

    class Config:
        orm_mode = True
