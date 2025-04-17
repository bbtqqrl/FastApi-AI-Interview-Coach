from typing import Annotated
from pydantic import BaseModel, EmailStr, ConfigDict
from annotated_types import MaxLen, MinLen
from uuid import UUID


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    password_hash: str

class UserCreate(BaseUser):
    pass

class Users(BaseUser):
    model_config = ConfigDict(from_attributes=True)
    id: UUID