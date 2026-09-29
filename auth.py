from fastapi import APIRouter, HTTPException
from app.db import get_db
from app.models.schemas import RegisterRequest, LoginRequest
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(tags=["auth"])

@router.post("/register")
def register(payload: RegisterRequest):
    conn = get_db()
    try:
        existing = conn.execute("SELECT id FROM users WHERE email=?", (payload.email,)).fetchone()
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")
        cur = conn.execute(
            "INSERT INTO users(name,email,password_hash) VALUES(?,?,?)",
            (payload.name, payload.email, hash_password(payload.password))
        )
        conn.commit()
        user_id = cur.lastrowid
        return {"access_token": create_access_token(user_id), "token_type": "bearer"}
    finally:
        conn.close()

@router.post("/login")
def login(payload: LoginRequest):
    conn = get_db()
    try:
        user = conn.execute("SELECT * FROM users WHERE email=?", (payload.email,)).fetchone()
        if not user or not verify_password(payload.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return {"access_token": create_access_token(user["id"]), "token_type": "bearer"}
    finally:
        conn.close()
