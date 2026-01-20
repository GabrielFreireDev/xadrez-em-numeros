import os
import json
from datetime import datetime, timezone
import logging
import time

import requests
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

# =========================================================
# Configurações
# =========================================================

load_dotenv()

DATA_RAW_PATH = os.getenv("DATA_RAW_PATH")
DATA_PROCESSED_PATH = os.getenv("DATA_PROCESSED_PATH")

URL_PERFIL = "https://api.chess.com/pub/player/{}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ChesscomBI/1.0; +https://github.com/gabrielfreiredev/xadrez-em-numeros)"
}

# =========================================================
# Logging
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# =========================================================
# Funções
# =========================================================

def carregar_enxadristas():
    caminho = f"{DATA_PROCESSED_PATH}/staging/staging_enxadristas_top.csv"
    return pd.read_csv(caminho)["username"].drop_duplicates().tolist()


def criar_diretorios():
    os.makedirs(f"{DATA_RAW_PATH}/chesscom/perfis", exist_ok=True)
    os.makedirs(f"{DATA_PROCESSED_PATH}/staging", exist_ok=True)


def coletar_perfil(username):
    url = URL_PERFIL.format(username)
    resposta = requests.get(url, headers=HEADERS, timeout=10)

    if resposta.status_code == 200:
        return resposta.json()

    logger.warning(f"Perfil não encontrado: {username}")
    return None


def main():
    logger.info("===== INÍCIO EXTRAÇÃO PERFIS CHESS.COM =====")

    criar_diretorios()
    usernames = carregar_enxadristas()

    registros = []

    for username in tqdm(usernames, desc="Perfis Chess.com"):
        dados = coletar_perfil(username)

        if dados:
            # -------------------------------------------------
            # Salva JSON bruto
            # -------------------------------------------------
            with open(
                f"{DATA_RAW_PATH}/chesscom/perfis/{username}.json",
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)

        
            registros.append({
                "player_id": dados.get("player_id"),
                "username": dados.get("username"),
                "nome": dados.get("name"),
                "titulo": dados.get("title"),
                "avatar": dados.get("avatar"),
                "url": dados.get("url"),
                "seguidores": dados.get("followers"),
                "pais": dados.get("country").split("/")[-1] if dados.get("country") else None,
                "data_entrada": (
                    datetime.fromtimestamp(dados["joined"], tz=timezone.utc)
                    .strftime("%Y-%m-%d")
                    if dados.get("joined")
                    else None
                ),
                "status": dados.get("status"),
                "is_streamer": dados.get("is_streamer"),
                "verificado": dados.get("verified"),
                "origem": "chess.com"
            })

        time.sleep(0.5)  # respeitando a API

    df = pd.DataFrame(registros)
    df.to_csv(
        f"{DATA_PROCESSED_PATH}/staging/staging_perfil_chesscom.csv",
        index=False
    )

    logger.info("Perfis Chess.com extraídos com sucesso")
    logger.info("===== FIM EXTRAÇÃO PERFIS CHESS.COM =====")


if __name__ == "__main__":
    main()
