# Arquitetura do Projeto – Xadrez em Números

Este documento descreve a arquitetura de dados, decisões técnicas e modelagem dimensional utilizadas no projeto.

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
