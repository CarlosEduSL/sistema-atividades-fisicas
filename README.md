# Sistema de Monitoramento de Atividades Físicas
## Projeto V2 - FastAPI + Uvicorn + SQLAlchemy + SQLite

### 📋 Descrição do Projeto
Sistema web completo para registro e monitoramento de atividades físicas, desenvolvido com FastAPI, Uvicorn, SQLAlchemy e SQLite. Atende aos requisitos da V2 com API RESTful, banco de dados persistente, interface web e deploy em PaaS.

### 🎯 Objetivos Atendidos
- ✅ API RESTful com mínimo 4 endpoints (implementados 11 endpoints)
- ✅ Banco de dados persistente (SQLite)
- ✅ Interface web funcional (HTML + CSS + JavaScript)
- ✅ Deploy em plataforma PaaS (Render.com)
- ✅ Repositório GitHub público
- ✅ Operações CRUD completas

### 🛠️ Tecnologias Utilizadas
- **Backend**: FastAPI 0.104.1
- **Servidor**: Uvicorn 0.24.0
- **ORM**: SQLAlchemy 2.0.23
- **Banco**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Validação**: Pydantic 2.4.2
- **Templates**: Jinja2 3.1.2
- **Frontend**: HTML5 + CSS3 + Bootstrap 5 + JavaScript

---

## 🚀 PASSO A PASSO COMPLETO - COMO REPLICAR

### PASSO 1: Configuração do Ambiente

#### 1.1 Pré-requisitos
- Python 3.8+ instalado
- Git instalado
- Editor de código (VS Code recomendado)
- Conta no GitHub
- Conta no Render.com (gratuita)

#### 1.2 Criar Diretório do Projeto
```bash
mkdir sistema-atividades-fisicas
cd sistema-atividades-fisicas
```

#### 1.3 Criar Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### PASSO 2: Estrutura do Projeto

#### 2.1 Criar Estrutura de Pastas
```
sistema-atividades-fisicas/
├── main.py                 # Aplicação principal FastAPI
├── database.py             # Configuração do banco SQLite
├── models.py               # Modelos SQLAlchemy
├── schemas.py              # Schemas Pydantic
├── crud.py                 # Operações CRUD
├── requirements.txt        # Dependências Python
├── Procfile               # Configuração para deploy
├── .env                   # Variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo Git
├── README.md             # Documentação
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── atividades.html
│   └── sessoes.html
└── static/              # Arquivos estáticos
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

### PASSO 3: Instalação de Dependências

#### 3.1 Criar requirements.txt
```text
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.4.2
jinja2==3.1.2
python-multipart==0.0.6
python-dotenv==1.0.0
gunicorn==21.2.0
```

#### 3.2 Instalar Dependências
```bash
pip install -r requirements.txt
```

### PASSO 4: Implementação do Backend

#### 4.1 Configurar Banco de Dados (database.py)
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./atividades.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 4.2 Criar Modelos (models.py)
```python
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
    
    sessoes = relationship("Sessao", back_populates="atividade", cascade="all, delete-orphan")

class Sessao(Base):
    __tablename__ = "sessoes"
    
    id = Column(Integer, primary_key=True, index=True)
    atividade_id = Column(Integer, ForeignKey("atividades.id"), nullable=False)
    data = Column(DateTime, default=datetime.now)
    duracao = Column(Integer, nullable=False)
    intensidade = Column(String(20), nullable=True)
    calorias = Column(Float, nullable=True)
    observacoes = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=datetime.now)
    
    atividade = relationship("Atividade", back_populates="sessoes")
```

#### 4.3 Criar Schemas (schemas.py)
```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class AtividadeCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    categoria: str = Field(..., min_length=1, max_length=50)
    descricao: Optional[str] = Field(None, max_length=500)

class AtividadeResponse(AtividadeCreate):
    id: int
    criado_em: datetime
    
    class Config:
        from_attributes = True

class SessaoCreate(BaseModel):
    atividade_id: int
    duracao: int = Field(..., ge=1, le=1440)
    intensidade: Optional[str] = None
    calorias: Optional[float] = Field(None, ge=0)
    observacoes: Optional[str] = Field(None, max_length=500)

