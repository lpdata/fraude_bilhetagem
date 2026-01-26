# 🚍 Detecção de Fraudes em Sistemas de Bilhetagem Eletrônica

## 📌 Contexto e Objetivo

Sistemas de transporte público enfrentam perdas financeiras relevantes decorrentes de fraudes em transações de bilhetagem eletrônica. Além do impacto financeiro direto, a área de negócio destacou um problema operacional crítico: **o cancelamento indevido de cartões legítimos**, que afeta usuários regulares e gera insatisfação.

Neste contexto, este projeto tem como objetivo **desenvolver e avaliar modelos preditivos capazes de identificar transações fraudulentas**, utilizando dados históricos de bilhetagem, priorizando **interpretabilidade, controle operacional e metodologia robusta**, em conformidade com as premissas do case.

---

## 📂 Estrutura do Repositório

```text
fraude_bilhetagem/
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── dados_tratados.csv
│       ├── schema_dados_tratados.json
│       ├── metadados_colunas.csv
│       └── metadados_dataset.json
│
├── notebooks/
│   ├── 01_exploracao_dados.ipynb
│   ├── 02_tratamento_features.ipynb
│   └── 03_modelagem.ipynb
│
├── src/
│   ├── features.py
│   ├── preprocessing.py
│   ├── models.py
│   └── metrics.py
│
├── README.md
└── requirements.txt
