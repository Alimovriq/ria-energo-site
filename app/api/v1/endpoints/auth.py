from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import timedelta

from app.models.user import User
from app.db.database import get_db
from app.utils.password import verify_password
from app.utils.security import create_access_token
from app.db.config import settings
from app.utils.security import get_current_user
from app.schemas.utils import TokenResponse

from app.schemas.user import UserRegisterRequest, UserUpdateRequest
from app.utils.password import get_password_hash

router = APIRouter()


@router.post("/api/v1/auth/login")
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
    access_token = create_access_token(
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


@router.post("/api/v1/auth/registration")
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


@router.patch("/api/v1/auth/me", response_model=UserUpdateRequest)
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