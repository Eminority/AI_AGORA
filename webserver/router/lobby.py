from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import httpx
import config

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/lobby")
async def lobby(request: Request):
    return templates.TemplateResponse("lobby.html", {"request": request, "title":"TITLE TEST"})
