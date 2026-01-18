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
# Funções auxiliares
# =========================================================

def carregar_chesscom():
    caminho = f"{DATA_PROCESSED_PATH}/staging/staging_perfil_chesscom.csv"
    df = pd.read_csv(caminho)

    df["nome_normalizado"] = (
        df["nome"]
        .fillna(df["username"])
        .str.lower()
        .str.strip()
    )

    return df


def carregar_fide(modalidade):
    caminho = f"{DATA_PROCESSED_PATH}/staging/staging_fide_{modalidade}.csv"
    return pd.read_csv(caminho)


def preparar_fide(df, modalidade):
    df = df[[
        "fide_id",
        "nome_normalizado",
        "rating_fide",
        "jogos_fide",
        "federacao_fide",
        "ano_nascimento",
        "sexo",
        "titulo_fide"
    ]]

    df = df.rename(columns={
        "rating_fide": f"rating_fide_{modalidade}",
        "jogos_fide": f"jogos_fide_{modalidade}"
    })

    return df.drop_duplicates(subset=["fide_id", "nome_normalizado"])


# =========================================================
# Execução principal
# =========================================================

def main():
    logger.info("===== INÍCIO DIM_ENXADRISTRA =====")

    os.makedirs(DATA_ANALYTICS_PATH, exist_ok=True)

    # Base Chess.com
    df_enxadrista = carregar_chesscom()
    logger.info(f"Enxadristas Chess.com: {len(df_enxadrista)}")

    # FIDE - Standard
    df_standard = preparar_fide(carregar_fide("standard"), "standard")
    df_enxadrista = df_enxadrista.merge(
        df_standard,
        on="nome_normalizado",
        how="left"
    )

    # FIDE - Rapid
    df_rapid = preparar_fide(carregar_fide("rapid"), "rapid")
    df_enxadrista = df_enxadrista.merge(
        df_rapid,
        on="nome_normalizado",
        how="left"
    )

    # FIDE - Blitz
    df_blitz = preparar_fide(carregar_fide("blitz"), "blitz")
    df_enxadrista = df_enxadrista.merge(
        df_blitz,
        on="nome_normalizado",
        how="left"
    )

    # ID surrogate
    df_enxadrista.insert(
        0,
        "enxadrista_id",
        range(1, len(df_enxadrista) + 1)
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
        "fide_id",
        "federacao_fide",
        "ano_nascimento",
        "sexo",
        "titulo_fide",
        "rating_fide_standard",
        "jogos_fide_standard",
        "rating_fide_rapid",
        "jogos_fide_rapid",
        "rating_fide_blitz",
        "jogos_fide_blitz",
        "origem"
    ]

    df_dim = df_enxadrista[colunas_finais]

    # Salvar dimensão
    caminho_saida = f"{DATA_ANALYTICS_PATH}/dim_enxadrista.csv"
    df_dim.to_csv(caminho_saida, index=False, encoding="utf-8")

    logger.info(f"Dimensão criada com sucesso: {caminho_saida}")
    logger.info("===== FIM DIM_ENXADRISTRA =====")


if __name__ == "__main__":
    main()
