import json
from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.db import get_db
from app.dependencies import get_current_user
from app.models.schemas import HomeRequest, PartyRequest
from app.services.gemini_service import generate_recommendation

router = APIRouter(tags=["planners"])

def save_history(user_id, planner, payload, result):
    conn = get_db()
    conn.execute(
        "INSERT INTO history(user_id,planner,input_json,output_json) VALUES(?,?,?,?)",
        (user_id, planner, json.dumps(payload), json.dumps(result))
    )
    conn.commit()
    conn.close()

@router.post("/generate-home")
def generate_home(payload: HomeRequest, user=Depends(get_current_user)):
    data = payload.model_dump()
    result = generate_recommendation("home", data)
    save_history(user["id"], "home", data, result)
    return result

@router.post("/generate-party")
def generate_party(payload: PartyRequest, user=Depends(get_current_user)):
    data = payload.model_dump()
    result = generate_recommendation("party", data)
    save_history(user["id"], "party", data, result)
    return result

@router.post("/generate-jewelry")
async def generate_jewelry(
    budget: float = Form(...),
    occasion: str = Form("Wedding"),
    style: str = Form("Elegant"),
    outfit_color: str = Form(""),
    image: UploadFile | None = File(default=None),
    user=Depends(get_current_user),
):
    data = {
        "budget": budget,
        "occasion": occasion,
        "style": style,
        "outfit_color": outfit_color or None,
    }
    image_bytes = await image.read() if image else None
    result = generate_recommendation(
        "jewelry",
        data,
        image_bytes=image_bytes,
        image_mime=image.content_type if image else None,
    )
    save_history(user["id"], "jewelry", data, result)
    return result
