import os
import logging

import pandas as pd
from dotenv import load_dotenv

# =========================================================
# Configurações
# =========================================================

load_dotenv()

DATA_PROCESSED_PATH = os.getenv("DATA_PROCESSED_PATH")
DATA_ANALYTICS_PATH = os.getenv("DATA_ANALYTICS_PATH")

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

def carregar_perfil_chesscom():
    caminho = f"{DATA_PROCESSED_PATH}/staging/staging_perfil_chesscom.csv"
    return pd.read_csv(caminho)


# =========================================================
# Execução principal
# =========================================================

def main():
    logger.info("===== INÍCIO DIM_ENXADRISTRA =====")

    os.makedirs(DATA_ANALYTICS_PATH, exist_ok=True)

    df = carregar_perfil_chesscom()
    logger.info(f"Enxadristas carregados: {len(df)}")

    # ID surrogate
    df.insert(
        0,
        "enxadrista_id",
        range(1, len(df) + 1)
    )

    # Seleção final de colunas
    colunas_finais = [
        "enxadrista_id",
        "player_id",
        "username",
        "nome",
        "titulo",
        "pais",
        "avatar",
        "seguidores",
        "data_entrada",
        "status",
        "is_streamer",
        "verificado",
        "origem"
    ]

    df_dim = df[colunas_finais]

    caminho_saida = f"{DATA_ANALYTICS_PATH}/dim_enxadrista.csv"
    df_dim.to_csv(caminho_saida, index=False, encoding="utf-8")

    logger.info(f"Dimensão criada com sucesso: {caminho_saida}")
    logger.info("===== FIM DIM_ENXADRISTRA =====")


if __name__ == "__main__":
    main()
