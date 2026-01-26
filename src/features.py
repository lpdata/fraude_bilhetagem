"""
features.py

Módulo responsável pela definição, organização e validação de features
utilizadas no projeto de detecção de fraude em bilhetagem eletrônica.

Este arquivo não executa engenharia de features bruta (realizada nos notebooks),
mas centraliza:
- definição de papéis das colunas
- agrupamento de features por tipo
- utilitários para seleção consistente de variáveis
"""

from typing import List, Dict


# =========================
# Papéis das colunas
# =========================

COLUNAS_RASTREIO: List[str] = [
    "id_transacao",
    "id_cartao",
    "ts_transacao",
    "data_transacao",
]

COLUNA_ALVO: str = "target_fraude"


# =========================
# Features categóricas
# =========================

FEATURES_CATEGORICAS: List[str] = [
    "temp_faixa",
    "valor_transacao_faixa",
    "periodo_dia",
]


# =========================
# Features numéricas
# =========================

FEATURES_NUMERICAS: List[str] = [
    "hora_transacao",
    "dia_semana",
    "fim_de_semana",
    "tempo_vida_cartao_dias",
    "tempo_desde_ultima_transacao_min",
    "tempo_desde_ultima_transacao_horas",
    "uso_intervalo_curto",
    "qtd_transacoes_dia",
    "qtd_transacoes_24h",
    "uso_intenso_24h",
    "linha_repetida",
    "dispositivo_repetido",
    "qtd_linhas_distintas_dia",
    "qtd_dispositivos_distintos_dia",
    "idade_suspeita",
    "feriado_bin",
    "feriado_nao_mapeado",
    "sentido_ida",
    "clima_adverso",
    "cartao_qtd_transacoes",
    "cartao_dias_ativos",
    "cartao_media_transacoes_por_dia",
    "cartao_qtd_linhas_distintas",
    "cartao_qtd_dispositivos_distintos",
    "cartao_qtd_motoristas_distintos",
    "cartao_valor_transacao_mean",
    "cartao_valor_transacao_std",
    "cartao_pct_integracao",
    "cartao_pct_feriado",
    "cartao_pct_intervalo_curto",
    "valor_vs_media_cartao",
    "valor_zscore_cartao",
    "valor_outlier_cartao",
    "uso_acima_media_dia_cartao",
]


# =========================
# Utilitários
# =========================

def get_features() -> Dict[str, List[str]]:
    """
    Retorna um dicionário com o agrupamento oficial das features.
    Útil para construção de pipelines e validações.
    """
    return {
        "rastreio": COLUNAS_RASTREIO,
        "alvo": [COLUNA_ALVO],
        "categoricas": FEATURES_CATEGORICAS,
        "numericas": FEATURES_NUMERICAS,
    }


def get_feature_names() -> List[str]:
    """
    Retorna a lista completa de features utilizadas na modelagem,
    excluindo colunas de rastreio e a variável alvo.
    """
    return FEATURES_CATEGORICAS + FEATURES_NUMERICAS


def validate_feature_set(columns: List[str]) -> None:
    """
    Valida se o conjunto de colunas fornecido contém todas as features esperadas.
    Levanta erro caso alguma esteja ausente.
    """
    expected = set(get_feature_names())
    received = set(columns)

    missing = expected - received
    if missing:
        raise ValueError(
            f"Conjunto de features inconsistente. Features ausentes: {sorted(missing)}"
        )

