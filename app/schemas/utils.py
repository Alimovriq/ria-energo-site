from pydantic import BaseModel


# Модель для ответа
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str