# Achou! — Marketplace de E-commerce | Backend 03

**Equipe:** Paulo Augusto e Guilherme Monteiro  
**Status:** implementação acadêmica de referência, não validação do repositório original.

## 1. Contexto do negócio
O Achou! conecta pequenos vendedores a compradores por meio de um marketplace digital. A plataforma pretende reunir catálogo, busca, carrinho, checkout, pagamentos e avaliações, simplificando a descoberta e comercialização de produtos. O principal desafio de arquitetura é lidar com picos sazonais de até 20 vezes o tráfego habitual.

## 2. Objetivo e escopo
Construir uma API REST documentada e testada para iniciar o backend do marketplace. **Nesta versão de referência estão implementados**: cadastro, listagem e consulta de produtos, além de verificação de saúde. Carrinho, pedidos, pagamentos simulados, vendedores e avaliações estão no backlog; não são funcionalidades concluídas.

### Requisitos não funcionais
- Meta de disponibilidade em operação normal: 99,5% (não medida nesta versão).
- Campanhas promocionais: objetivo de evitar indisponibilidade, sem garantia técnica de zero falhas.
- Pico esperado: 20x; exige testes de carga e planejamento de capacidade antes da produção.
- Segurança: validação de dados; autenticação e autorização ainda precisam ser implementadas.

## 3. Stack tecnológica
| Categoria | Tecnologia | Finalidade |
|---|---|---|
| Linguagem | Python 3.12+ | Backend |
| Framework | FastAPI | API REST |
| Validação | Pydantic 2 | Contratos e validação |
| ORM | SQLAlchemy 2 | Persistência |
| Banco principal | PostgreSQL | Dados relacionais |
| Driver | Psycopg 3 | Conexão PostgreSQL |
| Servidor | Uvicorn | ASGI |
| Testes | Pytest + HTTPX | Testes automatizados |
| Documentação | Swagger / OpenAPI | Contratos da API |
| Versionamento | Git + GitHub | Histórico e colaboração |
| Testes locais isolados | SQLite | Simplificação dos testes, não substitui testes de integração com PostgreSQL |

**Fora do MVP:** Redis, nuvem, balanceamento de carga e múltiplas instâncias.

## 4. Arquitetura proposta
Padrão: **monólito modular**; nesta versão inicial os endpoints ainda estão concentrados em `app/main.py` e a separação em módulos faz parte da próxima etapa.

```mermaid
flowchart TD
    C[Cliente / Swagger] --> API[FastAPI - Rotas REST]
    API --> V[Pydantic - Validação]
    V --> S[Serviços de domínio - evolução]
    S --> R[Repositórios SQLAlchemy - evolução]
    R --> DB[(PostgreSQL)]
    API --> ORM[SQLAlchemy - implementação atual]
    ORM --> DB
    S -. futura integração .-> P[Pagamento Mock]
    API -. evolução .-> CACHE[(Redis)]
```

## 5. Plano de desenvolvimento
| Etapa | Atividades | Critério de aceite |
|---|---|---|
| 1. Planejamento | Contexto, backlog, stack, ADRs | README e decisões registradas |
| 2. Ambiente | Python, dependências, banco, Git | API inicia localmente |
| 3. Catálogo | Modelagem e três endpoints de produtos | POST/GET/GET por ID respondem |
| 4. Qualidade | Pytest, HTTPX, casos de erro | Testes passam no ambiente da equipe |
| 5. Carrinho e pedidos | Regras, persistência e contratos | Fluxo de compra demonstrável |
| 6. Pagamento mock | Aprovação/recusa simuladas | Pedidos atualizam estado corretamente |
| 7. Preparação | Documentação, segurança, carga e demonstração | Evidências e limitações apresentadas |

## 6. Como executar no Windows 11
Pré-requisitos: Python 3.12+, Docker Desktop (opcional para PostgreSQL) e Git.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

**Opção A — execução rápida local:** sem definir `DATABASE_URL`, a API utiliza `sqlite:///./achou_dev.db` apenas para desenvolvimento.

```powershell
uvicorn app.main:app --reload
```

**Opção B — PostgreSQL (recomendado para integração):**

```powershell
docker compose up -d
$env:DATABASE_URL="postgresql+psycopg://achou:achou@localhost:5432/achou"
uvicorn app.main:app --reload
```

Abra `http://127.0.0.1:8000/docs` para testar via Swagger. A criação automática de tabelas é uma simplificação acadêmica; em produção, adotar migrações (por exemplo, Alembic).

## 7. Endpoints implementados na referência
| Método | Rota | Resultado |
|---|---|---|
| GET | `/health` | Saúde da aplicação |
| POST | `/produtos` | Cadastra produto (201) |
| GET | `/produtos` | Lista produtos (200) |
| GET | `/produtos/{produto_id}` | Consulta produto (200 ou 404) |

Exemplo de POST `/produtos`:

```json
{"nome":"Teclado","preco":"99.90","estoque":4}
```

Exemplo de resposta (ID ilustrativo):

```json
{"id":1,"nome":"Teclado","preco":"99.90","estoque":4}
```

Validação de dados inválidos retorna **422**. Os exemplos são da implementação incluída neste pacote; não comprovam que os endpoints existem no projeto anterior da equipe.

## 8. Testes automatizados
```powershell
python -m pytest -v
```

Casos: saúde, cadastro/listagem/consulta, produto inexistente e validação. Testes usam SQLite temporário e **não** comprovam integração com PostgreSQL nem capacidade sob pico de tráfego. Antes da entrega final, executar e registrar o resultado no ambiente real.

## 9. Histórico de decisão
O projeto começou com Java, Spring Boot e IntelliJ IDEA. Após dificuldades técnicas que impediram a continuidade, a equipe optou por Python/FastAPI. A causa específica da falha inicial não foi documentada; portanto, não se atribui o problema ao Java ou ao Spring Boot. Consultar `docs/adr/`.

## 10. Entregáveis e pendências
- [x] README com plano e documentação
- [x] Contexto do negócio e stack
- [x] Diagrama Mermaid da arquitetura proposta
- [x] Implementação de referência com 3 endpoints de produto e health
- [x] Testes automatizados escritos
- [x] ADRs iniciais
- [ ] Validar testes no ambiente da equipe e anexar evidências
- [ ] Implementar carrinho, pedidos e pagamento mock
- [ ] Autenticação, autorização e controle de acesso
- [ ] Separar serviços/repositórios em módulos
- [ ] Testes de integração com PostgreSQL e testes de carga
- [ ] Publicar no repositório oficial da equipe
