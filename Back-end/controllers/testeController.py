from fastapi import APIRouter, Body,status


router = APIRouter()

@router.get('/',
             summary='teste',
             status_code=status.HTTP_200_OK,)
def post():
    return[
        {"conta_um" : 1}
    ]