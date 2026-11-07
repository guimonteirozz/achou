from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from core.database import Base

class VendedorModel(Base):
    __tablename__ = "vendedores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    status = Column(String(20), default="ativo")

    produtos = relationship("ProdutoModel", back_populates="vendedor")

class CategoriaModel(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, index=True, nullable=False)

    produtos = relationship("ProdutoModel", back_populates="categoria")

class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    vendedor_id = Column(Integer, ForeignKey("vendedores.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    nome = Column(String(150), index=True, nullable=False)
    descricao = Column(Text, nullable=True)
    preco = Column(Float, nullable=False)
    estoque_atual = Column(Integer, default=0, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    vendedor = relationship("VendedorModel", back_populates="produtos")
    categoria = relationship("CategoriaModel", back_populates="produtos")