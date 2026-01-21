import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações
DATA_PROCESSED_PATH = os.getenv("DATA_PROCESSED_PATH")
# Caminhos
CAMINHO_DIM_PAIS = f"{DATA_PROCESSED_PATH}/dimensoes_auxiliares/dim_pais.csv"


# Leitura
df = pd.read_csv(CAMINHO_DIM_PAIS)

# Mapeamento padrão PT-BR (uso comum / IBGE)
traducao_paises = {
    "Brazil": "Brasil",
    "United States": "Estados Unidos",
    "United Kingdom": "Reino Unido",
    "Germany": "Alemanha",
    "France": "França",
    "Spain": "Espanha",
    "Italy": "Itália",
    "Netherlands": "Países Baixos",
    "Russian Federation": "Rússia",
    "Ukraine": "Ucrânia",
    "Poland": "Polônia",
    "Sweden": "Suécia",
    "Norway": "Noruega",
    "Finland": "Finlândia",
    "Denmark": "Dinamarca",
    "Switzerland": "Suíça",
    "Austria": "Áustria",
    "Portugal": "Portugal",
    "Belgium": "Bélgica",
    "Ireland": "Irlanda",
    "Czech Republic": "República Tcheca",
    "Slovakia": "Eslováquia",
    "Hungary": "Hungria",
    "Romania": "Romênia",
    "Bulgaria": "Bulgária",
    "Greece": "Grécia",
    "Serbia": "Sérvia",
    "Croatia": "Croácia",
    "Bosnia and Herzegovina": "Bósnia e Herzegovina",
    "Montenegro": "Montenegro",
    "Albania": "Albânia",
    "Latvia": "Letônia",
    "Lithuania": "Lituânia",
    "Estonia": "Estônia",
    "Iceland": "Islândia",
    "Canada": "Canadá",
    "Mexico": "México",
    "Argentina": "Argentina",
    "Chile": "Chile",
    "Colombia": "Colômbia",
    "Peru": "Peru",
    "Uruguay": "Uruguai",
    "Paraguay": "Paraguai",
    "Bolivia": "Bolívia",
    "Ecuador": "Equador",
    "Venezuela": "Venezuela",
    "China": "China",
    "Japan": "Japão",
    "South Korea": "Coreia do Sul",
    "North Korea": "Coreia do Norte",
    "India": "Índia",
    "Indonesia": "Indonésia",
    "Philippines": "Filipinas",
    "Thailand": "Tailândia",
    "Vietnam": "Vietnã",
    "Malaysia": "Malásia",
    "Singapore": "Singapura",
    "Australia": "Austrália",
    "New Zealand": "Nova Zelândia",
    "South Africa": "África do Sul",
    "Egypt": "Egito",
    "Morocco": "Marrocos",
    "Tunisia": "Tunísia",
    "Algeria": "Argélia",
    "Nigeria": "Nigéria",
    "Ghana": "Gana",
    "Kenya": "Quênia",
    "Senegal": "Senegal",
    "Turkey": "Turquia",
}

# Tradução (fallback mantém o original)
df["nome_pais"] = df["nome_pais"].apply(
    lambda x: traducao_paises.get(x, x)
)

# Exportação
caminho_saida = f"{DATA_PROCESSED_PATH}/dimensoes_auxiliares/dim_pais_ptbr.csv"
df.to_csv(caminho_saida, index=False, encoding="utf-8")

print(f"Arquivo gerado: {caminho_saida}")