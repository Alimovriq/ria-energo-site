from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="app/frontend/templates")


@router.get("/registration", response_class=HTMLResponse)
async def registration_page(request: Request):
    """
    о компании
    :param request:
    :return:
    """
    return templates.TemplateResponse(
        "registration.html",
        {"request": request,
         "title": "РИА-Энерго",
         "is_main_page": False,
         "page_class": "registration-page"
         })
