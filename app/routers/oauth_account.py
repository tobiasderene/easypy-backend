from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from datetime import datetime
import httpx
import os

from app.db.database import get_db
from app.crud import oauth_account as crud_oauth
from app.crud import user as crud_user
from app.schemas.user import UserCreate
from app.schemas.oauth_account import OAuthAccountCreate
from itsdangerous import URLSafeSerializer, BadSignature

router = APIRouter(prefix="/auth", tags=["Auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SECRET_KEY = os.getenv("SECRET_KEY")

serializer = URLSafeSerializer(SECRET_KEY)

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def create_session_cookie(response: Response, user_id: int):
    token = serializer.dumps({"user_id": user_id})
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,       # no accesible desde JS
        secure=True,         # solo HTTPS en producción
        samesite="lax"
    )


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


@router.get("/google")
def login_google():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return {"url": f"{GOOGLE_AUTH_URL}?{query}"}


@router.get("/callback")
async def google_callback(code: str, response: Response, db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:

        # intercambiar code por access token
        token_response = await client.post(GOOGLE_TOKEN_URL, data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        })
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="Error al obtener token de Google")

        # obtener info del usuario de Google
        userinfo_response = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        userinfo = userinfo_response.json()

    google_id = userinfo.get("sub")
    email = userinfo.get("email")
    name = userinfo.get("name")

    if not google_id or not email:
        raise HTTPException(status_code=400, detail="No se pudo obtener información de Google")

    # buscar si ya existe una cuenta con este google_id
    oauth_account = crud_oauth.get_oauth_account_by_google_id(db, google_id)

    if oauth_account:
        # usuario ya existe, simplemente logueamos
        create_session_cookie(response, oauth_account.user_id)
        return {"detail": "Login exitoso"}

    # buscar si el email ya está registrado con otro método
    existing_by_email = crud_oauth.get_oauth_account_by_email(db, email)
    if existing_by_email:
        # vincular google_id a la cuenta existente
        crud_oauth.update_oauth_account(db, existing_by_email.oauth_account_id, {"google_id": google_id})
        create_session_cookie(response, existing_by_email.user_id)
        return {"detail": "Cuenta vinculada y login exitoso"}

    # usuario nuevo: crear user y oauth_account
    new_user = crud_user.create_user(db, UserCreate(
        user_nickname=name,
        user_role="user",
        user_status="active",
        user_description="",
        created_at=datetime.utcnow()
    ))

    crud_oauth.create_oauth_account(db, OAuthAccountCreate(
        user_id=new_user.user_id,
        google_id=google_id,
        email=email,
        name=name,
        created_at=datetime.utcnow()
    ))

    create_session_cookie(response, new_user.user_id)
    return {"detail": "Registro exitoso"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("session")
    return {"detail": "Sesión cerrada"}


@router.get("/me")
def get_me(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    return user