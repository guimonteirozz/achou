from sqlalchemy.orm import Session
from modules.cart.models import CarrinhoModel, ItemCarrinhoModel
from modules.catalog.models import ProdutoModel
from fastapi import HTTPException, status

def get_or_create_carrinho(db: Session, usuario_id: int) -> CarrinhoModel:
    carrinho = db.query(CarrinhoModel).filter(CarrinhoModel.usuario_id == usuario_id).first()
    if not carrinho:
        carrinho = CarrinhoModel(usuario_id=usuario_id)
        db.add(carrinho)
        db.commit()
        db.refresh(carrinho)
    return carrinho

def adicionar_item(db: Session, usuario_id: int, produto_id: int, quantidade: int):
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    if produto.estoque_atual < quantidade:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Estoque insuficiente")

    carrinho = get_or_create_carrinho(db, usuario_id)
    
    item = db.query(ItemCarrinhoModel).filter(
        ItemCarrinhoModel.carrinho_id == carrinho.id,
        ItemCarrinhoModel.produto_id == produto_id
    ).first()

    if item:
        item.quantidade += quantidade
    else:
        item = ItemCarrinhoModel(carrinho_id=carrinho.id, produto_id=produto_id, quantidade=quantidade)
        db.add(item)
    
    db.commit()
    db.refresh(carrinho)
    return carrinho