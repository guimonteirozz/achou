# ADR 0001 — Migração de Java/Spring Boot para Python/FastAPI
**Status:** Aceita (relato da equipe)

## Contexto
A equipe iniciou o backend com Java, Spring Boot e IntelliJ IDEA. O projeto apresentou dificuldades que impediram a continuidade; a causa técnica específica não foi fornecida.

## Decisão
Adotar Python 3.12+, FastAPI e Pydantic para a API REST do MVP.

## Alternativas
Corrigir a configuração do projeto Spring Boot; reiniciar a base Java; migrar para FastAPI.

## Consequências
A equipe busca simplificar o desenvolvimento e obter Swagger/OpenAPI automaticamente. A migração exige reescrever componentes e validar persistência e testes. Não significa que Java/Spring Boot sejam inadequados.
