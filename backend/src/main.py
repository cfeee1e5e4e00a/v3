from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.routers import router as auth_router
from src.api.routers import example_router, log_router

from src.core.config import KeyCloakSettings

app = FastAPI()

origins = [KeyCloakSettings.login_callback_uri]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "PUT", "GET", "DELETE"],
    allow_headers=["*"],
    max_age=3600,
)

app.include_router(log_router)
app.include_router(auth_router)
app.include_router(example_router)
