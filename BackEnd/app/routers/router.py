from fastapi import APIRouter
from app.controllers.user_controller import router as user_router
from app.controllers.voo_controller import router as voo_controller
from app.controllers.auth_controller import router as auth_controller

api_router = APIRouter()

api_router.include_router(user_router, prefix="/user", tags=["User"])
api_router.include_router(auth_controller, prefix="/auth", tags=["Auth"])
api_router.include_router(voo_controller, prefix="/voo", tags=["voo"])
