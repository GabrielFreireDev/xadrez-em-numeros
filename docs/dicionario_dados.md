# Dicionário de Dados – Xadrez em números

Este documento descreve todas as tabelas e colunas do modelo dimensional do projeto.

---

## 📘 Dimensões

### dim_enxadrista

| Coluna                | Descrição |
|-----------------------|-----------|
| enxadrista_id         | Identificador interno do enxadrista |
| player_id_api         | Identificador do enxadrista na API do Chess.com |
| username              | Nome de usuário no Chess.com |
| nome                  | Nome real do enxadrista |
| avatar_url            | URL da imagem do perfil |
| perfil_url            | Link do perfil no Chess.com |
| seguidores            | Quantidade de seguidores |
| status                | Status da conta no Chess.com |
| eh_streamer           | Indica se o enxadrista é streamer |
| verificado            | Indica se a conta é verificada |
| data_entrada          | Data de entrada no Chess.com |
| pais_id               | Chave estrangeira para dim_pais |
| titulo_chesscom       | Título exibido no Chess.com (GM, IM, FM etc.) |



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

## 📕 Tabelas Fato

### fato_estatisticas enxadrista

| Coluna              | Descrição |
|---------------------|-----------|
| enxadrista_id       | Chave estrangeira para dim enxadrista |
| modalidade_id       | Chave estrangeira para dim_modalidade |
| data_id             | Data do snapshot |
| rating_atual        | Rating atual do enxadrista |
| melhor_rating       | Melhor rating histórico |
| data_rating_melhor  | Data com melhor rating histórico |
| vitorias            | Total de vitórias |
| derrotas            | Total de derrotas |
| empates             | Total de empates |

---

### fato_classificacao

| Coluna           | Descrição |
|------------------|-----------|
| enxadrista_id    | Chave estrangeira para dim enxadrista |
| pais_id          | Chave estrangeira para dim_pais |
| modalidade_id    | Chave estrangeira para dim_modalidade |
| data_id          | Data do snapshot |
| posicao_ranking  | Posição no ranking |
| rating           | Rating no ranking |
| vitorias         | Total de vitórias |
| derrotas         | Total de derrotas |
| empates          | Total de empates |


