from fastapi import APIRouter, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
import httpx
import config

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/lobby")
async def lobby(request: Request):
    url = f"{config.debate_server_uri}/profile/list"
    with httpx.Client() as client:
        response = client.get(url)
    profiles = response.json()
    print(profiles)
    return templates.TemplateResponse("lobby.html", {"request": request, "profiles":profiles})

@router.get("/lobby/create")
async def lobby_create_debate(request:Request):
    url = f"{config.debate_server_uri}/profile/list"
    with httpx.Client() as client:
        response = client.get(url)
    profiles = response.json()
    return templates.TemplateResponse("lobby_create_debate.html", {"request":request, "profiles":profiles})


@router.post("/lobby/objectdetect")
async def list_from_object_detect(original_image: UploadFile = File(...)):
    url = f"{config.debate_server_uri}/profile/objectdetect"
    with httpx.Client() as client:
        response = client.post(url=url, data=original_image)
    return #response.json()

@router.post("/lobby/createprofile")
async def create_profile(request:Request, file: UploadFile = File(...)):
    url = f"{config.debate_server_uri}/profile/create"