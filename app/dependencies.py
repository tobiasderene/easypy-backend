from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from itsdangerous import URLSafeSerializer, BadSignature
import os

from app.db.database import get_db
from app.crud import user as crud_user

SECRET_KEY = os.getenv("SECRET_KEY")
serializer = URLSafeSerializer(SECRET_KEY)


def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("session")
    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")
    try:
        data = serializer.loads(token)
    except BadSignature:
        raise HTTPException(status_code=401, detail="Sesión inválida")
    user = crud_user.get_user(db, data["user_id"])
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user


def get_admin_user(user=Depends(get_current_user)):
    if user.user_role != "admin":
        raise HTTPException(status_code=403, detail="No tenés permisos para esto")
    return user