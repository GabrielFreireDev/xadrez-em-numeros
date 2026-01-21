# 📘 Dicionário de Dados – Xadrez em Números

Este documento descreve as tabelas e colunas do modelo dimensional do projeto **Xadrez em Números**, bem como suas responsabilidades e relacionamentos.

O modelo foi construído com foco em análise exploratória e informativa, priorizando flexibilidade no Power BI e clareza para fins de portfólio.

---

## 📘 Dimensões

### ♟️ dim_enxadrista

Dimensão que representa os enxadristas analisados no projeto, com dados oriundos da API do Chess.com.

| Coluna | Descrição |
|------|-----------|
| enxadrista_id | Identificador surrogate do enxadrista |
| player_id_api | Identificador do enxadrista na API do Chess.com |
| username | Nome de usuário no Chess.com |
| nome | Nome real do enxadrista |
| avatar_url | URL da imagem de perfil |
| perfil_url | URL do perfil no Chess.com |
| seguidores | Quantidade de seguidores |
| status | Status da conta no Chess.com |
| eh_streamer | Indica se o enxadrista é streamer |
| verificado | Indica se a conta é verificada |
| data_entrada | Data de entrada no Chess.com |
| pais_id | Chave estrangeira para `dim_pais` |
| titulo_chesscom | Título exibido no Chess.com (GM, IM, FM etc.) |

---

### 🌍 dim_pais

Dimensão que representa os países associados aos enxadristas.

| Coluna | Descrição |
|------|-----------|
| pais_id | Sigla ISO do país |
| nome_pais | Nome do país |
| continente | Continente do país |
| regiao | Região geográfica |
| bandeira_url | URL da bandeira do país |

---

### ♟️ dim_ECO_aberturas

Dimensão que cataloga as aberturas de xadrez utilizadas nas partidas.

> A API do Chess.com não fornece o código ECO estruturado de forma direta.  
> As aberturas são derivadas a partir da URL fornecida pela API.

| Coluna | Descrição |
|------|-----------|
| eco_id | Identificador surrogate da abertura |
| eco_abertura | Nome completo da abertura extraído da URL |
| eco_nome_reduzido | Nome limpo da abertura, sem traços ou movimentos |
| origem | Origem dos dados (`chess.com`) |

---

## 📕 Tabelas Fato

### 📊 fat_estatisticas_enxadrista

Tabela fato de **snapshot**, contendo estatísticas acumuladas do enxadrista por modalidade e data de referência.

| Coluna | Descrição |
|------|-----------|
| enxadrista_id | Chave estrangeira para `dim_enxadrista` |
| modalidade_id | Chave estrangeira para `dim_modalidade` |
| data_referencia | Data de referência do snapshot |
| rating_atual | Rating atual do enxadrista |
| melhor_rating | Melhor rating histórico |
| data_rating_melhor | Data em que o melhor rating foi atingido |
| vitorias | Total de vitórias |
| derrotas | Total de derrotas |
| empates | Total de empates |

---

### 🏆 fat_classificacao

Tabela fato de **snapshot**, representando a classificação geral dos enxadristas nos rankings do Chess.com.

| Coluna | Descrição |
|------|-----------|
| enxadrista_id | Chave estrangeira para `dim_enxadrista` |
| pais_id | Chave estrangeira para `dim_pais` |
| modalidade_id | Chave estrangeira para `dim_modalidade` |
| data_referencia | Data de referência do ranking |
| posicao_ranking | Posição no ranking |
| rating | Rating no ranking |
| vitorias | Total de vitórias |
| derrotas | Total de derrotas |
| empates | Total de empates |

---

### ♟️📊 fat_partidas_mensais

Tabela fato **granular**, no nível de **uma linha por partida**, contendo informações detalhadas das partidas jogadas.

> Atualmente, a tabela contém partidas apenas do enxadrista `lpsupi`,  
> mas foi modelada para suportar partidas de qualquer enxadrista futuramente.

| Coluna | Tipo | Descrição |
|------|------|-----------|
| partida_url | string | URL única da partida no Chess.com |
| data | date | Data de término da partida |
| rated | boolean | Indica se a partida foi ranqueada |
| precisao_brancas | float | Acurácia das peças brancas (%) |
| precisao_pretas | float | Acurácia das peças pretas (%) |
| modalidade | string | Modalidade da partida (blitz, rapid, bullet etc.) |
| regras | string | Tipo de regra aplicada (ex: chess) |
| rating_brancas | integer | Rating das brancas no momento da partida |
| resultado_brancas | string | Resultado das brancas (PT-BR) |
| brancas_username | string | Username das brancas (minúsculo) |
| brancas_@id | string | Identificador da API Chess.com (brancas) |
| rating_pretas | integer | Rating das pretas no momento da partida |
| resultado_pretas | string | Resultado das pretas (PT-BR) |
| pretas_username | string | Username das pretas (minúsculo) |
| pretas_@id | string | Identificador da API Chess.com (pretas) |
| eco_id | integer | Chave estrangeira para `dim_ECO_aberturas` |
| origem | string | Origem dos dados (`chess.com`) |

---

## 📌 Observações Gerais

- Não há métricas agregadas pré-calculadas nas tabelas fato.
- Todos os cálculos analíticos são realizados no Power BI.
- O modelo prioriza clareza, escalabilidade e valor demonstrativo para portfólio.
- Algumas entidades (como adversários das partidas) podem não existir nas dimensões.
