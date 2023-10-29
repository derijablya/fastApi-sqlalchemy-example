import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Users


async def verify_email_exists(email: str, repository: AsyncSession) -> Optional[Users]:
    try:
        stmt = select(select(Users).where(Users.email == email).exists())
        return await repository.scalar(stmt)
    except Exception as e:
        logging.exception(e, exc_info=True)
