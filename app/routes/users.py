from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import services
from app.repository import postgres
from app.serializers import User
from app.serializers.users import UserIn
from app.services.utils import validator

router = APIRouter(
    tags=["Users"],
    prefix="/users",
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserIn | None,
)
async def create_user(
        request: User,
        service: services.Users = Depends(),
        repository: AsyncSession = Depends(postgres.get_session)
):
    user = await validator.verify_email_exists(request.email, repository)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )
    return await service.create_user(request)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[UserIn] | None,
)
async def get_users(
        service: services.Users = Depends(),
):
    return await service.get_users()


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserIn | None,
)
async def get_user_by_id(
        user_id: int,
        service: services.Users = Depends(),
):
    return await service.get_user_by_id(user_id)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
        user_id: int,
        service: services.Users = Depends(),
):
    await service.delete_user(user_id)
