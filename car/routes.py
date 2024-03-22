from fastapi import APIRouter, HTTPException, status
from .models import Car
from .schemas import CarSchema, CarGetSchema, CarUpdateSchema
import logging
from fastapi import Query
from typing import Optional,List
from mongoengine.queryset.visitor import Q


router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/", response_model=dict)
def create_car(car: CarSchema):
    try:
        new_car = Car(make=car.make,model=car.model,engine_capacity=car.engine_capacity,
                      power=car.power,torque=car.torque,user=str(car.user))
        new_car.save()
        return {"message":"Added Successfully"}    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

# @router.put("/", response_model=dict)
# def update_cars(cars_data: CarUpdateSchema):
    
@router.put("/{car_id}", response_model=dict)
def update_car(car_id: str, car_data: CarUpdateSchema):
    try:
        car = Car.objects(id=car_id).first()
        if not car:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

        for field, value in car_data.dict().items():
            if value is not None:
                setattr(car, field, value)

        car.save()

        return {"message": "Car updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{car_id}", response_model=dict)
def delete_car(car_id: str):
    try:
        car = Car.objects(id=car_id).first()
        if not car:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
        
        car.delete()
        
        return {"message": "Car deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

@router.get("/filter", response_model=List[CarGetSchema])
def filter_cars(make: Optional[str] = None,
                model: Optional[str] = None,
                min_engine_capacity: Optional[float] = None,
                max_engine_capacity: Optional[float] = None,
                min_power: Optional[int] = None,
                max_power: Optional[int] = None,
                min_torque: Optional[int] = None,
                max_torque: Optional[int] = None):
    try:
        query_params = {}

        if make:
            query_params["make__icontains"] = make
        if model:
            query_params["model__icontains"] = model
        if min_engine_capacity:
            query_params["engine_capacity__gte"] = min_engine_capacity
        if max_engine_capacity:
            query_params["engine_capacity__lte"] = max_engine_capacity
        if min_power:
            query_params["power__gte"] = min_power
        if max_power:
            query_params["power__lte"] = max_power
        if min_torque:
            query_params["torque__gte"] = min_torque
        if max_torque:
            query_params["torque__lte"] = max_torque

        filtered_cars = Car.objects(**query_params)
        
        serialized_results = []
        for car in filtered_cars:
            car_data = car.to_mongo().to_dict()
            car_data['_id'] = str(car.id)
            serialized_results.append(CarGetSchema(**car_data))

        return serialized_results
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

# @router.get("/search/", response_model=List[CarSchema])
# def search_cars(keyword: str):
#     logger.info("jj",keyword)
#     try:
#         # Define a query to search for cars where the make or model contains the keyword
#         query = {
#             "$or": [
#                 {"make__icontains": keyword},
#                 {"model__icontains": keyword}
#             ]
#         }
        
#         # Perform the search using the defined query
#         search_results = Car.objects(__raw__=query)
#         logger.info("seea",query)
        
#         return search_results
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/search/", response_model=List[CarGetSchema])
def search_cars(keyword: str):
    try:
        query = Q(make__icontains=keyword) | Q(model__icontains=keyword)
        search_results = Car.objects(query)
        
        serialized_results = []
        for car in search_results:
            car_data = car.to_mongo().to_dict()
            car_data['_id'] = str(car.id)
            serialized_results.append(CarGetSchema(**car_data))
        
        return serialized_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))