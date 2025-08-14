from pydantic import BaseModel, EmailStr

from typing import Optional


# class UserBase(BaseModel):
#     email: EmailStr | str
#     first_name: str
#     last_name: str
#     phone: str
#
# class UserCreate(UserBase):
#     password: str
#
# class UserInDB(UserBase):
#     id: int
#     is_active: bool
#
#     class Config:
#         from_attributes  = True

# Модель для запроса регистрации
class UserRegisterRequest(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    password: str

# Модель для ответа
class UserRegisterResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None