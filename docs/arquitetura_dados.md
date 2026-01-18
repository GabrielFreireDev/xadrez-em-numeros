# Arquitetura do Projeto – Xadrez em Números

Este documento descreve a arquitetura de dados, decisões técnicas e modelagem dimensional utilizadas no projeto.

O projeto utiliza como critério de seleção de enxadristas a presença no Top 50 do ranking do Chess.com, garantindo foco analítico, controle de volume e relevância esportiva, com atualizaçãoes semanais, gerando snapshots históricos que permitem análise de evolução de ranking.

O projeto utiliza a biblioteca nativa logging do Python para controle e rastreamento do pipeline de dados, evitando dependências externas desnecessárias.

---

## 🧱 Visão Geral da Arquitetura

O projeto segue uma arquitetura clássica de BI:

```text
API Chess.com
     ↓
Extração (Python)
     ↓
Dados Brutos (JSON)
     ↓
Transformação / Limpeza
     ↓
Modelo Dimensional (Curated)
     ↓
Power BI
