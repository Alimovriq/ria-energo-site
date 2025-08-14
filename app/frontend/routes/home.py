from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates")


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """
    Главная страница
    :param request:
    :return:
    """
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "title": "РИА-Энерго",
            "is_main_page": True,
            "page_class": "home-page"
        })