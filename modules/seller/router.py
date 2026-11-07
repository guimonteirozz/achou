from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.database import get_db
from modules.seller import schemas, services
from modules.catalog.schemas import ProdutoResponse

router = APIRouter(prefix="/seller", tags=["Painel do Vendedor"])

@router.get("/{vendedor_id}/painel", response_model=schemas.PainelVendedorResponse)
def visualizar_painel(vendedor_id: int, db: Session = Depends(get_db)):
    """Exibe o resumo de vendas, faturamento e estatísticas do vendedor."""
    return services.obter_painel_vendedor(db, vendedor_id)

@router.patch("/{vendedor_id}/produtos/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(vendedor_id: int, produto_id: int, dados: schemas.ProdutoVendedorUpdate, db: Session = Depends(get_db)):
    """Permite ao vendedor atualizar preço, estoque ou descrição de seus produtos."""
    return services.atualizar_produto_vendedor(db, vendedor_id, produto_id, dados)