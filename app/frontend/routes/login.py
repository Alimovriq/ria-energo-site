from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request) :
    """
    Эндпоинт для гет зпроса страницы логина пользователя
    :param request: запрос
    :return: страница для логина пользователя
    """

    return templates.TemplateResponse(
        "login.html",
        {"request": request,
         "title": "РИА-Энерго",
         "is_main_page": False,
         "page_class": "login-page"
         })
