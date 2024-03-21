from .endpoints.auth import auth_router, create_user, get_user
from .endpoints.log import router as log_router
from .endpoints.mqtt import router as mqtt_router, mqtt
from .endpoints.flats import flats_router
from .endpoints.bill import bill_router

routers = [auth_router, log_router, mqtt_router, flats_router, bill_router]
