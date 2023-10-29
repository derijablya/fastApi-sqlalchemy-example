from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Users


async def verify_email_exists(email: str, repository: AsyncSession) -> Optional[Users]:
    return await repository.get(Users, email)
