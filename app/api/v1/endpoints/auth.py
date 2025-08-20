from fastapi import APIRouter, Depends, HTTPException, Request, status, Response, BackgroundTasks
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from datetime import timedelta

from app.models.user import User
from app.db.database import get_db
from app.utils.password import verify_password
from app.utils.security import create_access_token
from app.core.config import settings

from app.schemas.user import UserRegisterRequest
from app.utils.password import get_password_hash

router = APIRouter()


@router.post("/auth/login")
async def login_user(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Аутентификация пользователя
    Принимает email и password, возвращает JWT токен и данные пользователя.
    """

    print("Login user...")
    json_data = await request.json()
    print(f"json_data {json_data}")
    email, password = json_data.get("username"), json_data.get("password")

    if not email or not password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email and password required")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    print(f"Создание токена...")
    access_token = await create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "user_id": user.id,
            "email": user.email,
            "access_token": access_token,
            "token_type": "bearer",
            "redirect_url": "/"
            }
        )

    # response.set_cookie(
    #     key="access_token",
    #     value=f"Bearer {access_token}",
    #     httponly=True,
    #     secure=True,
    #     samesite='lax',
    #     max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    # )

    return response


# @router.get("/api/v1/auth/logout")
# async def logout(response: Response):
#     """
#     Удаляет куки для выхода пользователя
#     :param response:
#     :return:
#     """
#
#     response.delete_cookie("access_token")
#     return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Logged out"})


@router.post("/auth/registration")
async def register_user(user_data: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    """
    Регистрация нового пользователя

    Принимает данные пользователя, создает запись в БД и возвращает данные созданного пользователя.
    """

    existing_user = await db.execute(select(User).where(User.email == user_data.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        hashed_password=hashed_password
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=dict(user_data))


# @router.post("/auth/reset-password")
# async def reset_password(
#         data: ResetPasswordRequest,
#         db: AsyncSession = Depends(get_db)):
#
#     email = await verify_password_by_token(data.token)
#     if not email:
#         return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             content="Invalid or expired token"
#         )
#
#     user = await db.execute(select(User).where(email == User.email))
#     user = user.scalar_one_or_none()
#     print(data)
#     user.hashed_password = get_password_hash(data.new_password)
#
#     await db.commit()
#
#     return {"message": "Password updated"}
