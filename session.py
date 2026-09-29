import json
from fastapi import APIRouter, Depends
from app.db import get_db
from app.dependencies import get_current_user

router = APIRouter(tags=["session"])

@router.get("/session-info")
def session_info(user=Depends(get_current_user)):
    return {"logged_in": True, "user": user}

@router.get("/history")
def history(user=Depends(get_current_user)):
    conn = get_db()
    rows = conn.execute(
        "SELECT id, planner, input_json, output_json, created_at FROM history WHERE user_id=? ORDER BY id DESC",
        (user["id"],)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
