from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from utils.jwt_manager import create_token
from schemas.user import User

user_router = APIRouter()

@user_router.post('/login', tags=['auth'])
def login(user: User):
    try:
        if user.email == "test@email.com" and user.password == "secret_Password":
            token: str = create_token(user.model_dump())
            return JSONResponse(status_code=status.HTTP_200_OK, content=token)

        raise JSONResponse(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})
    
