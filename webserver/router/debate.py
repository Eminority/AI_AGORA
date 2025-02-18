from fastapi import APIRouter, Path, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
import httpx
import config
import os
import requests
router = APIRouter()
templates = Jinja2Templates(directory="templates")

#pydantic 모델 정의


##토론장 입장
# 이 때 기록 받아와서 현재까지 진행된 토론 보이기
@router.get("/debate")
async def get_debate(request:Request):
    return templates.TemplateResponse("debate.html", {"request":request})

#토론 정보 가져오기
@router.get("/debate/info")
async def get_debate_info(id:str):
    url = f"{config.debate_server_uri}/debate/info?id={id}"
    with httpx.Client() as client:
        response = client.get(url)
    result = response.json()
    posimg = result["participants"]["pos"]["img"]
    negimg = result["participants"]["neg"]["img"]
    print(result, flush=True)
    posimg = await download_image_if_not_exists(posimg)
    negimg = await download_image_if_not_exists(negimg)

    result["participants"]["pos"]["img"] = posimg
    result["participants"]["neg"]["img"] = negimg
    
    return result

async def download_image_if_not_exists(image_name: str):
    """이미지가 로컬에 없으면 A 서버에서 다운로드"""
    image_path = os.path.join(os.getcwd(), f"static\\img\\profile\\{image_name}")
    print(image_path, flush=True)
    if os.path.exists(image_path):
        return image_name  # 이미 존재하면 그대로 반환

    image_url = f"{config.debate_server_uri}/image/{image_name}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(image_url)

            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")
                if "image" not in content_type:
                    raise HTTPException(status_code=404, detail=f"잘못된 응답: {content_type}")

                # 이미지 저장
                with open(image_path, "wb") as f:
                    f.write(response.content)

                print(f"✅ {image_name} 다운로드 완료!")
                return image_name  # 정상 저장되었으면 원래 파일명 반환

        except httpx.RequestError as e:
            print(f"❌ {image_name} 다운로드 실패: {e}")

    return "default.png"  # 실패 시 기본 이미지 반환



##토론 만들기
@router.post("/debate/create")
async def create_debate(pos_id:str=Form(...),
                        neg_id:str=Form(...),
                        topic:str=Form(...)):
    print(pos_id, neg_id, topic)
    url = f"{config.debate_server_uri}/debate"
    with httpx.Client() as client:
        response = client.post(
            url,
            data={ "pos_id" : pos_id,
                    "neg_id" : neg_id,
                    "topic" : topic
                },
            timeout=100)
    return response.json()

#토론 진행하기
@router.post("/debate/progress")
async def progress_debate(request:Request):
    url = f"{config.debate_server_uri}/debate/progress"
    body = await request.body()
    content_type = request.headers.get("Content-Type", "application/x-www-form-urlencoded")
    headers = {"Content-Type" : content_type}
    with httpx.Client() as client:
        response = client.post(url, headers=headers, content=body, timeout=20)
    return response.json()


#토론 목록 받아오기
@router.get("/debate/list")
async def get_debate_list():
    url = f"{config.debate_server_uri}/debate/list"
    with httpx.Client() as client:
        response = client.get(url)
    debate_list = response.json()
    return debate_list
