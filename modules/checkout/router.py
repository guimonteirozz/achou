from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from modules.catalog import schemas, services

router = APIRouter(prefix="/catalog", tags=["Catálogo e Busca"])

@router.get("/produtos", response_model=List[schemas.ProdutoResponse])
def listar_produtos(
    search: Optional[str] = Query(None, description="Termo para buscar por nome ou descrição"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por ID da categoria"),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Lista e busca produtos no catálogo com suporte a filtros e paginação."""
    return services.get_produtos(db, search=search, categoria_id=categoria_id, skip=skip, limit=limit)

@router.get("/produtos/{produto_id}", response_model=schemas.ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    """Retorna os detalhes de um produto específico."""
    produto = services.get_produto_by_id(db, produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    return produto

@router.post("/produtos", response_model=schemas.ProdutoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    """Cadastra um novo produto no catálogo (Painel do Vendedor)."""
    return services.create_produto(db, produto)

@router.get("/categorias", response_model=List[schemas.CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    """Lista todas as categorias de produtos disponíveis."""
    return services.get_categorias(db)

@router.post("/categorias", response_model=schemas.CategoriaResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    """Cadastra uma nova categoria."""
    return services.create_categoria(db, categoria)

@router.post("/vendedores", response_model=schemas.VendedorResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_vendedor(vendedor: schemas.VendedorCreate, db: Session = Depends(get_db)):
    """Cadastra um novo vendedor."""
    return services.create_vendedor(db, vendedor)

router = APIRouter(prefix="/checkout", tags=["Checkout e Pagamento"])

@router.post("/", response_model=schemas.PedidoResponse, status_code=status.HTTP_201_CREATED)
def realizar_checkout(payload: schemas.CheckoutRequest, db: Session = Depends(get_db)):
    """Realiza o fechamento do carrinho, valida concorrência de estoque e simula o pagamento."""
    return services.processar_checkout(db, payload.usuario_id)