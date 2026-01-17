# ♟️ Xadrez em Números – Análise de Desempenho no Chess.com

Este projeto tem como objetivo realizar uma **análise de dados de partidas de xadrez online**, utilizando a **API pública do Chess.com**, com foco em **desempenho de jogadores, estatísticas de partidas e comparações globais**, traduzidas e contextualizadas para o **público brasileiro**.

O projeto cobre todo o pipeline de dados, desde a **coleta via API**, passando pela **modelagem analítica**, até a **visualização em dashboards interativos no Power BI**.

---

## 🎯 Objetivos do Projeto

- Analisar o desempenho de jogadores de xadrez online
- Comparar modalidades **Blitz**, **Rapid** e **Bullet**
- Acompanhar evolução de rating ao longo do tempo
- Avaliar rankings globais (Top 50)
- Explorar padrões de desempenho por país e abertura

---

## 📊 O que o dashboard responde?

- Analisar o desempenho de jogadores de xadrez online
- Comparar modalidades **Blitz**, **Rapid** e **Bullet**
- Acompanhar evolução de rating ao longo do tempo
- Avaliar rankings globais (Top 50)
- Explorar padrões de desempenho por país e abertura

---

## 🌍 Público-alvo

- Analistas de dados
- Entusiastas de xadrez
- Comunidade brasileira de BI
- Recrutadores e gestores técnicos

> Todos os dados e métricas estão **em português**, para melhor entendimento geral.

---

## 🔌 Fonte de Dados

Os dados são coletados exclusivamente a partir da **API pública do Chess.com**, que disponibiliza informações abertas e gratuitas.

Principais endpoints utilizados:
- Perfil do jogador
- Estatísticas por modalidade
- Arquivos históricos de partidas
- Classificação global (Leaderboards)
- Dados por país (Country)

Documentação oficial:  
https://www.chess.com/news/view/published-data-api

---

## 🏗️ Arquitetura e Modelagem

O projeto utiliza:
- Modelo dimensional (estrela)
- Tabelas fato com granularidade bem definida
- Dimensões reutilizáveis
- Snapshots temporais

📄 Detalhes técnicos completos em:
- `docs/arquitetura.md`
- `docs/dicionario_dados.md`

---

## 📊 Dashboards (em desenvolvimento)

Os dashboards abordarão:
- Visão geral de desempenho
- Evolução de rating
- Análise por modalidade (blitz, rapid, bullet)
- Aberturas mais jogadas e taxa de vitória
- Comparação com rankings globais
- Contexto geográfico por país

---

## 🛠️ Tecnologias Utilizadas

- Python
- API pública do Chess.com
- Pandas
- Power BI
- Git & GitHub

---

## 📌 Observações

- Todos os dados utilizados são públicos
- O projeto não realiza nenhuma ação autenticada ou privada
- As análises refletem apenas os dados disponíveis via API

---

## 🚀 Status do Projeto

🔄 Em desenvolvimento

---

## 👤 Autor

Gabriel Freire  
Projeto desenvolvido para fins de estudo, portfólio e prática em análise de dados.

