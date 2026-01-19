# Arquitetura do Projeto – Xadrez em Números

Este documento descreve a arquitetura de dados, decisões técnicas e modelagem dimensional utilizadas no projeto.

O projeto utiliza como critério de seleção de enxadristas a presença no Top 50 do ranking do Chess.com, garantindo foco analítico, controle de volume e relevância esportiva, com atualizaçãoes semanais, gerando snapshots históricos que permitem análise de evolução de ranking.

Uma informação importante como o rating FIDE do enxadrista seria considerada também, mas não foi incluído por falta de integração oficial via API e alto custo de governança visto que os arquivos disponibilizados pela FIDE e a API do Chess.com não possuem valores em comum para uma identificação precisa. O projeto foca exclusivamente no ecossistema Chess.com para garantir consistência e reprodutibilidade

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
