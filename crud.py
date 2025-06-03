"""
Operações CRUD para o banco de dados
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models import Atividade, Sessao
from schemas import AtividadeCreate, SessaoCreate, EstatisticasResponse
from datetime import datetime
from typing import Optional, List

# =================== OPERAÇÕES ATIVIDADE ===================

def create_atividade(db: Session, atividade: AtividadeCreate):
    """Criar nova atividade"""
    db_atividade = Atividade(**atividade.model_dump())
    db.add(db_atividade)
    db.commit()
    db.refresh(db_atividade)
    return db_atividade

def get_atividades(db: Session, skip: int = 0, limit: int = 100):
    """Obter lista de atividades"""
    return db.query(Atividade).offset(skip).limit(limit).all()

def get_atividade(db: Session, atividade_id: int):
    """Obter atividade por ID"""
    return db.query(Atividade).filter(Atividade.id == atividade_id).first()

def delete_atividade(db: Session, atividade_id: int):
    """Excluir atividade"""
    atividade = db.query(Atividade).filter(Atividade.id == atividade_id).first()
    if atividade:
        db.delete(atividade)
        db.commit()
        return True
    return False

# =================== OPERAÇÕES SESSÃO ===================

def create_sessao(db: Session, sessao: SessaoCreate):
    """Criar nova sessão"""
    db_sessao = Sessao(**sessao.model_dump())
    db.add(db_sessao)
    db.commit()
    db.refresh(db_sessao)
    return db_sessao

def get_sessoes(db: Session, tipo: Optional[str] = None, data_inicio: Optional[str] = None, 
               data_fim: Optional[str] = None, skip: int = 0, limit: int = 100):
    """Obter lista de sessões com filtros"""
    query = db.query(Sessao).join(Atividade)
    
    # Filtro por tipo de atividade
    if tipo:
        query = query.filter(Atividade.categoria.ilike(f"%{tipo}%"))
    
    # Filtro por data de início
    if data_inicio:
        try:
            data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
            query = query.filter(Sessao.data >= data_inicio_dt)
        except ValueError:
            pass
    
    # Filtro por data de fim
    if data_fim:
        try:
            data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
            query = query.filter(Sessao.data <= data_fim_dt)
        except ValueError:
            pass
    
    return query.order_by(desc(Sessao.data)).offset(skip).limit(limit).all()

def get_sessao(db: Session, sessao_id: int):
    """Obter sessão por ID"""
    return db.query(Sessao).filter(Sessao.id == sessao_id).first()

def delete_sessao(db: Session, sessao_id: int):
    """Excluir sessão"""
    sessao = db.query(Sessao).filter(Sessao.id == sessao_id).first()
    if sessao:
        db.delete(sessao)
        db.commit()
        return True
    return False

# =================== ESTATÍSTICAS ===================

def get_estatisticas(db: Session) -> EstatisticasResponse:
    """Calcular estatísticas gerais do sistema"""
    
    # Total de atividades
    total_atividades = db.query(Atividade).count()
    
    # Total de sessões
    total_sessoes = db.query(Sessao).count()
    
    # Tempo total de exercício (em minutos)
    tempo_total = db.query(func.sum(Sessao.duracao)).scalar() or 0
    
    # Calorias totais queimadas
    calorias_totais = db.query(func.sum(Sessao.calorias)).scalar() or 0.0
    
    # Atividade mais praticada
    atividade_mais_praticada_query = (
        db.query(Atividade.nome, func.count(Sessao.id).label('count'))
        .join(Sessao)
        .group_by(Atividade.nome)
        .order_by(desc('count'))
        .first()
    )
    
    atividade_mais_praticada = atividade_mais_praticada_query[0] if atividade_mais_praticada_query else None
    
    # Tempo médio por sessão
    tempo_medio_sessao = db.query(func.avg(Sessao.duracao)).scalar() or 0.0
    
    return EstatisticasResponse(
        total_atividades=total_atividades,
        total_sessoes=total_sessoes,
        tempo_total_exercicio=int(tempo_total),
        calorias_totais=float(calorias_totais),
        atividade_mais_praticada=atividade_mais_praticada,
        tempo_medio_sessao=float(tempo_medio_sessao)
    )