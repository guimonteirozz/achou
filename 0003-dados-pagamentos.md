# ADR 0003 — PostgreSQL e pagamento simulado
**Status:** PostgreSQL escolhido; pagamento mock planejado

## Contexto
Pedidos e produtos exigem consistência relacional; gateway real adiciona dependências e custos de integração.

## Decisão
Usar PostgreSQL como banco principal e SQLAlchemy 2 com Psycopg 3. Simular pagamentos na próxima fase do MVP.

## Alternativas
Banco não relacional; gateway de pagamento real desde o início.

## Consequências
Facilita modelagem transacional e evita cobranças reais na fase acadêmica. O mock não demonstra segurança ou conformidade de processamento financeiro. SQLite é usado somente na execução simplificada e nos testes isolados.
