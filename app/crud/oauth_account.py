from sqlalchemy.orm import Session
from app.db.models import OAuthAccount
from app.schemas.oauth_account import OAuthAccountCreate, OAuthAccountUpdate


def get_oauth_account(db: Session, oauth_account_id: int):
    return db.query(OAuthAccount).filter(OAuthAccount.oauth_account_id == oauth_account_id).first()


def get_oauth_account_by_user(db: Session, user_id: int):
    return db.query(OAuthAccount).filter(OAuthAccount.user_id == user_id).all()


def get_oauth_account_by_provider(db: Session, provider: str, provider_user_id: str):
    return db.query(OAuthAccount).filter(
        OAuthAccount.provider == provider,
        OAuthAccount.provider_user_id == provider_user_id
    ).first()


def get_oauth_account_by_email_and_provider(db: Session, email: str, provider: str):
    return db.query(OAuthAccount).filter(
        OAuthAccount.email == email,
        OAuthAccount.provider == provider
    ).first()


def get_oauth_accounts_by_email(db: Session, email: str):
    return db.query(OAuthAccount).filter(OAuthAccount.email == email).all()


def create_oauth_account(db: Session, oauth_account: OAuthAccountCreate):
    db_oauth = OAuthAccount(**oauth_account.model_dump())
    db.add(db_oauth)
    db.commit()
    db.refresh(db_oauth)
    return db_oauth


def update_oauth_account(db: Session, oauth_account_id: int, oauth_account: OAuthAccountUpdate):
    db_oauth = db.query(OAuthAccount).filter(OAuthAccount.oauth_account_id == oauth_account_id).first()
    if not db_oauth:
        return None
    for field, value in oauth_account.model_dump(exclude_unset=True).items():
        setattr(db_oauth, field, value)
    db.commit()
    db.refresh(db_oauth)
    return db_oauth


def delete_oauth_account(db: Session, oauth_account_id: int):
    db_oauth = db.query(OAuthAccount).filter(OAuthAccount.oauth_account_id == oauth_account_id).first()
    if not db_oauth:
        return None
    db.delete(db_oauth)
    db.commit()
    return db_oauth