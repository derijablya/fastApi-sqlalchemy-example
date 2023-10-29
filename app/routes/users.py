from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import services
from app.repository import postgres
from app.serializers import User
from app.services.utils import validator

router = APIRouter(
    tags=["Users"],
    prefix="/users",
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
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
