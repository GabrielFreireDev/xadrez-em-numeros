import os
import json
import logging
import time
from datetime import datetime, timezone

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

USERNAME = "lpsupi"
MESES = [
    ('2025', '06'),
    ('2025', '07'),
    ('2025', '08'),
    ('2025', '09'),
    ('2025', '10'),
    ('2025', '11'),
    ('2025', '12'),
]

URL_GAMES = "https://api.chess.com/pub/player/{}/games/{}/{}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ChesscomBI/1.0; +https://github.com/gabrielfreiredev/xadrez-em-numeros)"
}

TRADUCAO_RESULTADO = {
    "abandoned": "abandonado",
    "agreed": "empate por acordo",
    "checkmated": "xeque-mate",
    "insufficient": "material insuficiente",
    "repetition": "tripla repetição",
    "resigned": "desistência",
    "stalemate": "rei afogado",
    "timeout": "tempo esgotado",
    "timevsinsufficient": "tempo vs. material insuficiente",
    "win": "vitória"
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
# Funções auxiliares
# =========================================================

def unix_para_data(unix_time):
    if not unix_time:
        return None
    return datetime.fromtimestamp(unix_time, tz=timezone.utc).date()


def extrair_eco_sufixo(eco_url):
    if not eco_url:
        return None
    return eco_url.rstrip("/").split("/")[-1]


def traduzir_resultado(resultado):
    if not resultado:
        return None
    return TRADUCAO_RESULTADO.get(resultado, resultado)


def criar_diretorios():
    os.makedirs(f"{DATA_RAW_PATH}/chesscom/partidas", exist_ok=True)
    os.makedirs(f"{DATA_PROCESSED_PATH}/staging", exist_ok=True)

# =========================================================
# Execução principal
# =========================================================

def main():
    logger.info("===== INÍCIO STAGING_PARTIDAS_MENSAIS =====")

    criar_diretorios()
    registros = []

    for ano, mes in MESES:
        logger.info(f"Coletando partidas {USERNAME} - {ano}/{mes}")
        url = URL_GAMES.format(USERNAME, ano, mes)

        response = requests.get(url, headers=HEADERS, timeout=15)

        if response.status_code != 200:
            logger.warning(f"Erro na API: {url}")
            continue

        dados = response.json()

        # salva json bruto
        with open(
            f"{DATA_RAW_PATH}/chesscom/partidas/{USERNAME}_{ano}_{mes}.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

        games = dados.get("games", [])

        for game in games:
            data_partida = unix_para_data(game.get("end_time"))
            eco_raw = extrair_eco_sufixo(game.get("eco"))

            # Registro BRANCAS
            white = game.get("white", {})
            registros.append({
                "partida_url": game.get("url"),
                "data": data_partida,
                "rated": game.get("rated"),
                "modalidade": game.get("time_class"),
                "regras": game.get("rules"),
                "cor": "branca",
                "resultado": traduzir_resultado(white.get("result")),
                "rating": white.get("rating"),
                "precisao": game.get("accuracies", {}).get("white"),
                "username": white.get("username", "").lower(),
                "player_api_id": white.get("@id"),
                "eco_abertura_raw": eco_raw,
                "origem": "chess.com"
            })

            # Registro PRETAS
            black = game.get("black", {})
            registros.append({
                "partida_url": game.get("url"),
                "data": data_partida,
                "rated": game.get("rated"),
                "modalidade": game.get("time_class"),
                "regras": game.get("rules"),
                "cor": "preta",
                "resultado": traduzir_resultado(black.get("result")),
                "rating": black.get("rating"),
                "precisao": game.get("accuracies", {}).get("black"),
                "username": black.get("username", "").lower(),
                "player_api_id": black.get("@id"),
                "eco_abertura_raw": eco_raw,
                "origem": "chess.com"
            })

        time.sleep(1)

    df = pd.DataFrame(registros)

    caminho_saida = f"{DATA_PROCESSED_PATH}/staging/staging_partidas_mensais.csv"
    df.to_csv(caminho_saida, index=False, encoding="utf-8")

    logger.info(f"Arquivo gerado: {caminho_saida}")
    logger.info("===== FIM STAGING_PARTIDAS_MENSAIS =====")

if __name__ == "__main__":
    main()
