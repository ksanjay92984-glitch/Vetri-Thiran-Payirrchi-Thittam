from fastapi import Depends, Header, HTTPException
from app.security import decode_token
from app.db import get_db

def get_current_user(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    user_id = decode_token(authorization.split(" ", 1)[1])
    conn = get_db()
    user = conn.execute("SELECT id, name, email FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return dict(user)
