from fastapi import FastAPI
from app.routes import router as api_router
from car.routes import router as car_router
from mongoengine import connect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Connect to MongoDB
def connect_to_mongo():
    connect(db="testdb4", host="localhost")

connect_to_mongo()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
app.include_router(car_router, prefix="/api/cars")
