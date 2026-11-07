# ADR 0002 — Monólito modular
**Status:** Proposta aceita para o MVP

## Contexto
Equipe pequena, prazo acadêmico e necessidade de reduzir complexidade operacional.

## Decisão
Adotar uma aplicação REST única, evoluindo a organização interna para módulos de catálogo, carrinho, pedidos e pagamentos.

## Alternativas
Microsserviços e serverless.

## Consequências
Facilita testes e execução local. Exige disciplina de separação de responsabilidades. A implementação de referência ainda concentra rotas e persistência em um arquivo; a modularização é pendência explícita.
