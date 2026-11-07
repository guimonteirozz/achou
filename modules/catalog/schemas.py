from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class CategoriaBase(BaseModel):
    nome: str
    slug: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int
    model_config = {"from_attributes": True}

class VendedorBase(BaseModel):
    nome: str
    email: EmailStr

class VendedorCreate(VendedorBase):
    pass

class VendedorResponse(VendedorBase):
    id: int
    status: str
    model_config = {"from_attributes": True}

class ProdutoCreate(BaseModel):
    vendedor_id: int
    categoria_id: int
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque_atual: int

class ProdutoResponse(ProdutoCreate):
    id: int
    criado_em: datetime
    model_config = {"from_attributes": True}