# Dicionário de Dados – Xadrez em números

Este documento descreve todas as tabelas e colunas do modelo dimensional do projeto.

---

## 📘 Dimensões

### dim_jogador

| Coluna          | Descrição |
|-----------------|-----------|
| jogador_id      | Identificador interno do jogador |
| player_id_api   | Identificador original da API do Chess.com |
| username        | Nome de usuário no Chess.com |
| nome            | Nome real do jogador |
| titulo          | Título oficial (GM, IM, FM, etc.) |
| avatar_url      | URL da imagem do perfil |
| perfil_url      | Link do perfil no Chess.com |
| seguidores      | Quantidade de seguidores |
| pais_id         | Chave estrangeira para dim_pais |
| data_entrada    | Data de entrada no Chess.com |
| status          | Status da conta |
| eh_streamer     | Indica se o jogador é streamer |
| verificado      | Indica se a conta é verificada |

---

### dim_pais

| Coluna       | Descrição |
|--------------|-----------|
| pais_id      | Identificador interno do país |
| codigo_pais  | Código ISO do país (BR, US, etc.) |
| nome_pais    | Nome do país |
| continente   | Continente |
| regiao       | Região geográfica |
| bandeira_url | URL da bandeira do país |

---

### dim_modalidade

| Coluna            | Descrição |
|-------------------|-----------|
| modalidade_id     | Identificador da modalidade |
| nome_modalidade   | Nome da modalidade (Blitz, Rapid, Bullet) |
| slug_stats        | Identificador usado na API de estatísticas |
| slug_leaderboard  | Identificador usado na API de ranking |
| minutos_min       | Tempo mínimo da modalidade |
| minutos_max       | Tempo máximo da modalidade |

---

### dim_calendario

| Coluna            | Descrição |
|-------------------|-----------|
| data_id           | Identificador no formato YYYYMMDD |
| data_completa     | Data completa |
| dia               | Dia do mês |
| nome_dia          | Nome do dia da semana |
| mes               | Número do mês |
| nome_mes          | Nome do mês |
| trimestre         | Trimestre do ano |
| ano               | Ano |
| eh_fim_de_semana  | Indica se é fim de semana |

---

### dim_abertura

| Coluna       | Descrição |
|--------------|-----------|
| abertura_id  | Identificador da abertura |
| eco_codigo   | Código ECO (ex: B12, C45) |
| nome_abertura| Nome da abertura |
| familia      | Família da abertura |

---

## 📕 Tabelas Fato

### fato_partidas_mensal

| Coluna                      | Descrição |
|-----------------------------|-----------|
| jogador_id                  | Chave estrangeira para dim_jogador |
| modalidade_id               | Chave estrangeira para dim_modalidade |
| data_id                     | Chave estrangeira para dim_tempo (mês) |
| total_partidas              | Total de partidas no mês |
| vitorias                    | Total de vitórias |
| derrotas                    | Total de derrotas |
| empates                     | Total de empates |
| partidas_ranqueadas         | Quantidade de partidas ranqueadas |
| rating_medio_jogador        | Rating médio do jogador |
| rating_medio_adversario     | Rating médio dos adversários |
| diferenca_media_rating      | Diferença média de rating |
| duracao_media_partida_seg   | Duração média das partidas (segundos) |
| partidas_brancas            | Partidas jogadas com peças brancas |
| partidas_pretas             | Partidas jogadas com peças pretas |
| abertura_mais_jogada_id     | Chave estrangeira para dim_abertura |

---

### fato_estatisticas_jogador

| Coluna              | Descrição |
|---------------------|-----------|
| jogador_id          | Chave estrangeira para dim_jogador |
| modalidade_id       | Chave estrangeira para dim_modalidade |
| data_id             | Data do snapshot |
| rating_atual        | Rating atual do jogador |
| melhor_rating       | Melhor rating histórico |
| vitorias            | Total de vitórias |
| derrotas            | Total de derrotas |
| empates             | Total de empates |

---

### fato_classificacao

| Coluna           | Descrição |
|------------------|-----------|
| jogador_id       | Chave estrangeira para dim_jogador |
| pais_id          | Chave estrangeira para dim_pais |
| modalidade_id    | Chave estrangeira para dim_modalidade |
| data_id          | Data do snapshot |
| posicao_ranking  | Posição no ranking |
| rating           | Rating no ranking |
| vitorias         | Total de vitórias |
| derrotas         | Total de derrotas |
| empates          | Total de empates |

