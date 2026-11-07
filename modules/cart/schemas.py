from pydantic import BaseModel

class ItemCarrinhoCreate(BaseModel):
    produto_id: int
    quantidade: int

class ItemCarrinhoResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    model_config = {"from_attributes": True}

class CarrinhoResponse(BaseModel):
    id: int
    usuario_id: int
    itens: list[ItemCarrinhoResponse] = []
    model_config = {"from_attributes": True}