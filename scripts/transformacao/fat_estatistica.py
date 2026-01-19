import os
import json
import time
import logging
from datetime import datetime, timezone
from typing import Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

# =========================================================
# Configurações iniciais
# =========================================================

load_dotenv()

DATA_ANALYTICS_PATH = os.getenv("DATA_ANALYTICS_PATH")


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

API_BASE_URL = "https://api.chess.com/pub/player"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ChesscomBI/1.0; +https://github.com/gabrielfreiredev/xadrez-em-numeros)"
}

MODALIDADES = {
    "chess_rapid": "rapid",
    "chess_blitz": "blitz",
    "chess_bullet": "bullet"
}

# =========================================================
# Funções auxiliares
# =========================================================

def carregar_dim_enxadrista() -> pd.DataFrame:
    caminho = os.path.join(DATA_ANALYTICS_PATH, "dim_enxadrista.csv")
    return pd.read_csv(caminho)


def obter_estatisticas(username: str) -> Dict:
    url = f"{API_BASE_URL}/{username}/stats"
    response = requests.get(url, timeout=30, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def processar_modalidade(
    bloco: Dict,
    modalidade: str,
    player_id: int,
    data_ref: datetime.date
) -> Dict | None:
    if "last" not in bloco or "record" not in bloco:
        return None

    best = bloco.get("best")

    return {
        "player_id": player_id,
        "modalidade": modalidade,
        "data_referencia": data_ref,
        "rating_atual": bloco["last"].get("rating"),
        "rating_melhor": best.get("rating") if best else None,
        "data_rating_melhor": (
            datetime.fromtimestamp(best["date"]).date()
            if best and best.get("date")
            else None
        ),
        "vitorias": bloco["record"].get("win"),
        "derrotas": bloco["record"].get("loss"),
        "empates": bloco["record"].get("draw")
    }


# =========================================================
# Função principal
# =========================================================

def main():
    logging.info("Iniciando coleta da fato_estatistica")

    dim_enxadrista = carregar_dim_enxadrista()
    data_referencia = datetime.now(timezone.utc).date()

    registros: List[Dict] = []

    for _, row in dim_enxadrista.iterrows():
        username = row["username"]
        player_id = row["player_id"]

        logging.info(f"Coletando estatísticas de {username}")

        try:
            stats = obter_estatisticas(username)

            for chave_api, nome_modalidade in MODALIDADES.items():
                bloco = stats.get(chave_api)

                if not bloco:
                    continue

                registro = processar_modalidade(
                    bloco=bloco,
                    modalidade=nome_modalidade,
                    player_id=player_id,
                    data_ref=data_referencia
                )

                if registro:
                    registros.append(registro)

            time.sleep(1)  # respeitar rate limit

        except Exception as e:
            logging.error(f"Erro ao processar {username}: {e}")

    if not registros:
        logging.warning("Nenhum registro gerado.")
        return

    df = pd.DataFrame(registros)

    caminho_saida = os.path.join(DATA_ANALYTICS_PATH, "fat_estatistica.csv")
    df.to_csv(caminho_saida, index=False, encoding="utf-8")

    logging.info(f"fat_estatistica gerada com sucesso em: {caminho_saida}")


# =========================================================
# Execução
# =========================================================

if __name__ == "__main__":
    main()
