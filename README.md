# 🚍 Detecção de Fraudes em Sistemas de Bilhetagem Eletrônica


## 📌 Contexto e Objetivo

Sistemas de transporte utilizam amplamente a bilhetagem eletrônica como meio de controle de acesso e arrecadação tarifária. Nesse contexto, fraudes em transações representam um problema recorrente, com impactos financeiros e operacionais relevantes para o sistema.

Foi disponibilizado um conjunto de dados contendo **30.000 registros históricos de transações de bilhetagem**, com atributos relacionados ao cartão, ao usuário e às circunstâncias da transação. O objetivo central do projeto é **explorar esse conjunto de dados e desenvolver modelos preditivos capazes de identificar ocorrências de fraude**, seguindo boas práticas de Ciência de Dados e Aprendizado de Máquina.

### Desafios do Problema

Ainda que os desafios específicos sejam analisados ao longo do projeto, o problema apresenta, de forma geral, características que tornam a tarefa de detecção de fraude não trivial, tais como:

- Diferença de frequência entre transações legítimas e fraudulentas.
- Impacto operacional associado a decisões automatizadas incorretas.
- Necessidade de compreensão e explicação das decisões do modelo.
- Dependência exclusiva de dados históricos internos ao sistema.

Diante disso, o projeto foi estruturado em etapas bem definidas: análise exploratória, tratamento de dados, engenharia de features e modelagem, com o objetivo de avaliar de forma transparente e criteriosa as possibilidades e limitações dos modelos construídos.


## 📂 Estrutura do Repositório

