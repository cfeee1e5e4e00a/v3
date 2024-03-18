from .endpoints.auth import auth_router, create_user, get_user
from .endpoints.log import router as log_router
from .endpoints.example import router as example_router
from .endpoints.mqtt import router as mqtt_router, mqtt

routers = [auth_router, log_router, example_router, mqtt_router]
