import os
import logging

import pandas as pd
from dotenv import load_dotenv

# =========================================================
# Configurações
# =========================================================

load_dotenv()

DATA_RAW_PATH = os.getenv("DATA_RAW_PATH")
DATA_PROCESSED_PATH = os.getenv("DATA_PROCESSED_PATH")

ARQUIVOS_FIDE = {
    "standard": f"{DATA_RAW_PATH}/fide/standard_rating_list.txt",
    "rapid": f"{DATA_RAW_PATH}/fide/rapid_rating_list.txt",
    "blitz": f"{DATA_RAW_PATH}/fide/blitz_rating_list.txt",
}

# =========================================================
# Layout ORIGINAL do arquivo FIDE (fixed-width)
# =========================================================

COLUNAS_FIDE_ORIGINAIS = [
    "id_number",   # ID Number
    "name",        # Name
    "fed",         # Fed
    "sex",         # Sex
    "tit",         # Tit
    "wtit",        # WTit
    "otit",        # OTit
    "foa",         # FOA
    "rating",      # JAN26 (rating do mês)
    "gms",         # Gms
    "k",           # K
    "b_day",       # B-day
    "flag"         # Flag
]

# Largura fixa de cada coluna (em caracteres)
WIDTHS_FIDE = [
    10,  # ID Number
    60,  # Name
    4,   # Fed
    4,   # Sex
    5,   # Tit
    6,   # WTit
    6,   # OTit
    6,   # FOA
    6,   # Rating
    5,   # Gms
    3,   # K
    7,   # B-day
    4    # Flag
]

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

def carregar_fide_por_modalidade(modalidade, caminho_arquivo):
    logger.info(f"Processando arquivo FIDE ({modalidade})")

    df = pd.read_fwf(
        caminho_arquivo,
        widths=WIDTHS_FIDE,
        names=COLUNAS_FIDE_ORIGINAIS
    )

    # Limpeza básica
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Tradução das colunas para português (camada staging)
    df = df.rename(columns={
        "id_number": "fide_id",
        "name": "nome",
        "fed": "federacao_fide",
        "sex": "sexo",
        "tit": "titulo_fide",
        "wtit": "titulo_feminino_fide",
        "otit": "outro_titulo_fide",
        "foa": "federacao_origem",
        "rating": "rating_fide",
        "gms": "jogos_fide",
        "k": "fator_k",
        "b_day": "ano_nascimento",
        "flag": "flag"
    })

    # Campos auxiliares
    df["modalidade_fide"] = modalidade
    df["nome_normalizado"] = df["nome"].str.lower().str.strip()

    return df


def salvar_staging(df, modalidade):
    os.makedirs(f"{DATA_PROCESSED_PATH}/staging", exist_ok=True)

    caminho = f"{DATA_PROCESSED_PATH}/staging/staging_fide_{modalidade}.csv"
    df.to_csv(caminho, index=False, encoding="utf-8")

    logger.info(f"Staging FIDE salva: {caminho}")

# =========================================================
# Execução principal
# =========================================================

def main():
    logger.info("===== INÍCIO EXTRAÇÃO FIDE =====")

    for modalidade, caminho in ARQUIVOS_FIDE.items():
        if not os.path.exists(caminho):
            logger.warning(f"Arquivo não encontrado: {caminho}")
            continue

        df_fide = carregar_fide_por_modalidade(modalidade, caminho)
        salvar_staging(df_fide, modalidade)

    logger.info("===== FIM EXTRAÇÃO FIDE =====")


if __name__ == "__main__":
    main()
