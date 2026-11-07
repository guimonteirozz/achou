from fastapi import FastAPI
from core.config import settings
from core.database import engine, Base
from modules.catalog.router import router as catalog_router
from modules.cart.router import router as cart_router
from modules.checkout.router import router as checkout_router
from modules.seller.router import router as seller_router

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend modular para o marketplace Achou! com suporte a picos de tráfego."
)

# Registra os módulos
app.include_router(catalog_router)
app.include_router(cart_router)
app.include_router(checkout_router)
app.include_router(seller_router)

@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "message": "Todos os módulos, incluindo o Painel do Vendedor, foram integrados com sucesso!"
    }