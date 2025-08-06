# главная страница

# app/endpoints/main.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """
    Главная страница
    :param request:
    :return:
    """
    return templates.TemplateResponse("index.html", {"request": request, "title": "РИА-Энерго"})