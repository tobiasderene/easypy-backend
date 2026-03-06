from fastapi import FastAPI
from app.routers import user, product, wallet, order, transaction, withdrawal, bank_movement, oauth_account, image
import os


app = FastAPI(
    title="Easypy",
    docs_url="/docs" if os.getenv("ENV") == "development" else None,
    redoc_url="/redoc" if os.getenv("ENV") == "development" else None
)

origins = [
    "https://easypy-6d0d3.web.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(oauth_account.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(wallet.router)
app.include_router(order.router)
app.include_router(transaction.router)
app.include_router(withdrawal.router)
app.include_router(bank_movement.router)
app.include_router(image.router)