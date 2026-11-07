from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.database import get_db
from modules.cart import schemas, services

router = APIRouter(prefix="/cart", tags=["Carrinho de Compras"])

@router.get("/{usuario_id}", response_model=schemas.CarrinhoResponse)
def ver_carrinho(usuario_id: int, db: Session = Depends(get_db)):
    """Retorna os itens presentes no carrinho do usuário."""
    return services.get_or_create_carrinho(db, usuario_id)

@router.post("/{usuario_id}/itens", response_model=schemas.CarrinhoResponse, status_code=status.HTTP_201_CREATED)
def adicionar_ao_carrinho(usuario_id: int, item: schemas.ItemCarrinhoCreate, db: Session = Depends(get_db)):
    """Adiciona um produto ao carrinho validando o estoque disponível."""
    return services.adicionar_item(db, usuario_id, item.produto_id, item.quantidade)