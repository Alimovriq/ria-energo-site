from pydantic import BaseModel, EmailStr, field_validator

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


class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

    @field_validator("new_password")
    def validate_password(cls, password: str) -> str | None:
        if len(password) < 8:
            raise ValueError("Password is too short")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain one or more digit")
        if not any(char.isalpha() and char == char.upper() for char in password):
            raise ValueError("Password must contain one or more upper char")
        if not any(char.isalpha() and char == char.lower() for char in password):
            raise ValueError("Password must contain one or more lower char")
        if not any(symbol in password for symbol in set(".,/=-)(*&^%$#@!?^+_")):
            raise ValueError("Password must contain one or more symbol")
        return password


class ForgotPasswordRequest(BaseModel):
    email: EmailStr