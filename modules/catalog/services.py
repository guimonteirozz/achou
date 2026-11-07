from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from modules.catalog.models import ProdutoModel, CategoriaModel, VendedorModel
from modules.catalog.schemas import ProdutoCreate, CategoriaCreate, VendedorCreate

def get_produtos(db: Session, search: Optional[str] = None, categoria_id: Optional[int] = None, skip: int = 0, limit: int = 10) -> List[ProdutoModel]:
    query = db.query(ProdutoModel)
    if search:
        query = query.filter(or_(ProdutoModel.nome.ilike(f"%{search}%"), ProdutoModel.descricao.ilike(f"%{search}%")))
    if categoria_id:
        query = query.filter(ProdutoModel.categoria_id == categoria_id)
    return query.offset(skip).limit(limit).all()

def get_produto_by_id(db: Session, produto_id: int) -> Optional[ProdutoModel]:
    return db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()

def create_produto(db: Session, produto: ProdutoCreate) -> ProdutoModel:
    db_produto = ProdutoModel(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def get_categorias(db: Session) -> List[CategoriaModel]:
    return db.query(CategoriaModel).all()

def create_categoria(db: Session, categoria: CategoriaCreate) -> CategoriaModel:
    db_cat = CategoriaModel(**categoria.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def create_vendedor(db: Session, vendedor: VendedorCreate) -> VendedorModel:
    db_vend = VendedorModel(**vendedor.model_dump())
    db.add(db_vend)
    db.commit()
    db.refresh(db_vend)
    return db_vend