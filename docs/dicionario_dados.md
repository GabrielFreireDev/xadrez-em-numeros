
---

# 📄 docs/dicionario_dados.md

```md
# Dicionário de Dados – Xadrez em Números

Este documento descreve todas as tabelas e colunas do modelo dimensional.

---

## 📘 Dimensões

### dim_jogador
| Coluna | Descrição |
|------|----------|
| jogador_id | Identificador interno |
| player_id_api | ID original da API |
| username | Nome do usuário |
| nome | Nome real |
| titulo | GM, IM, FM etc |
| avatar_url | Imagem do perfil |
| perfil_url | Link do Chess.com |
| seguidores | Nº de seguidores |
| pais_id | FK dim_pais |
| data_entrada | Data de entrada no Chess.com |
| status | Status da conta |
| eh_streamer | Indicador de streamer |
| verificado | Conta verificada |

---

### dim_pais
| Coluna | Descrição |
|------|----------|
| pais_id | Identificador |
| codigo_pais | ISO (BR, US) |
| nome_pais | Nome do país |
| continente | Continente |
| regiao | Região |
| bandeira_url | URL da bandeira |

---

### dim_modalidade
| Coluna | Descrição |
|------|----------|
| modalidade_id | Identificador |
| nome_modalidade | Blitz, Rapid, Bullet |
| slug_stats | Identificador na API |
| slug_leaderboard | Identificador leaderboard |
| minutos_min | Tempo mínimo |
| minutos_max | Tempo máximo |

---

### dim_tempo
| Coluna | Descrição |
|------|----------|
| data_id | YYYYMMDD |
| data_completa | Data |
| dia | Dia |
| nome_dia | Nome do dia |
| mes | Mês |
| nome_mes | Nome do mês |
| trimestre | Trimestre |
| ano | Ano |
| eh_fim_de_semana | Boolean |

---

## 📕 Tabelas Fato

### fato_partidas_mensal
| Coluna | Descrição |
|------|----------|
| jogador_id | FK |
| modalidade_id | FK |
| data_id | FK (mês) |
| total_partidas | Total |
| vitorias | Vitórias |
| derrotas | Derrotas |
| empates | Empates |
| partidas_ranqueadas | Jogos rated |
| rating_medio_jogador | Rating médio |
| rating_medio_adversario | Rating adversário |
| diferenca_media_rating | Diferença |
| duracao_media_partida_seg | Duração média |
| partidas_brancas | Jogos de brancas |
| partidas_pretas | Jogos de pretas |
| abertura_mais_jogada_id | FK dim_abertura |

---

### fato_estatisticas_jogador
| Coluna | Descrição |
|------|----------|
| jogador_id | FK |
| modalidade_id | FK |
| data_id | Snapshot |
| rating_atual | Rating atual |
| melhor_rating | Melhor rating |
| vitorias | Total |
| derrotas | Total |
| empates | Total |

---

### fato_classificacao
| Coluna | Descrição |
|------|----------|
| jogador_id | FK |
| pais_id | FK |
| modalidade_id | FK |
| data_id | Snapshot |
| posicao_ranking | Ranking |
| rating | Rating |
| vitorias | Vitórias |
| derrotas | Derrotas |
| empates | Empates |

