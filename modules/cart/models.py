from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class CarrinhoModel(Base):
    __tablename__ = "carrinhos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, unique=True, nullable=False) # Identificador simples do usuário/sessão

    itens = relationship("ItemCarrinhoModel", back_populates="carrinho", cascade="all, delete-orphan")

class ItemCarrinhoModel(Base):
    __tablename__ = "itens_carrinho"

    id = Column(Integer, primary_key=True, index=True)
    carrinho_id = Column(Integer, ForeignKey("carrinhos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)

    carrinho = relationship("CarrinhoModel", back_populates="itens")
    produto = relationship("ProdutoModel")