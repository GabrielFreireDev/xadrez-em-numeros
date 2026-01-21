import os
import logging
import re

import pandas as pd
from dotenv import load_dotenv

# =========================================================
# Configurações
# =========================================================

load_dotenv()

DATA_PROCESSED_PATH = os.getenv("DATA_PROCESSED_PATH")
DATA_ANALYTICS_PATH = os.getenv("DATA_ANALYTICS_PATH")

CAMINHO_STAGING = f"{DATA_PROCESSED_PATH}/staging/staging_partidas_mensais.csv"

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
# Funções auxiliares
# =========================================================

def limpar_nome_abertura(nome_raw):
    if not nome_raw:
        return None

    # Remove sufixos com números e lances (ex: 3.c3-e6-4.Bf4)
    nome_limpo = re.split(r"\d+\.", nome_raw)[0]

    # Substitui hífens por espaço
    nome_limpo = nome_limpo.replace("-", " ")

    # Remove espaços duplicados
    nome_limpo = " ".join(nome_limpo.split())

    return nome_limpo.strip()


# =========================================================
# Execução principal
# =========================================================

def main():
    logger.info("===== INÍCIO DIM_ECO_ABERTURAS =====")

    os.makedirs(DATA_ANALYTICS_PATH, exist_ok=True)

    df = pd.read_csv(CAMINHO_STAGING)

    logger.info(f"Partidas carregadas: {len(df)}")

    # valores únicos de abertura
    df_eco = (
        df[["eco_abertura_raw"]]
        .dropna()
        .drop_duplicates()
        .rename(columns={"eco_abertura_raw": "eco_abertura"})
        .reset_index(drop=True)
    )

    logger.info(f"Aberturas únicas encontradas: {len(df_eco)}")

    # nome reduzido
    df_eco["eco_nome_reduzido"] = df_eco["eco_abertura"].apply(limpar_nome_abertura)

    # origem
    df_eco["origem"] = "chess.com"

    # surrogate key
    df_eco.insert(0, "eco_id", range(1, len(df_eco) + 1))

    caminho_saida = f"{DATA_ANALYTICS_PATH}/dim_eco_aberturas.csv"
    df_eco.to_csv(caminho_saida, index=False, encoding="utf-8")

    logger.info(f"Dimensão criada com sucesso: {caminho_saida}")
    logger.info("===== FIM DIM_ECO_ABERTURAS =====")


if __name__ == "__main__":
    main()
