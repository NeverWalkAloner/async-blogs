from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr, validator


class TokenBase(BaseModel):
    token: UUID4
    expires: datetime

    class Config:
        orm_mode = True

    @validator("token")
    def hexlify_token(cls, value):
        return value.hex


class UserBase(BaseModel):
    id: int
    email: EmailStr
    name: str


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class User(UserBase):
    token: TokenBase = {}
