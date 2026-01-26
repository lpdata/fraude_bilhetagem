# 🚍 Detecção de Fraudes em Sistemas de Bilhetagem Eletrônica

## 📌 Contexto e Objetivo

Sistemas de transporte público enfrentam perdas financeiras relevantes decorrentes de fraudes em transações de bilhetagem eletrônica. Além do impacto financeiro direto, a área de negócio destacou um problema operacional crítico: o cancelamento indevido de cartões legítimos, que afeta usuários regulares e gera insatisfação.

Neste contexto, este projeto tem como objetivo desenvolver e avaliar modelos preditivos capazes de identificar transações fraudulentas, utilizando dados históricos de bilhetagem, priorizando interpretabilidade, controle operacional e metodologia robusta, em conformidade com as premissas do case.

---

## 📂 Estrutura do Repositório

fraude_bilhetagem/  
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

---

## 📘 Dicionário de Dados (Features Originais)

O dataset original é composto por 30.000 transações e 25 atributos brutos, descrevendo informações do cartão, do usuário e do contexto da transação.

Exemplo de features originais:

| Feature | Descrição | Tipo |
|------|-----------|------|
| id_transacao | Identificador único da transação | Inteiro |
| id_cartao | Identificador do cartão | Inteiro |
| ts_transacao | Data e hora da transação | Datetime |
| idade_usuario | Idade do titular do cartão | Inteiro |
| valor_transacao | Valor debitado | Float |
| linha_onibus | Linha utilizada | Inteiro |
| id_dispositivo | Validador da transação | Inteiro |
| target_fraude | Indicador de fraude | Binário |

O dicionário completo encontra-se no arquivo **Dicionário de Dados.pdf**.

---

## 🛠 Engenharia de Features

A partir das variáveis originais, foi conduzida uma engenharia de features robusta, resultando em 38 novas variáveis, sem vazamento de informação, organizadas nos seguintes grupos:

| Grupo | Exemplo | Descrição |
|----|--------|----------|
| Temporais | hora_transacao | Hora da transação |
| Comportamentais | uso_intervalo_curto | Uso repetido em curto intervalo |
| Contextuais | feriado_bin | Indica feriado |
| Agregadas por cartão | cartao_valor_transacao_std | Variabilidade histórica |
| Relativas ao cartão | valor_zscore_cartao | Desvio em relação ao histórico |

Essas features buscaram capturar padrões de comportamento, intensidade de uso e consistência operacional.

---

## 🔎 Principais Insights Exploratórios

Durante a análise e criação das features, alguns padrões relevantes foram identificados:

- Fraudes tendem a ocorrer proporcionalmente mais em cartões com maior tempo de vida.
- Observou-se maior incidência de fraude em cartões associados a perfis etários mais elevados, sugerindo possível uso indevido de benefícios.
- Transações fraudulentas apresentam, em média, maior variabilidade de valor em relação ao histórico do próprio cartão.
- Mesmo após engenharia de features, não foi observada separação clara entre fraude e não fraude no espaço de variáveis.

---

## 🔍 Diagnóstico Exploratório da Separabilidade

Antes da modelagem, foi realizada uma análise diagnóstica utilizando PCA (Principal Component Analysis), técnica de redução de dimensionalidade, com o objetivo de avaliar a separabilidade geométrica entre as classes.

A projeção nos dois primeiros componentes principais explicou cerca de 30% da variância total, e o gráfico resultante evidenciou forte sobreposição entre transações fraudulentas e legítimas, indicando baixa separabilidade estrutural do problema.

---

## 🤖 Modelagem Preditiva

### Seleção de Modelos Candidatos

Foram considerados modelos amplamente utilizados em classificação, avaliando sua aderência ao problema de fraude, interpretabilidade e controle operacional:

| Modelo | Interpretabilidade | Robustez a ruído | Controle de falsos positivos | Adequação ao problema |
|------|------------------|------------------|-----------------------------|----------------------|
| Regressão Logística | Alta | Média | Alta (threshold ajustável) | Alta |
| Árvore de Decisão | Alta | Baixa | Média | Média |
| Random Forest | Média | Alta | Baixa | Média |
| Gradient Boosting | Baixa | Alta | Baixa | Não priorizado |
| Redes Neurais | Baixa | Alta | Baixa | Não priorizado |

---

### Avaliação e Comparação

Os modelos foram avaliados utilizando validação cruzada estratificada, conjunto holdout independente e métricas adequadas a dados desbalanceados, com foco em PR-AUC e análise de trade-off operacional.

O modelo escolhido como baseline final foi a Regressão Logística, por apresentar melhor desempenho relativo em PR-AUC, maior estabilidade, alta interpretabilidade e capacidade de ajuste fino de threshold, essencial para reduzir cancelamentos indevidos.

---

## 📊 Resultados Visuais Relevantes

Algumas visualizações foram fundamentais para compreensão do problema e dos resultados:

- Projeção PCA evidenciando sobreposição entre classes
- Matrizes de confusão comparativas dos três modelos
- Análise do trade-off operacional entre recuperação de fraudes e volume de alertas

As figuras correspondentes encontram-se documentadas no notebook de modelagem.

---

## 🧠 Conclusões

Os resultados indicam que o principal limitador do desempenho dos modelos não está na escolha do algoritmo, mas na natureza dos dados disponíveis. Mesmo com engenharia de features robusta, o problema apresenta baixa separabilidade, o que restringe o desempenho de modelos supervisionados tradicionais.

Nesse contexto, a modelagem atua de forma mais adequada como ferramenta de priorização de risco, e não como mecanismo automático de decisão.

---

## 🚀 Recomendações e Próximos Passos

Para evoluir a solução em um ambiente real, recomenda-se:

- Enriquecimento do dataset com informações geográficas e sequenciais
- Modelagem explícita de sequências temporais por cartão
- Abordagem de ranqueamento de risco ao invés de classificação rígida
- Ajuste dinâmico de thresholds conforme perfil do cartão
- Integração do modelo a processos de revisão humana
- Exploração de métodos não supervisionados para detecção de anomalias

---

## 📌 Considerações Finais

Este projeto entregou um pipeline completo, interpretável e metodologicamente sólido para detecção de fraude em bilhetagem eletrônica, além de diagnosticar com transparência os limites do problema. A principal contribuição reside na compreensão clara do espaço de dados, dos trade-offs envolvidos e dos caminhos mais promissores para evolução da solução em um cenário real.
