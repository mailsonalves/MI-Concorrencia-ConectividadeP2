from fastapi import APIRouter
from controllers.testeController import router
api_router = APIRouter()

api_router.include_router(router, prefix='/teste', tags=['teste'])