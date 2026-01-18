import os
import json
import logging
from datetime import date

import requests
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

# =========================================================
# Configurações iniciais
# =========================================================

load_dotenv()

DATA_RAW_PATH = os.getenv("DATA_RAW_PATH")
DATA_PROCESSED_PATH = os.getenv("DATA_PROCESSED_PATH")

URL_BASE_LEADERBOARD = "https://api.chess.com/pub/leaderboards"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ChesscomBI/1.0; +https://github.com/gabrielfreiredev/xadrez-em-numeros)"
    }

MODALIDADES = {
    "blitz": "live_blitz",
    "rapid": "live_rapid",
    "bullet": "live_bullet"
}

DATA_SNAPSHOT = date.today().isoformat()

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

def criar_diretorios():
    os.makedirs(f"{DATA_RAW_PATH}/leaderboard", exist_ok=True)
    os.makedirs(f"{DATA_PROCESSED_PATH}/staging", exist_ok=True)


def coletar_leaderboard():
    logger.info("Iniciando coleta do leaderboard do Chess.com")

    resposta = requests.get(URL_BASE_LEADERBOARD, headers=HEADERS)
    resposta.raise_for_status()

    dados = resposta.json()
    logger.info("Leaderboard coletado com sucesso")

    return dados


def salvar_json_bruto(dados):
    caminho_arquivo = f"{DATA_RAW_PATH}/leaderboard/leaderboard_{DATA_SNAPSHOT}.json"

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    logger.info(f"Arquivo bruto salvo em: {caminho_arquivo}")


def gerar_staging_enxadristas_top(dados):
    registros = []

    for nome_modalidade, chave_api in MODALIDADES.items():
        logger.info(f"Processando modalidade: {nome_modalidade}")

        for jogador in tqdm(dados[chave_api], desc=f"{nome_modalidade}"):
            registros.append({
                "username": jogador.get("username"),
                "modalidade": nome_modalidade,
                "posicao_ranking": jogador.get("rank"),
                "rating": jogador.get("rating"),
                "data_snapshot": DATA_SNAPSHOT,
                "origem_ranking": f"chesscom_{nome_modalidade}"
            })

    df = pd.DataFrame(registros)
    return df


def salvar_staging(df):
    caminho_arquivo = f"{DATA_PROCESSED_PATH}/staging/staging_enxadristas_top.csv"

    if os.path.exists(caminho_arquivo):
        df_existente = pd.read_csv(caminho_arquivo)
        df_final = pd.concat([df_existente, df], ignore_index=True)
    else:
        df_final = df

    df_final.to_csv(caminho_arquivo, index=False)
    logger.info(f"Staging atualizada em: {caminho_arquivo}")

# =========================================================
# Execução principal
# =========================================================

def main():
    logger.info("===== INÍCIO DO SCRIPT LEADERBOARD =====")

    criar_diretorios()

    dados_leaderboard = coletar_leaderboard()
    salvar_json_bruto(dados_leaderboard)

    df_staging = gerar_staging_enxadristas_top(dados_leaderboard)
    salvar_staging(df_staging)

    logger.info("===== FIM DO SCRIPT LEADERBOARD =====")


if __name__ == "__main__":
    main()
