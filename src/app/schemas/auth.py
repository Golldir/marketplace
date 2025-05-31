from pydantic import BaseModel, EmailStr, Field
from pydantic.config import ConfigDict
class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserCreateSchema(UserBase):
    password: str = Field(..., min_length=8)

class UserInDBSchema(UserBase):
    hashed_password: str

class UserReadSchema(UserBase):
    id: int
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class LoginSchema(BaseModel):
    username: str
    password: str