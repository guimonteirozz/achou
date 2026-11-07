import uuid
from sqlalchemy.orm import Session
from modules.cart.models import CarrinhoModel
from modules.checkout.models import PedidoModel, ItemPedidoModel, PagamentoMockModel
from modules.catalog.models import ProdutoModel
from fastapi import HTTPException, status

def processar_checkout(db: Session, usuario_id: int) -> PedidoModel:
    carrinho = db.query(CarrinhoModel).filter(CarrinhoModel.usuario_id == usuario_id).first()
    if not carrinho or not carrinho.itens:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O carrinho está vazio")

    # Inicia transação segura para cálculo de valor e baixa de estoque
    try:
        valor_total = 0.0
        itens_pedido_data = []

        for item in carrinho.itens:
            # Bloqueia a linha do produto para escrita concorrente (Prevenção de Race Condition na Black Friday)
            produto = db.query(ProdutoModel).filter(ProdutoModel.id == item.produto_id).with_for_update().first()
            
            if not produto or produto.estoque_atual < item.quantidade:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail=f"Estoque esgotado ou insuficiente para o produto: {produto.nome if produto else item.produto_id}"
                )
            
            # Baixa o estoque
            produto.estoque_atual -= item.quantidade
            subtotal = produto.preco * item.quantidade
            valor_total += subtotal

            itens_pedido_data.append({
                "produto_id": produto.id,
                "quantidade": item.quantidade,
                "preco_unitario": produto.preco
            })

        # Cria o pedido
        novo_pedido = PedidoModel(
            usuario_id=usuario_id,
            status="pago", # Simulação direta aprovada
            valor_total=valor_total
        )
        db.add(novo_pedido)
        db.flush() # Gera o ID do pedido

        for ip in itens_pedido_data:
            item_ped = ItemPedidoModel(pedido_id=novo_pedido.id, **ip)
            db.add(item_ped)

        # Simulação do Gateway de Pagamento
        transacao_mock = PagamentoMockModel(
            pedido_id=novo_pedido.id,
            status="sucesso",
            gateway_transacao_id=f"tx_mock_{uuid.uuid4().hex[:12]}"
        )
        db.add(transacao_mock)

        # Esvazia o carrinho após o checkout bem-sucedido
        db.query(ItemCarrinhoModel).filter(ItemCarrinhoModel.carrinho_id == carrinho.id).delete()

        db.commit()
        db.refresh(novo_pedido)
        return novo_pedido

    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro no checkout: {str(e)}")