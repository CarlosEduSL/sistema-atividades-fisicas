"""
Sistema de Monitoramento de Atividades Físicas - API FastAPI
Desenvolvido para o projeto V2 - Desenvolvimento de Aplicações Distribuídas
"""

from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional, List
import uvicorn
from datetime import datetime

from database import get_db, engine
from models import Base, Atividade, Sessao
from schemas import AtividadeCreate, AtividadeResponse, SessaoCreate, SessaoResponse, EstatisticasResponse
from crud import (
    create_atividade,
    get_atividades,
    get_atividade,
    delete_atividade,
    create_sessao,
    get_sessoes,
    get_sessao,
    delete_sessao,
    get_estatisticas
)

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Instanciar o FastAPI
app = FastAPI(
    title="Sistema de Monitoramento de Atividades Físicas",
    description="API para registro e monitoramento de atividades físicas com FastAPI, SQLAlchemy e SQLite",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configurar arquivos estáticos e templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# =================== ROTAS DO FRONTEND ===================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """Página inicial com dashboard"""
    estatisticas = get_estatisticas(db)
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "estatisticas": estatisticas}
    )

@app.get("/atividades", response_class=HTMLResponse)
async def pagina_atividades(request: Request, db: Session = Depends(get_db)):
    """Página de gerenciamento de atividades"""
    atividades = get_atividades(db)
    return templates.TemplateResponse(
        "atividades.html", 
        {"request": request, "atividades": atividades}
    )

@app.get("/sessoes", response_class=HTMLResponse)
async def pagina_sessoes(request: Request, db: Session = Depends(get_db)):
    """Página de gerenciamento de sessões"""
    sessoes = get_sessoes(db)
    atividades = get_atividades(db)
    return templates.TemplateResponse(
        "sessoes.html", 
        {"request": request, "sessoes": sessoes, "atividades": atividades}
    )

# =================== API ENDPOINTS ===================

# Health Check
@app.get("/api/health")
async def health_check():
    """Endpoint de verificação de saúde da API"""
    return {"status": "ok", "timestamp": datetime.now()}

# Endpoints de Atividades
@app.post("/api/atividades", response_model=AtividadeResponse)
async def criar_atividade(atividade: AtividadeCreate, db: Session = Depends(get_db)):
    """Cadastrar nova atividade"""
    return create_atividade(db=db, atividade=atividade)

@app.get("/api/atividades", response_model=List[AtividadeResponse])
async def listar_atividades(db: Session = Depends(get_db)):
    """Listar todas as atividades"""
    return get_atividades(db)

@app.get("/api/atividades/{atividade_id}", response_model=AtividadeResponse)
async def obter_atividade(atividade_id: int, db: Session = Depends(get_db)):
    """Obter atividade específica"""
    atividade = get_atividade(db, atividade_id=atividade_id)
    if atividade is None:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    return atividade

@app.delete("/api/atividades/{atividade_id}")
async def excluir_atividade(atividade_id: int, db: Session = Depends(get_db)):
    """Excluir atividade"""
    success = delete_atividade(db, atividade_id=atividade_id)
    if not success:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    return {"message": "Atividade excluída com sucesso"}

# Endpoints de Sessões
@app.post("/api/sessoes", response_model=SessaoResponse)
async def criar_sessao(sessao: SessaoCreate, db: Session = Depends(get_db)):
    """Registrar nova sessão de atividade"""
    # Verificar se a atividade existe
    atividade = get_atividade(db, atividade_id=sessao.atividade_id)
    if atividade is None:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    return create_sessao(db=db, sessao=sessao)

@app.get("/api/sessoes", response_model=List[SessaoResponse])
async def listar_sessoes(
    tipo: Optional[str] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Listar sessões com filtros opcionais"""
    return get_sessoes(db, tipo=tipo, data_inicio=data_inicio, data_fim=data_fim)

@app.get("/api/sessoes/{sessao_id}", response_model=SessaoResponse)
async def obter_sessao(sessao_id: int, db: Session = Depends(get_db)):
    """Obter sessão específica"""
    sessao = get_sessao(db, sessao_id=sessao_id)
    if sessao is None:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    return sessao

@app.delete("/api/sessoes/{sessao_id}")
async def excluir_sessao(sessao_id: int, db: Session = Depends(get_db)):
    """Excluir sessão"""
    success = delete_sessao(db, sessao_id=sessao_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    return {"message": "Sessão excluída com sucesso"}

# Endpoint de Estatísticas
@app.get("/api/estatisticas", response_model=EstatisticasResponse)
async def obter_estatisticas(db: Session = Depends(get_db)):
    """Obter estatísticas gerais do sistema"""
    return get_estatisticas(db)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)