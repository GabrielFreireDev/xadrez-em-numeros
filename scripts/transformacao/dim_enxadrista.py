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

CAMINHO_DIM_PAIS = f"{DATA_PROCESSED_PATH}/dimensoes_auxiliares/dim_pais_ptbr.csv"

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


def carregar_dim_pais():
    return pd.read_csv(CAMINHO_DIM_PAIS)


# =========================================================
# Execução principal
# =========================================================

def main():
    logger.info("===== INÍCIO DIM_ENXADRISTRA =====")

    os.makedirs(DATA_ANALYTICS_PATH, exist_ok=True)

    # -----------------------------------------------------
    # Carregamento dos dados
    # -----------------------------------------------------

    df_enxadrista = carregar_perfil_chesscom()
    logger.info(f"Enxadristas carregados: {len(df_enxadrista)}")

    df_pais = carregar_dim_pais()
    logger.info(f"Países carregados: {len(df_pais)}")

    # -----------------------------------------------------
    # Merge com dim_pais
    # -----------------------------------------------------

    df_merge = df_enxadrista.merge(
        df_pais[["pais_id", "continente", "bandeira_url", "nome_pais"]],
        how="left",
        left_on="pais",
        right_on="pais_id"
    )

    # Regras para países não encontrados
    df_merge["continente"] = df_merge["continente"].fillna("Não Informado")

    # -----------------------------------------------------
    # Criação do ID surrogate
    # -----------------------------------------------------

    df_merge.insert(
        0,
        "enxadrista_id",
        range(1, len(df_merge) + 1)
    )

    # -----------------------------------------------------
    # Seleção final de colunas
    # -----------------------------------------------------

    colunas_finais = [
        "enxadrista_id",
        "@id",
        "url",
        "player_id",
        "username",
        "nome",
        "titulo",
        "pais",
        "nome_pais",
        "continente",
        "bandeira_url",
        "avatar",
        "seguidores",
        "data_entrada",
        "status",
        "is_streamer",
        "verificado",
        "origem"
    ]

    df_dim = df_merge[colunas_finais]

    caminho_saida = f"{DATA_ANALYTICS_PATH}/dim_enxadrista.csv"
    df_dim.to_csv(caminho_saida, index=False, encoding="utf-8")

    logger.info(f"Dimensão criada com sucesso: {caminho_saida}")
    logger.info("===== FIM DIM_ENXADRISTRA =====")


if __name__ == "__main__":
    main()
