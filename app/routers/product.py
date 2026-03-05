from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.crud import product as crud_product

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductOut])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_product.get_products(db, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_product


@router.get("/user/{user_id}", response_model=List[ProductOut])
def get_products_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_product.get_products_by_user(db, user_id, skip=skip, limit=limit)


@router.get("/category/{category}", response_model=List[ProductOut])
def get_products_by_category(category: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_product.get_products_by_category(db, category, skip=skip, limit=limit)


@router.post("/", response_model=ProductOut, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db, product)


@router.patch("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud_product.update_product(db, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_product


@router.delete("/{product_id}", response_model=ProductOut)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud_product.delete_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_product