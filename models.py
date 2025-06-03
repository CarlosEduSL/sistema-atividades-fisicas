"""
Modelos SQLAlchemy para o banco de dados
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Atividade(Base):
    __tablename__ = "atividades"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    descricao = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=datetime.now)
    
    # Relacionamento com Sessao
    sessoes = relationship("Sessao", back_populates="atividade", cascade="all, delete-orphan")

class Sessao(Base):
    __tablename__ = "sessoes"
    
    id = Column(Integer, primary_key=True, index=True)
    atividade_id = Column(Integer, ForeignKey("atividades.id"), nullable=False)
    data = Column(DateTime, default=datetime.now)
    duracao = Column(Integer, nullable=False)  # em minutos
    intensidade = Column(String(20), nullable=True)  # baixa, moderada, alta
    calorias = Column(Float, nullable=True)
    observacoes = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=datetime.now)
    
    # Relacionamento com Atividade
    atividade = relationship("Atividade", back_populates="sessoes")