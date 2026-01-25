# 🚍 Detecção de Fraudes em Sistemas de Bilhetagem Eletrônica

## 📌 Visão Geral

Este projeto apresenta o desenvolvimento **end-to-end** de um modelo preditivo para **detecção de fraudes em sistemas de bilhetagem eletrônica**, com foco na **redução de perdas financeiras** e na **minimização de falsos positivos**, especialmente bloqueios indevidos de cartões legítimos.

O trabalho contempla todas as etapas clássicas de um pipeline profissional de Machine Learning, desde a **análise exploratória**, passando por **tratamento de dados e engenharia de features**, até a **modelagem e comparação de múltiplos modelos**, priorizando **interpretabilidade e rigor metodológico**.

---

## 🎯 Objetivo do Projeto

A missão é **desenvolver um modelo capaz de identificar e prever ocorrências de fraude** a partir de dados transacionais de bilhetagem, respeitando os seguintes princípios:

- Utilização de **Python 3.12.12**
- Competição de performance entre **no mínimo 3 modelos distintos**
- **Prioridade para modelos interpretáveis**
- Clareza na escolha de métricas e critérios de avaliação
- Organização, rastreabilidade e reprodutibilidade do pipeline

---

## 🧠 Abordagem Metodológica

O projeto foi estruturado de forma incremental e auditável, seguindo boas práticas de **Data Science aplicada e MLOps**:

1. **Análise Exploratória**
   - Entendimento do domínio
   - Análise de distribuição, outliers e padrões iniciais
   - Avaliação preliminar do comportamento de fraude

2. **Tratamento de Dados**
   - Limpeza
   - Padronização de tipos
   - Preparação de variáveis temporais e categóricas

3. **Engenharia de Features**
   - Criação de **features temporais, comportamentais e contextuais**
   - Agregações por cartão
   - Indicadores de intensidade, repetição e consistência operacional
   - Auditoria de vazamento de informação
   - Consolidação de **38 features finais**

4. **Preparação do Dataset Final**
   - Separação clara entre colunas de rastreio, target e features
   - Validação de tipos, cardinalidade e valores ausentes
   - Exportação versionada dos dados processados

5. **Modelagem (em andamento)**
   - Construção e comparação de múltiplos modelos
   - Priorização de interpretabilidade
   - Avaliação criteriosa de métricas adequadas ao problema de fraude

---

## 🗂 Estrutura do Repositório

## 🗂 Estrutura do Repositório

```
fraude_bilhetagem/
│
├── data/
│   ├── raw/                     # Dados brutos (originais)
│   └── processed/               # Dados tratados e prontos para modelagem
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
│   ├── features.py              # Funções reutilizáveis de engenharia de features
│   ├── preprocessing.py         # Rotinas de pré-processamento
│   ├── models.py                # Treinamento e comparação de modelos
│   └── metrics.py               # Métricas e avaliação
│
├── outputs/                     # Resultados, gráficos e artefatos gerados
│
├── README.md                    # Documentação principal do projeto
└── requirements.txt             # Dependências do projeto
```

> 🔎 **Observação:**  
> O desenvolvimento inicial foi realizado em notebooks para facilitar análise, auditoria e comunicação.  
> A migração para `src/` será feita após validação completa da modelagem, seguindo boas práticas de MLOps.

---

## 📊 Dataset Processado

O dataset final contém:

- **30.000 transações**
- **38 features finais**
- Separação clara entre:
  - Colunas de rastreio
  - Variável alvo (`target_fraude`)
  - Features utilizáveis em modelos

Todos os artefatos de dados foram **versionados**, incluindo:
- schema de colunas
- metadados de tipos
- estatísticas globais do dataset

---

## 📈 Métricas e Avaliação

A avaliação dos modelos considera:
- Natureza desbalanceada do problema
- Custo assimétrico entre falso positivo e falso negativo
- Necessidade de **interpretação clara** para uso operacional

As métricas e critérios finais serão detalhados na etapa de modelagem.

---

## 🧩 Tecnologias Utilizadas

- Python 3.x
- Pandas / NumPy
- Scikit-learn
- Jupyter Notebook
- Git / GitHub

---

## 🚀 Status do Projeto

- ✔ Análise exploratória
- ✔ Tratamento de dados
- ✔ Engenharia de features
- ✔ Preparação e exportação do dataset final
- 🚧 Modelagem e comparação de modelos (em andamento)

---

## ✍️ Autoria

Projeto desenvolvido por **lpdata**, como estudo aplicado de **Machine Learning para detecção de fraudes**, com foco em rigor técnico, clareza metodológica e boas práticas de engenharia.

---

