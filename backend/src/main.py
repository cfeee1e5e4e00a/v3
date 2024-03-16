from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.routers import router as auth_router
from src.api.routers import example_router, root_router

from src.core.config import LOGIN_CALLBACK_URI

app = FastAPI()

origins = [LOGIN_CALLBACK_URI]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "PUT", "GET", "DELETE"],
    allow_headers=["*"],
    max_age=3600,
)

app.include_router(root_router)
app.include_router(auth_router)
app.include_router(example_router)
