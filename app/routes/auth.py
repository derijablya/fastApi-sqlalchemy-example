from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import services
from app.services.utils.jwt import create_access_token

router = APIRouter(
    tags=["Auth"],
)


@router.post(
    "/login",
)
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    auth_service: services.Auth = Depends(),
):
    user = await auth_service.check_credentials(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    return {
        "access_token": create_access_token(user.model_dump()),
        "token_type": "bearer",
    }
