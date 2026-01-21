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

CAMINHO_STAGING = f"{DATA_PROCESSED_PATH}/staging/staging_partidas_mensais.csv"
CAMINHO_DIM_ECO = f"{DATA_ANALYTICS_PATH}/dim_eco_aberturas.csv"

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
# Execução principal
# =========================================================

def main():
    logger.info("===== INÍCIO FATO_PARTIDAS_MENSAIS =====")

    os.makedirs(DATA_ANALYTICS_PATH, exist_ok=True)

    # -----------------------------------------------------
    # Carregamentos
    # -----------------------------------------------------

    df_partidas = pd.read_csv(CAMINHO_STAGING)
    logger.info(f"Partidas carregadas (staging): {len(df_partidas)}")

    df_eco = pd.read_csv(CAMINHO_DIM_ECO)
    logger.info(f"Aberturas carregadas (dimensão): {len(df_eco)}")

    # -----------------------------------------------------
    # Merge com dimensão ECO
    # -----------------------------------------------------

    df_fato = df_partidas.merge(
        df_eco[["eco_id", "eco_abertura"]],
        how="left",
        left_on="eco_abertura_raw",
        right_on="eco_abertura"
    )

    # -----------------------------------------------------
    # Remoção de colunas auxiliares
    # -----------------------------------------------------

    df_fato = df_fato.drop(columns=["eco_abertura_raw", "eco_abertura"])

    # -----------------------------------------------------
    # Ordenação opcional (data)
    # -----------------------------------------------------

    if "data" in df_fato.columns:
        df_fato = df_fato.sort_values("data")

    # -----------------------------------------------------
    # Gravação final
    # -----------------------------------------------------

    caminho_saida = f"{DATA_ANALYTICS_PATH}/fat_partidas_mensais.csv"
    df_fato.to_csv(caminho_saida, index=False, encoding="utf-8")

    logger.info(f"Fato criada com sucesso: {caminho_saida}")
    logger.info("===== FIM FATO_PARTIDAS_MENSAIS =====")


if __name__ == "__main__":
    main()