- **data/**
  - **raw/**
    - `dados.csv`
    - `Dicionário de Dados.pdf`
  - **processed/**
    - `dados_tratados.csv`
    - `schema_dados_tratados.json`
    - `metadados_colunas.csv`
    - `metadados_dataset.json`

- **notebooks/**
  - `01_exploracao_dados.ipynb`
  - `02_tratamento_features.ipynb`
  - `03_modelagem.ipynb`

- **outputs/**
  - `matrizes_confusao_modelos.png`

- **src/**
  - `features.py`
  - `preprocessing.py`
  - `models.py`
  - `metrics.py`

- `README.md`
- `requirements.txt`


## 📘 Dicionário de Dados (Features Originais)

O conjunto de dados original é composto por 30.000 registros de transações de bilhetagem eletrônica e diversas variáveis operacionais e cadastrais. Abaixo são apresentadas algumas das colunas mais relevantes:

| Coluna | Descrição | Tipo |
|------|-----------|------|
| id_transacao | Identificador único da transação. | Int |
| id_cartao | Identificador único do cartão (usuário). | Int |
| ts_transacao | Timestamp (data e hora) do uso na catraca. | Datetime |
| valor_transacao | Valor debitado no momento do giro da catraca. | Float |
| target_fraude | Variável Alvo: 1 para Fraude Confirmada, 0 para Normal. | Binary |

O dicionário completo, contendo todas as variáveis originais do dataset, encontra-se no arquivo **Dicionário de Dados.pdf**, disponível na pasta `data/raw/`.

## 🔍 Análise Exploratória dos Dados

A análise exploratória foi conduzida ao longo das etapas iniciais do projeto, com o objetivo de compreender a estrutura do dataset, a natureza do problema de fraude e os principais padrões associados ao uso dos cartões. Essa etapa orientou tanto a engenharia de features quanto as decisões posteriores de modelagem.

### Estrutura e Qualidade dos Dados

O conjunto de dados apresenta volume adequado e estrutura consistente para fins de modelagem preditiva. As variáveis temporais, categóricas e numéricas encontram-se bem definidas, permitindo análises sob diferentes perspectivas comportamentais e contextuais. Não foram identificados problemas críticos de integridade que inviabilizassem o uso dos dados, embora algumas variáveis demandassem tratamento e padronização em etapas posteriores.

### Variável Alvo e Desbalanceamento

A variável alvo `target_fraude` apresenta desbalanceamento, com predominância de transações normais em relação às fraudulentas. Esse cenário reforça a necessidade de cuidado na escolha das métricas de avaliação e na interpretação dos resultados, especialmente considerando o impacto operacional de falsos positivos sinalizado pela área de negócio.

### Padrões Temporais e Contextuais

As análises temporais, como hora do dia, dia da semana e tempo de vida do cartão, indicaram variações discretas na taxa de fraude, sem padrões determinísticos claros quando observadas de forma isolada. Variáveis de contexto operacional, como integração tarifária e limites de uso, também apresentaram baixo poder discriminante individual, sugerindo atuação apenas como sinais auxiliares quando combinadas a outros atributos.

### Perfil do Usuário e Características da Transação

Variáveis demográficas e cadastrais não demonstraram diferenças relevantes entre transações normais e fraudulentas. Da mesma forma, o valor da transação, analisado isoladamente, apresentou forte sobreposição entre os grupos, indicando que não constitui um indicador direto de fraude neste contexto. Por outro lado, o tipo de cartão apresentou diferenças mais expressivas na taxa de fraude, sugerindo influência do perfil do benefício no risco associado.

### Comportamento de Uso dos Cartões

A análise comportamental evidenciou que métricas simples de frequência ou intervalo entre transações não são suficientes, isoladamente, para diferenciar cartões com e sem fraude. Em contrapartida, atributos relacionados à diversidade e dispersão de uso mostraram associação mais consistente com a ocorrência de fraude, como a utilização de múltiplas linhas e dispositivos distintos, indicando padrões operacionais menos previsíveis.

### Direcionamento para as Etapas Seguintes

De forma geral, os resultados exploratórios indicam que a fraude não se manifesta por meio de regras simples ou limiares fixos, mas sim por combinações de padrões comportamentais. Esses achados fundamentaram a etapa de engenharia de features e reforçaram a necessidade de modelos interpretáveis, avaliados com métricas alinhadas ao impacto operacional do problema.


## 🧠 Engenharia de Features

A etapa de engenharia de features teve como objetivo transformar a base transacional bruta em um dataset analiticamente consistente, rastreável e adequado à modelagem preditiva. O foco não foi apenas aumentar o número de variáveis, mas **representar padrões comportamentais e temporais relevantes ao problema de fraude**, mantendo clareza e controle sobre cada transformação aplicada.

### Visão Geral do Dataset Final

| Elemento | Descrição |
|-------|----------|
| Registros | 30.000 transações |
| Total de colunas | 42 |
| Colunas de rastreio | Garantem auditabilidade e depuração |
| Variável alvo | Isolada e protegida contra vazamentos |
| Features derivadas | 38 variáveis construídas de forma incremental |

A relação completa das features criadas, com tipos e descrições detalhadas, está documentada nos arquivos de metadados disponíveis em `data/processed/`.

### Eixos Principais da Engenharia de Features

Em vez de depender de atributos isolados, a engenharia de features foi organizada em **quatro eixos conceituais**, descritos a seguir.

#### ⏱️ Enriquecimento temporal e sequencial

Foram criadas variáveis voltadas à dinâmica de uso do cartão ao longo do tempo, permitindo capturar padrões que não emergem em análises pontuais.

Principais ideias exploradas:
- Intervalo desde a última transação
- Frequência de uso em janelas móveis
- Identificação de uso em intervalos curtos
- Flags de uso intenso em períodos reduzidos

Essas features permitem identificar comportamentos acelerados ou fora do padrão esperado.

#### 🧭 Comportamento diário e consistência operacional

Esse eixo buscou representar **estabilidade versus ruptura de padrão** no uso cotidiano do cartão.

Foram consideradas, por exemplo:
- Quantidade de linhas distintas utilizadas no dia
- Quantidade de dispositivos distintos por dia
- Repetição de linha ou dispositivo em transações consecutivas

Esses sinais ajudam a diferenciar comportamentos recorrentes legítimos de sequências operacionais atípicas.

#### 🧾 Consolidação do histórico do cartão

Agregações por cartão permitiram construir uma visão de longo prazo do comportamento individual, funcionando como uma referência histórica para cada usuário.

Entre as informações consolidadas estão:
- Volume total de transações
- Dias ativos do cartão
- Média de transações por dia
- Diversidade de linhas, dispositivos e motoristas
- Estatísticas de valor transacionado

Esse histórico fornece contexto para interpretar cada nova transação.

#### 📊 Comparações relativas ao comportamento individual

Além de valores absolutos, foram criadas variáveis que **comparam cada transação com o próprio histórico do cartão**, permitindo capturar desvios sutis.

Exemplos de abordagens adotadas:
- Razão entre valor da transação e média do cartão
- Z-score individual do valor transacionado
- Identificação de outliers comportamentais
- Uso acima da média diária do cartão

Esse tipo de feature tende a ser especialmente informativo em cenários reais de fraude, onde desvios graduais podem ser mais relevantes do que picos isolados.

### Resultado da Etapa

Ao final do processo, o dataset encontra-se organizado, documentado e pronto para suportar a comparação entre diferentes modelos de machine learning, permitindo análises consistentes de desempenho, interpretabilidade e impacto operacional.

### Exemplos de Features Criadas

A tabela abaixo apresenta algumas das principais features derivadas durante o processo:

| Feature | Descrição |
|------|-----------|
| tempo_desde_ultima_transacao_min | Intervalo de tempo, em minutos, desde a última transação do cartão |
| qtd_linhas_distintas_dia | Quantidade de linhas de ônibus distintas utilizadas pelo cartão no dia |
| cartao_media_transacoes_por_dia | Média histórica de transações diárias do cartão |
| valor_zscore_cartao | Z-score do valor da transação em relação ao histórico do cartão |
| uso_acima_media_dia_cartao | Flag indicando uso diário acima da média histórica do cartão |

### Avaliação de Prontidão para Modelagem

Ao final da Etapa, o dataset encontra-se:

- Sem vazamentos de informação em relação à variável alvo  
- Com tipagem adequada e categóricas preparadas para encoding  
- Com auditoria explícita de valores ausentes, restritos a casos semanticamente esperados  
- Totalmente versionado, documentado e exportado para reutilização  

Essa estruturação permitiu que a etapa seguinte do projeto fosse dedicada exclusivamente à construção, comparação e avaliação de modelos de machine learning, sem necessidade de retrabalho nas fases anteriores.


## 🤖 Modelagem e Avaliação dos Modelos

Com o dataset tratado e enriquecido por meio da engenharia de features, iniciou-se a etapa de modelagem supervisionada com o objetivo de avaliar diferentes algoritmos de Machine Learning aplicados à detecção de fraudes em transações de bilhetagem eletrônica.

Essa etapa foi conduzida seguindo boas práticas metodológicas, incluindo validação cruzada estratificada, uso de métricas adequadas a dados desbalanceados e avaliação final em conjunto de teste independente. Além do desempenho preditivo, foram considerados critérios de interpretabilidade, estabilidade e impacto operacional, conforme as premissas do problema de negócio.

### Seleção e Justificativa dos Modelos Avaliados

| Modelo | Prós | Contras | Adequação |
|------|------|--------|----------|
| Regressão Logística | Alta interpretabilidade<br>Coeficientes explicáveis<br>Baseline robusto | Relações lineares<br>Depende de boas features | Muito alta<br>Baseline interpretável |
| Árvore de Decisão | Regras claras<br>Alta explicabilidade<br>Captura não linearidades | Sensível a ruído<br>Overfitting sem controle | Alta<br>Boa para explicação |
| Random Forest | Boa performance<br>Reduz overfitting<br>Interações complexas | Menor transparência<br>Custo computacional maior | Alta<br>Equilíbrio geral |
| Gradient Boosting | Forte poder preditivo<br>Bom em fraude | Complexidade elevada<br>Difícil explicação | Média |
| XGBoost / LightGBM | Performance de ponta<br>Robusto | Caixa-preta relativa<br>Difícil uso operacional | Média / Baixa |
| SVM | Bom em certos cenários | Pouco interpretável<br>Escala limitada | Baixa |
| kNN | Simples conceitualmente | Não escala bem<br>Difícil interpretação | Baixa |
| Naive Bayes | Rápido<br>Simples | Suposição forte<br>Baixa performance | Baixa |

A partir da análise comparativa, foram selecionados três modelos para avaliação prática no projeto: **Regressão Logística**, **Árvore de Decisão** e **Random Forest**.

A Regressão Logística foi adotada como baseline interpretável, permitindo leitura direta dos coeficientes e maior transparência na tomada de decisão. A Árvore de Decisão foi incluída por sua capacidade de capturar não linearidades de forma explicável, enquanto o Random Forest foi utilizado como um ensemble capaz de reduzir variância e explorar interações mais complexas entre as features.

Modelos de maior complexidade, como Gradient Boosting e XGBoost, foram deliberadamente mantidos fora do escopo principal devido à menor interpretabilidade e à dificuldade de uso operacional, considerando as restrições do problema e os requisitos do case.


### Comparação Visual dos Modelos

A figura abaixo apresenta as matrizes de confusão dos três modelos avaliados no conjunto de teste (holdout), considerando threshold padrão de 0.5. A visualização permite comparar diretamente o volume de falsos alertas, fraudes detectadas e fraudes perdidas em cada abordagem.

![Matrizes de Confusão dos Modelos](outputs/matrizes_confusao_modelos.png)

Os resultados obtidos indicaram desempenho limitado para todos os modelos avaliados, com métricas próximas ao comportamento aleatório. A análise de diagnóstico exploratório da separabilidade já havia evidenciado forte sobreposição entre transações fraudulentas e legítimas no espaço de features, o que se confirmou durante a modelagem.

A Regressão Logística apresentou o melhor desempenho relativo em termos de PR-AUC, estabilidade e interpretabilidade, sendo definida como o modelo vencedor do projeto. Ainda assim, os resultados reforçam que o principal limitador do desempenho não está na escolha do algoritmo, mas na natureza dos dados disponíveis.

Nesse contexto, os modelos supervisionados atuam de forma mais adequada como ferramentas de **priorização de risco**, e não como soluções definitivas de detecção automática de fraude.


## 📊 Resultados Visuais Relevantes

Durante o projeto, algumas visualizações desempenharam papel central na compreensão do problema e na interpretação dos resultados obtidos. Em especial:

- A projeção por PCA permitiu avaliar visualmente a separabilidade entre transações fraudulentas e legítimas.
- As matrizes de confusão possibilitaram a comparação direta do comportamento dos modelos no conjunto de teste.
- A análise do trade-off operacional evidenciou o impacto prático das decisões do modelo em termos de alertas e fraudes capturadas.

Essas visualizações complementam a análise quantitativa e estão documentadas no notebook de modelagem, servindo como apoio à interpretação dos resultados.


## 🧠 Conclusões

A avaliação dos modelos confirmou que a limitação central do problema não está associada à escolha do algoritmo, mas sim às características do espaço de dados disponível. Mesmo após a construção de features temporais, comportamentais e agregadas, observou-se baixa separabilidade entre as classes.

Nesse contexto, os modelos supervisionados avaliados apresentam maior adequação como mecanismos de **priorização de risco**, auxiliando a tomada de decisão, do que como soluções automáticas de detecção definitiva de fraude.


## 🚀 Recomendações e Próximos Passos

Considerando um cenário real de aplicação, alguns caminhos podem ser explorados para evolução da solução:

- Enriquecimento do dataset com informações adicionais de contexto e localização.
- Modelagem explícita de sequências temporais por cartão, capturando padrões de longo prazo.
- Reformulação do problema como ranqueamento de risco em vez de classificação binária rígida.
- Ajuste dinâmico de thresholds conforme perfil do cartão ou contexto operacional.
- Integração do modelo a fluxos de revisão humana.
- Exploração de abordagens não supervisionadas ou semi-supervisionadas para detecção de anomalias.


## 📌 Considerações Finais

O projeto resultou em um pipeline completo, interpretável e metodologicamente consistente para análise de fraude em bilhetagem eletrônica. Mais do que buscar maximizar métricas, o trabalho concentrou-se em compreender o problema, explicitar limitações e propor caminhos realistas de evolução.

A principal contribuição está na clareza do diagnóstico, na avaliação crítica dos trade-offs envolvidos e na construção de uma base sólida para decisões futuras em um ambiente operacional real.


## ✍️ Autoria

Este projeto foi desenvolvido por **Letícia Pacheco**, como estudo aplicado em Ciência de Dados e Aprendizado de Máquina, com foco em detecção de fraude em sistemas de bilhetagem eletrônica.

O trabalho contempla todas as etapas do ciclo de um projeto de Machine Learning, desde a análise exploratória e engenharia de features até a modelagem, avaliação crítica dos resultados e proposição de caminhos de evolução, seguindo boas práticas metodológicas e priorizando interpretabilidade e impacto operacional.
