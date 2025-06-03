"""
Schemas Pydantic para validação de dados
"""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

# Schemas para Atividade
class AtividadeBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100, description="Nome da atividade")
    categoria: str = Field(..., min_length=1, max_length=50, description="Categoria da atividade")
    descricao: Optional[str] = Field(None, max_length=500, description="Descrição da atividade")

class AtividadeCreate(AtividadeBase):
    pass

class AtividadeResponse(AtividadeBase):
    id: int
    criado_em: datetime
    
    class Config:
        from_attributes = True

# Schemas para Sessao
class SessaoBase(BaseModel):
    atividade_id: int = Field(..., description="ID da atividade")
    duracao: int = Field(..., ge=1, le=1440, description="Duração em minutos (1-1440)")
    intensidade: Optional[str] = Field(None, description="Intensidade: baixa, moderada ou alta")
    calorias: Optional[float] = Field(None, ge=0, description="Calorias queimadas")
    observacoes: Optional[str] = Field(None, max_length=500, description="Observações sobre a sessão")
    
    @validator('intensidade')
    def validar_intensidade(cls, v):
        if v is not None and v not in ['baixa', 'moderada', 'alta']:
            raise ValueError('Intensidade deve ser: baixa, moderada ou alta')
        return v

class SessaoCreate(SessaoBase):
    pass

class SessaoResponse(SessaoBase):
    id: int
    data: datetime
    criado_em: datetime
    atividade: AtividadeResponse
    
    class Config:
        from_attributes = True

# Schema para Estatísticas
class EstatisticasResponse(BaseModel):
    total_atividades: int
    total_sessoes: int
    tempo_total_exercicio: int  # em minutos
    calorias_totais: float
    atividade_mais_praticada: Optional[str]
    tempo_medio_sessao: float  # em minutos