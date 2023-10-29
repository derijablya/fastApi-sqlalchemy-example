import logging
from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, serializers
from app.repository.postgres import get_session
from app.serializers.users import UserIn


class Users:
    def __init__(self, repository: AsyncSession = Depends(get_session)):
        self.repository = repository

    async def create_user(self, request: serializers.User):
        try:
            stmt = select(models.Users.id, models.Users.username, models.Users.email).from_statement(
                insert(models.Users).values(request.model_dump()).
                returning(models.Users.id, models.Users.username, models.Users.email))
            result = await self.repository.execute(stmt)
            await self.repository.commit()
            return result.first()
        except Exception as e:
            logging.exception(e, exc_info=True)

    async def get_users(self):
        stmt = select(models.Users)
        return await self.repository.scalars(stmt)

    async def get_user_by_id(self, user_id: int):
        try:
            user = await self.repository.get(models.Users, user_id)
            if not user:
                return HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            logging.exception(e, exc_info=True)

    async def delete_user(self, user_id: int):
        try:
            stmt = delete(models.Users).where(models.Users.id == user_id)
            await self.repository.execute(stmt)
            await self.repository.commit()
        except Exception as e:
            logging.exception(e, exc_info=True)
