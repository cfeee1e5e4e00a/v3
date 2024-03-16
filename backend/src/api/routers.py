from fastapi import APIRouter

log_router = APIRouter(prefix="/log", tags=["log", "logs"])
example_router = APIRouter(prefix="/example", tags=["example"])