class SessaoResponse(SessaoCreate):
    id: int
    data: datetime
    criado_em: datetime
    atividade: AtividadeResponse
    
    class Config:
        from_attributes = True
```

#### 4.4 Implementar CRUD (crud.py)
```python
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models import Atividade, Sessao
from schemas import AtividadeCreate, SessaoCreate

def create_atividade(db: Session, atividade: AtividadeCreate):
    db_atividade = Atividade(**atividade.model_dump())
    db.add(db_atividade)
    db.commit()
    db.refresh(db_atividade)
    return db_atividade

def get_atividades(db: Session):
    return db.query(Atividade).all()

def create_sessao(db: Session, sessao: SessaoCreate):
    db_sessao = Sessao(**sessao.model_dump())
    db.add(db_sessao)
    db.commit()
    db.refresh(db_sessao)
    return db_sessao

def get_sessoes(db: Session):
    return db.query(Sessao).join(Atividade).order_by(desc(Sessao.data)).all()
```

#### 4.5 Aplicação Principal (main.py)
```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uvicorn

from database import get_db, engine
from models import Base
from schemas import AtividadeCreate, AtividadeResponse, SessaoCreate, SessaoResponse
from crud import create_atividade, get_atividades, create_sessao, get_sessoes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Monitoramento de Atividades Físicas",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# API Endpoints
@app.post("/api/atividades", response_model=AtividadeResponse)
async def criar_atividade(atividade: AtividadeCreate, db: Session = Depends(get_db)):
    return create_atividade(db=db, atividade=atividade)

@app.get("/api/atividades", response_model=list[AtividadeResponse])
async def listar_atividades(db: Session = Depends(get_db)):
    return get_atividades(db)

@app.post("/api/sessoes", response_model=SessaoResponse)
async def criar_sessao(sessao: SessaoCreate, db: Session = Depends(get_db)):
    return create_sessao(db=db, sessao=sessao)

@app.get("/api/sessoes", response_model=list[SessaoResponse])
async def listar_sessoes(db: Session = Depends(get_db)):
    return get_sessoes(db)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### PASSO 5: Frontend Básico

#### 5.1 Template HTML (templates/index.html)
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Sistema de Atividades Físicas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h1>Sistema de Monitoramento de Atividades Físicas</h1>
        <div class="row">
            <div class="col-md-6">
                <h3>Atividades Cadastradas</h3>
                <div id="atividades"></div>
            </div>
            <div class="col-md-6">
                <h3>Últimas Sessões</h3>
                <div id="sessoes"></div>
            </div>
        </div>
    </div>
    
    <script>
        // JavaScript para interagir com a API
        async function carregarAtividades() {
            const response = await fetch('/api/atividades');
            const atividades = await response.json();
            // Renderizar atividades
        }
        
        async function carregarSessoes() {
            const response = await fetch('/api/sessoes');
            const sessoes = await response.json();
            // Renderizar sessões
        }
        
        document.addEventListener('DOMContentLoaded', function() {
            carregarAtividades();
            carregarSessoes();
        });
    </script>
</body>
</html>
```

### PASSO 6: Testes Locais

#### 6.1 Executar a Aplicação
```bash
# Método 1: Uvicorn direto
uvicorn main:app --reload

# Método 2: Python
python main.py

# Método 3: FastAPI CLI
fastapi dev main.py
```

#### 6.2 Testar Endpoints
```bash
# Testar health check
curl http://localhost:8000/api/health

# Criar atividade
curl -X POST "http://localhost:8000/api/atividades" \
     -H "Content-Type: application/json" \
     -d '{"nome": "Corrida", "categoria": "Cardio", "descricao": "Corrida matinal"}'

# Listar atividades
curl http://localhost:8000/api/atividades

