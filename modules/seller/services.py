from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from modules.catalog.models import VendedorModel, ProdutoModel
from modules.checkout.models import ItemPedidoModel, PedidoModel
from modules.seller.schemas import ProdutoVendedorUpdate

def atualizar_produto_vendedor(db: Session, vendedor_id: int, produto_id: int, dados: ProdutoVendedorUpdate):
    produto = db.query(ProdutoModel).filter(
        ProdutoModel.id == produto_id,
        ProdutoModel.vendedor_id == vendedor_id
    ).first()

    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado ou não pertence a este vendedor")

    update_data = dados.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(produto, key, value)

    db.commit()
    db.refresh(produto)
    return produto

def obter_painel_vendedor(db: Session, vendedor_id: int):
    vendedor = db.query(VendedorModel).filter(VendedorModel.id == vendedor_id).first()
    if not vendedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendedor não encontrado")

    total_produtos = db.query(ProdutoModel).filter(ProdutoModel.vendedor_id == vendedor_id).count()

    # Consulta itens vendidos dos produtos deste vendedor cujos pedidos foram pagos
    resultados = (
        db.query(
            ProdutoModel.id,
            ProdutoModel.nome,
            func.sum(ItemPedidoModel.quantidade).label("qtd_vendida"),
            func.sum(ItemPedidoModel.quantidade * ItemPedidoModel.preco_unitario).label("faturamento")
        )
        .join(ItemPedidoModel, ItemPedidoModel.produto_id == ProdutoModel.id)
        .join(PedidoModel, PedidoModel.id == ItemPedidoModel.pedido_id)
        .filter(ProdutoModel.vendedor_id == vendedor_id, PedidoModel.status == "pago")
        .group_by(ProdutoModel.id, ProdutoModel.nome)
        .all()
    )

    faturamento_geral = sum([res.faturamento for res in resultados]) if resultados else 0.0

    itens_vendidos = [
        {
            "produto_id": res.id,
            "nome_produto": res.nome,
            "quantidade_total_vendida": res.qtd_vendida,
            "faturamento_total": res.faturamento
        }
        for res in resultados
    ]

    return {
        "vendedor_id": vendedor.id,
        "nome_vendedor": vendedor.nome,
        "total_produtos_cadastrados": total_produtos,
        "faturamento_geral": faturamento_geral,
        "itens_vendidos": itens_vendidos
    }