from pydantic import BaseModel
from typing import List

class ProdutoVendedorUpdate(BaseModel):
    preco: float | None = None
    estoque_atual: int | None = None
    descricao: str | None = None

class ItemVendidoResponse(BaseModel):
    produto_id: int
    nome_produto: str
    quantidade_total_vendida: int
    faturamento_total: float
    model_config = {"from_attributes": True}

class PainelVendedorResponse(BaseModel):
    vendedor_id: int
    nome_vendedor: str
    total_produtos_cadastrados: int
    faturamento_geral: float
    itens_vendidos: List[ItemVendidoResponse] = []
    model_config = {"from_attributes": True}