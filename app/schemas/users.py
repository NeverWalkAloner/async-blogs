from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr, validator


class TokenBase(BaseModel):
    """ Return response data """
    token: UUID4
    expires: datetime

    class Config:
        orm_mode = True

    @validator("token")
    def hexlify_token(cls, value):
        """ Convert UUID to pure hex string """
        return value.hex


class UserBase(BaseModel):
    """ Return response data """
    id: int
    email: EmailStr
    name: str


class UserCreate(BaseModel):
    """ Validate request data """
    email: EmailStr
    name: str
    password: str


class User(UserBase):
    """ Return detailed response data with token """
    token: TokenBase = {}
