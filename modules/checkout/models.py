from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class PedidoModel(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)
    status = Column(String(30), default="pendente", nullable=False) # pendente, pago, cancelado
    valor_total = Column(Float, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    itens = relationship("ItemPedidoModel", back_populates="pedido", cascade="all, delete-orphan")
    pagamento = relationship("PagamentoMockModel", back_populates="pedido", uselist=False)

class ItemPedidoModel(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)

    pedido = relationship("PedidoModel", back_populates="itens")

class PagamentoMockModel(Base):
    __tablename__ = "pagamentos_mock"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    status = Column(String(30), default="sucesso", nullable=False) # sucesso, falha
    gateway_transacao_id = Column(String(100), nullable=False)
    processado_em = Column(DateTime, default=datetime.utcnow)

    pedido = relationship("PedidoModel", back_populates="pagamento")