from fastapi import APIRouter, Depends, HTTPException, Request, status, Response, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, MessageType

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from datetime import timedelta

from app.models.user import User
from app.db.database import get_db

from app.utils.security import create_access_token
from app.core.config import settings
from app.core.email import email_conf
from app.utils.security import get_current_user

from app.schemas.user import UserUpdateRequest, ForgotPasswordRequest
from app.utils.password import get_password_hash

router = APIRouter()



@router.patch("/users/me", response_model=UserUpdateRequest)
async def update_user_me(
        update_data: UserUpdateRequest,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
    """
    Обновляет данные текущего пользователя.
    """

    update_values = {}

    if update_data.first_name is not None:
        update_values["first_name"] = update_data.first_name
    if update_data.last_name is not None:
        update_values["last_name"] = update_data.last_name
    if update_data.phone is not None:
        update_values["phone"] = update_data.phone
    if update_data.password is not None:
        update_values["password"] = get_password_hash(update_data.password)

    if not update_values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update")

    await db.execute(update(User).where(User.id == current_user.id).values(**update_values))
    await db.commit()

    result = await db.execute(select(User).where(User.id == current_user.id))
    updated_user = result.scalar_one_or_none()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "email": updated_user.email,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
            "phone": updated_user.phone,
        }
    )


@router.get("/users/me")
async def get_user_profile(user: User = Depends(get_current_user)):
    return user


@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_profile(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):

    await db.execute(delete(User).where(User.id == current_user.id))
    await db.commit()

    # return JSONResponse(
    #     status_code=status.HTTP_204_NO_CONTENT,
    #     content={"message": f"User was deleted"}
    # )

# Создать endpoint для восстановления пароля:
# автоматическая генерация пароля + сброс токена и отправка письма на email.

@router.post("/auth/forgot-password")
async def forgot_password(
        request: ForgotPasswordRequest,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_db)):

    email = request.email
    user = await db.execute(select(User).where(User.email == email))
    if not user.scalar_one_or_none():
        return {"message": "If email exists, reset link sent"}

    access_token = create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    reset_url =  f"https://localhost/reset-password?token={access_token}"
    message = MessageSchema(
        subject="Сброс пароля",
        recipients=[email],
        body=f"Перейдите по ссылке для сброса пароля: {reset_url}",
        subtype=MessageType.plain
    )

    background_tasks.add_task(FastMail(email_conf).send_message, message)

    return {"message": "Reset link sent"}