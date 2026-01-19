import os
import logging
from datetime import date

import requests
import pandas as pd
from dotenv import load_dotenv

# =========================================================
# Configurações
# =========================================================

load_dotenv()

DATA_ANALYTICS_PATH = os.getenv("DATA_ANALYTICS_PATH")
DATA_PROCESSED_PATH = os.getenv("DATA_PROCESSED_PATH")

URL_LEADERBOARD = "https://api.chess.com/pub/leaderboards"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ChesscomBI/1.0; +https://github.com/gabrielfreiredev/xadrez-em-numeros)"
}

MODALIDADES = {
    "live_blitz": "blitz",
    "live_rapid": "rapid",
    "live_bullet": "bullet"
}

# =========================================================
# Logging
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# =========================================================
# Funções
# =========================================================

def carregar_dim_enxadrista():
    caminho = f"{DATA_ANALYTICS_PATH}/dim_enxadrista.csv"
    return pd.read_csv(caminho)


def coletar_leaderboard():
    response = requests.get(URL_LEADERBOARD, timeout=30, headers=HEADERS)
    response.raise_for_status()
    return response.json()


# =========================================================
# Execução principal
# =========================================================

def main():
    logger.info("===== INÍCIO FACT_LEADERBOARD =====")

    os.makedirs(DATA_ANALYTICS_PATH, exist_ok=True)

    df_dim = carregar_dim_enxadrista()
    logger.info(f"Enxadristas na dimensão: {len(df_dim)}")

    leaderboard_json = coletar_leaderboard()
    data_ref = date.today()

    registros = []

    for chave_api, modalidade in MODALIDADES.items():
        logger.info(f"Processando modalidade: {modalidade}")

        jogadores = leaderboard_json.get(chave_api, [])

        for jogador in jogadores:
            registros.append({
                "player_id": jogador["player_id"],
                "modalidade": modalidade,
                "data_referencia": data_ref,
                "posicao": jogador.get("rank"),
                "rating": jogador.get("score"),
                "vitorias": jogador.get("win_count"),
                "derrotas": jogador.get("loss_count"),
                "empates": jogador.get("draw_count")
            })

    df_fact = pd.DataFrame(registros)

    # Merge com dimensão
    df_fact = df_fact.merge(
        df_dim[["enxadrista_id", "player_id"]],
        on="player_id",
        how="left"
    )

    # Seleção final
    colunas_finais = [
        "player_id",
        "modalidade",
        "data_referencia",
        "posicao",
        "rating",
        "vitorias",
        "derrotas",
        "empates"
    ]

    df_fact = df_fact[colunas_finais]

    caminho_saida = f"{DATA_ANALYTICS_PATH}/fat_classificacao.csv"
    df_fact.to_csv(caminho_saida, index=False, encoding="utf-8")

    logger.info(f"Fact criada com sucesso: {caminho_saida}")
    logger.info("===== FIM FACT_CLASSIFICACAO =====")


if __name__ == "__main__":
    main()
