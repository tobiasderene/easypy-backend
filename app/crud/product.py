from sqlalchemy.orm import Session
from app.db.models import Product
from app.schemas.product import ProductCreate, ProductUpdate


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.product_id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def get_products_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Product).filter(Product.user_id == user_id).offset(skip).limit(limit).all()


def get_products_by_category(db: Session, category: str, skip: int = 0, limit: int = 100):
    return db.query(Product).filter(Product.product_category == category).offset(skip).limit(limit).all()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if not db_product:
        return None
    for field, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if not db_product:
        return None
    db.delete(db_product)
    db.commit()
    return db_product