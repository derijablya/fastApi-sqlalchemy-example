from fastapi import Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.logger import logger
from app import models, serializers
from app.repository.postgres import get_session
from app.serializers.users import UserOut


class Users:
    def __init__(self, repository: AsyncSession = Depends(get_session)):
        self.repository = repository
        self.model = models.Users

    async def create_user(self, request: serializers.User):
        try:
            new_user = self.model(
                username=request.username,
                email=request.email,
                password=request.password,
            )
            self.repository.add(new_user)
            await self.repository.commit()
            await self.repository.refresh(new_user)
            return UserOut(
                id=new_user.id, username=new_user.username, email=new_user.email
            )
        except Exception as e:
            logger.exception(e, exc_info=True)

    async def get_users(self):
        stmt = select(self.model)
        return await self.repository.scalars(stmt)

    async def get_user_by_id(self, user_id: int):
        try:
            user = await self.repository.get(self.model, user_id)
            if not user:
                return HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            logger.exception(e, exc_info=True)

    async def get_user_by_name(self, username: str):
        try:
            stmt = select(self.model).where(self.model.username == username)
            return await self.repository.scalar(stmt)
        except Exception as e:
            logger.exception(e, exc_info=True)

    async def delete_user(self, user_id: int):
        try:
            stmt = delete(self.model).where(self.model.id == user_id)
            await self.repository.execute(stmt)
            await self.repository.commit()
        except Exception as e:
            logger.exception(e, exc_info=True)
