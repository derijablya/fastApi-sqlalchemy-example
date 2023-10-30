from pydantic import BaseModel, constr, EmailStr


class User(BaseModel):
    username: constr(min_length=2, max_length=50)
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: constr(min_length=2, max_length=50)
    email: EmailStr
