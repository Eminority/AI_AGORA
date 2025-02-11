from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import httpx
import config

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/lobby")
async def lobby(request: Request):
    return templates.TemplateResponse("lobby.html", {"request": request})

@router.get("/lobby/create")
async def lobby_create_debate(request:Request):
    return templates.TemplateResponse("lobby_create_profile.html", {"request":request})