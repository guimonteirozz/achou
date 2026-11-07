from datetime import datetime
from pydantic import BaseModel

class CheckoutRequest(BaseModel):
    usuario_id: int

class PagamentoResponse(BaseModel):
    id: int
    pedido_id: int
    status: str
    gateway_transacao_id: str
    processado_em: datetime
    model_config = {"from_attributes": True}

class PedidoResponse(BaseModel):
    id: int
    usuario_id: int
    status: str
    valor_total: float
    criado_em: datetime
    pagamento: PagamentoResponse | None = None
    model_config = {"from_attributes": True}