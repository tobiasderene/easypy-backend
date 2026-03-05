from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.database import get_db
from app.schemas.image import ImageOut, ImageCreate
from app.crud import image as crud_image
from app.services.storage import (
    upload_product_image,
    upload_profile_image,
    delete_product_image,
    delete_profile_image
)
from app.routers.auth import get_current_user

router = APIRouter(prefix="/images", tags=["Images"])

ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/png", "image/webp"]


def validate_image(file: UploadFile):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Formato no permitido. Usá JPG, PNG o WEBP")


@router.post("/product/{product_id}", response_model=ImageOut, status_code=201)
async def upload_product_image_endpoint(
    product_id: int,
    file: UploadFile = File(...),
    is_primary: bool = False,
    position: int = 0,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    validate_image(file)
    url = upload_product_image(file, product_id)
    return crud_image.create_image(db, image=ImageCreate(
        image_url=url,
        is_primary=is_primary,
        position=position,
        product_id=product_id,
        created_at=datetime.utcnow()
    ))


@router.post("/profile", response_model=ImageOut, status_code=201)
async def upload_profile_image_endpoint(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    validate_image(file)

    # si ya tiene foto de perfil la reemplazamos
    existing = crud_image.get_image_by_user(db, user.user_id)
    if existing:
        delete_profile_image(existing.image_url)
        crud_image.delete_image(db, existing.image_id)

    url = upload_profile_image(file, user.user_id)
    return crud_image.create_image(db, image=ImageCreate(
        image_url=url,
        is_primary=True,
        user_id=user.user_id,
        created_at=datetime.utcnow()
    ))


@router.get("/product/{product_id}", response_model=List[ImageOut])
def get_product_images(product_id: int, db: Session = Depends(get_db)):
    return crud_image.get_images_by_product(db, product_id)


@router.get("/profile/{user_id}", response_model=ImageOut)
def get_profile_image(user_id: int, db: Session = Depends(get_db)):
    image = crud_image.get_image_by_user(db, user_id)
    if not image:
        raise HTTPException(status_code=404, detail="Imagen de perfil no encontrada")
    return image


@router.patch("/product/{product_id}/primary/{image_id}", response_model=ImageOut)
def set_primary(
    product_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    image = crud_image.set_primary_image(db, product_id, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return image


@router.delete("/{image_id}", response_model=ImageOut)
def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    db_image = crud_image.get_image(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    if db_image.product_id:
        delete_product_image(db_image.image_url)
    elif db_image.user_id:
        delete_profile_image(db_image.image_url)

    return crud_image.delete_image(db, image_id)