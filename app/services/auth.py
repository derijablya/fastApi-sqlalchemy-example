from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app import services
from app.serializers.users import UserOut
from app.services.utils.hashing import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Auth:
    def __init__(
        self,
        users_service: services.Users = Depends(),
    ):
        self.users_service = users_service

    async def check_credentials(self, data: OAuth2PasswordRequestForm):
        user = await self.users_service.get_user_by_name(data.username)
        print(data.password)
        print(user.password)
        if not user:
            return False
        if not verify_password(data.password, user.password):
            return False
        return UserOut(id=user.id, username=user.username, email=user.email)
