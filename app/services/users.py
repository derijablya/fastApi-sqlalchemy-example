from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, serializers
from app.repository.postgres import get_session


class Users:
    def __init__(self, repository: AsyncSession = Depends(get_session)):
        self.repository = repository

    async def create_user(self, request: serializers.User):
        new_user = models.Users(
            name=request.name,
            email=request.email,
            password=request.password
        )
        self.repository.add(new_user)
        await self.repository.commit()
        await self.repository.refresh(new_user)
        return new_user
