from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates")


@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """
    Эндпоинт для гет запроса страницы о компании
    :param request: запрос
    :return: страница о компании
    """

    return templates.TemplateResponse(
        "about.html", {"request": request, "title": "РИА-Энерго", "is_main_page": False})