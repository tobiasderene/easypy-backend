from fastapi import FastAPI
from app.routers import user, product, wallet, order, transaction, withdrawal, bank_movement, oauth_account, image

app = FastAPI(title="Marketplace API")

app.include_router(oauth_account.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(wallet.router)
app.include_router(order.router)
app.include_router(transaction.router)
app.include_router(withdrawal.router)
app.include_router(bank_movement.router)
app.include_router(image.router)