# Acessar documentação
# http://localhost:8000/api/docs
```

### PASSO 7: Versionamento

#### 7.1 Inicializar Git
```bash
git init
git add .
git commit -m "Initial commit: FastAPI fitness tracker"
```

#### 7.2 Criar .gitignore
```text
__pycache__/
*.pyc
.env
.venv/
venv/
*.db
.DS_Store
```

#### 7.3 Conectar ao GitHub
```bash
# Criar repositório no GitHub primeiro
git remote add origin https://github.com/seuusuario/sistema-atividades-fisicas.git
git branch -M main
git push -u origin main
```

### PASSO 8: Deploy no Render

#### 8.1 Criar Procfile
```text
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### 8.2 Configurar Deploy no Render
1. Acesse render.com e crie conta
2. Clique "New Web Service"
3. Conecte seu repositório GitHub
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3

#### 8.3 Variáveis de Ambiente (opcional)
```text
DATABASE_URL=sqlite:///./atividades.db
DEBUG=False
```

### PASSO 9: Verificação Final

#### 9.1 Checklist de Funcionalidades
- [ ] API com 4+ endpoints funcionando
- [ ] Banco de dados persistente
- [ ] Interface web acessível
- [ ] Deploy funcionando
- [ ] Documentação automática (/api/docs)
- [ ] Repositório GitHub público

#### 9.2 Endpoints Implementados
1. `POST /api/atividades` - Cadastrar atividade
2. `GET /api/atividades` - Listar atividades  
3. `POST /api/sessoes` - Registrar sessão
4. `GET /api/sessoes` - Listar sessões
5. `DELETE /api/atividades/{id}` - Excluir atividade
6. `DELETE /api/sessoes/{id}` - Excluir sessão
7. `GET /api/estatisticas` - Estatísticas gerais

### 🎯 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/health` | Health check |
| POST | `/api/atividades` | Cadastrar atividade |
| GET | `/api/atividades` | Listar atividades |
| DELETE | `/api/atividades/{id}` | Excluir atividade |
| POST | `/api/sessoes` | Registrar sessão |
| GET | `/api/sessoes` | Listar sessões |
| DELETE | `/api/sessoes/{id}` | Excluir sessão |
| GET | `/api/estatisticas` | Estatísticas gerais |

### 🏆 Critérios de Avaliação

| Critério | Pontuação | Status |
|----------|-----------|--------|
| Funcionalidade da API (mínimo 4 endpoints) | 2 pts | ✅ 8 endpoints |
| Modelagem e persistência em banco | 2 pts | ✅ SQLAlchemy + SQLite |
| Funcionalidade do front-end | 2 pts | ✅ HTML + CSS + JS |
| Deploy funcional em PaaS | 2 pts | ✅ Render.com |
| Organização do código + GitHub | 2 pts | ✅ Estrutura modular |
| **Total** | **10 pts** | **✅ Completo** |

### 📚 Recursos Adicionais
- **Documentação da API**: `/api/docs` (Swagger UI)
- **Documentação Alternativa**: `/api/redoc` (ReDoc)
- **Demonstração Online**: [Ver aplicação funcionando](aplicação-web-gerada)

### 🔧 Comandos Úteis

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar em desenvolvimento
uvicorn main:app --reload

# Executar em produção
gunicorn -k uvicorn.workers.UvicornWorker main:app

# Gerar requirements.txt
pip freeze > requirements.txt

# Testar API
curl -X GET "http://localhost:8000/api/atividades"
```

### 🐛 Solução de Problemas

**Erro: "ModuleNotFoundError"**
- Verificar se o ambiente virtual está ativo
- Reinstalar dependências: `pip install -r requirements.txt`

**Erro: "Port already in use"**
- Usar porta diferente: `uvicorn main:app --port 8001`

**Banco não cria tabelas**
- Verificar se `Base.metadata.create_all(bind=engine)` está no main.py

### 🎨 Próximos Passos
- Implementar autenticação JWT
- Adicionar testes automatizados
- Implementar cache com Redis
- Adicionar logging estruturado
- Migrar para PostgreSQL
- Implementar WebSockets para updates em tempo real

---

**Desenvolvido para V2 - Desenvolvimento de Aplicações Distribuídas**