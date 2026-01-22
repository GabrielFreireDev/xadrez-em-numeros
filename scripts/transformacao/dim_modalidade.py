import os
import logging
import pandas as pd
from dotenv import load_dotenv

# =========================================================
# Configurações
# =========================================================

load_dotenv()

DATA_ANALYTICS_PATH = os.getenv("DATA_ANALYTICS_PATH")


# =========================================================
# Logging
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# =========================================================
# Execução principal
# =========================================================

def main():
    logger.info("===== INÍCIO DIM_MODALIDADE =====")

    os.makedirs(DATA_ANALYTICS_PATH, exist_ok=True)

    dados = [
        {
            "modalidade_id": 1,
            "modalidade": "blitz",
            "modalidade_nome": "Blitz",
            "origem": "chess.com"
        },
        {
            "modalidade_id": 2,
            "modalidade": "rapid",
            "modalidade_nome": "Rápidas",
            "origem": "chess.com"
        },
        {
            "modalidade_id": 3,
            "modalidade": "bullet",
            "modalidade_nome": "Bullet",
            "origem": "chess.com"
        }
    ]

    df = pd.DataFrame(dados)

    caminho_arquivo = f"{DATA_ANALYTICS_PATH}/dim_modalidade.csv"
    df.to_csv(caminho_arquivo, index=False, encoding="utf-8")

    logger.info(f"Arquivo gerado: {caminho_arquivo}")
    logger.info("===== FIM DIM_MODALIDADE =====")


if __name__ == "__main__":
    main()
