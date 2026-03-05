from sqlalchemy.orm import Session
from app.db.models import Image
from app.schemas.image import ImageCreate, ImageUpdate


def get_image(db: Session, image_id: int):
    return db.query(Image).filter(Image.image_id == image_id).first()


def get_images_by_product(db: Session, product_id: int):
    return db.query(Image).filter(Image.product_id == product_id).order_by(Image.position).all()


def get_primary_image_by_product(db: Session, product_id: int):
    return db.query(Image).filter(
        Image.product_id == product_id,
        Image.is_primary == True
    ).first()


def get_image_by_user(db: Session, user_id: int):
    return db.query(Image).filter(Image.user_id == user_id).first()


def create_image(db: Session, image: ImageCreate):
    db_image = Image(**image.model_dump())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def update_image(db: Session, image_id: int, image: ImageUpdate):
    db_image = db.query(Image).filter(Image.image_id == image_id).first()
    if not db_image:
        return None
    for field, value in image.model_dump(exclude_unset=True).items():
        setattr(db_image, field, value)
    db.commit()
    db.refresh(db_image)
    return db_image


def delete_image(db: Session, image_id: int):
    db_image = db.query(Image).filter(Image.image_id == image_id).first()
    if not db_image:
        return None
    db.delete(db_image)
    db.commit()
    return db_image


def set_primary_image(db: Session, product_id: int, image_id: int):
    # quitar primary de todas las imágenes del producto
    db.query(Image).filter(Image.product_id == product_id).update({"is_primary": False})
    # setear la nueva
    db_image = db.query(Image).filter(Image.image_id == image_id).first()
    if not db_image:
        return None
    db_image.is_primary = True
    db.commit()
    db.refresh(db_image)
    return db_image