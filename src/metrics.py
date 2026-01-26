"""
metrics.py

Módulo de métricas e utilitários de avaliação para o projeto de detecção de fraude
em bilhetagem eletrônica.

Objetivos:
- Padronizar o cálculo de métricas no holdout
- Consolidar resultados de validação cruzada
- Apoiar análise de trade-off operacional (alertas vs fraudes capturadas)

Observação:
Este projeto prioriza PR-AUC (Average Precision) como métrica principal,
por ser mais informativa em cenários desbalanceados e alinhada ao objetivo de
priorização de risco.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, Optional

import numpy as np
import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


# =========================
# Estruturas e constantes
# =========================

DEFAULT_METRICS: Tuple[str, ...] = ("pr_auc", "roc_auc", "precision", "recall", "f1")


@dataclass(frozen=True)
class HoldoutResults:
    pr_auc: float
    roc_auc: float
    precision: float
    recall: float
    f1: float


# =========================
# Métricas principais
# =========================

def compute_classification_metrics(
    y_true: np.ndarray,
    y_proba: np.ndarray,
    threshold: float = 0.5,
    zero_division: int = 0,
) -> HoldoutResults:
    """
    Calcula o conjunto padrão de métricas do projeto a partir de probabilidades.

    Parâmetros
    ----------
    y_true : array
        Rótulos verdadeiros (0/1).
    y_proba : array
        Probabilidades estimadas para classe positiva (fraude = 1).
    threshold : float
        Limiar para converter probabilidade em classe.
    zero_division : int
        Comportamento do precision/recall quando não há positivos previstos.

    Retorno
    -------
    HoldoutResults
        Conjunto padronizado de métricas.
    """
    y_true = np.asarray(y_true).astype(int)
    y_proba = np.asarray(y_proba).astype(float)

    y_pred = (y_proba >= threshold).astype(int)

    pr_auc = float(average_precision_score(y_true, y_proba))
    # ROC-AUC exige ambas as classes presentes
    roc_auc = float(roc_auc_score(y_true, y_proba)) if len(np.unique(y_true)) > 1 else float("nan")
    precision = float(precision_score(y_true, y_pred, zero_division=zero_division))
    recall = float(recall_score(y_true, y_pred, zero_division=zero_division))
    f1 = float(f1_score(y_true, y_pred, zero_division=zero_division))

    return HoldoutResults(
        pr_auc=pr_auc,
        roc_auc=roc_auc,
        precision=precision,
        recall=recall,
        f1=f1,
    )


def compute_confusion_matrix(
    y_true: np.ndarray,
    y_proba: np.ndarray,
    threshold: float = 0.5,
) -> pd.DataFrame:
    """
    Retorna a matriz de confusão em formato DataFrame com rótulos legíveis.
    """
    y_true = np.asarray(y_true).astype(int)
    y_proba = np.asarray(y_proba).astype(float)
    y_pred = (y_proba >= threshold).astype(int)

    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    return pd.DataFrame(
        cm,
        index=["Real: Não Fraude", "Real: Fraude"],
        columns=["Predito: Não Fraude", "Predito: Fraude"],
    )


# =========================
# Utilitários de consolidação
# =========================

def holdout_results_to_dataframe(results: HoldoutResults) -> pd.DataFrame:
    """
    Converte HoldoutResults em DataFrame (coluna 'valor'), padrão de relatório.
    """
    return pd.DataFrame(
        {
            "valor": {
                "pr_auc": results.pr_auc,
                "roc_auc": results.roc_auc,
                "precision": results.precision,
                "recall": results.recall,
                "f1": results.f1,
            }
        }
    )


def consolidate_cv_results(
    cv_summary: Dict[str, Dict[str, float]] | pd.DataFrame,
    model_name: str,
) -> pd.DataFrame:
    """
    Padroniza o output de validação cruzada (média e desvio) em um formato longo
    para consolidação entre modelos.

    Aceita:
    - dict no formato {metric: {"mean": x, "std": y}}
    - DataFrame com índice em métricas e colunas ['mean','std'] (ou equivalente)

    Retorna DataFrame com colunas: ['modelo','metrica','mean','std'].
    """
    if isinstance(cv_summary, dict):
        rows = []
        for metric, stats in cv_summary.items():
            rows.append(
                {
                    "modelo": model_name,
                    "metrica": metric,
                    "mean": float(stats.get("mean", np.nan)),
                    "std": float(stats.get("std", np.nan)),
                }
            )
        return pd.DataFrame(rows)

    if isinstance(cv_summary, pd.DataFrame):
        df = cv_summary.copy()
        df = df.rename_axis("metrica").reset_index()
        cols = {c.lower(): c for c in df.columns}
        mean_col = cols.get("mean")
        std_col = cols.get("std")
        if mean_col is None or std_col is None:
            raise ValueError("DataFrame de CV deve conter colunas 'mean' e 'std'.")
        df = df[["metrica", mean_col, std_col]].rename(columns={mean_col: "mean", std_col: "std"})
        df.insert(0, "modelo", model_name)
        return df

    raise TypeError("cv_summary deve ser dict ou pandas.DataFrame.")


# =========================
# Trade-off operacional
# =========================

def operational_tradeoff(
    y_true: np.ndarray,
    y_proba: np.ndarray,
    threshold: float = 0.5,
) -> Dict[str, float]:
    """
    Calcula indicadores operacionais simples no holdout:
    - alertas_totais: número de transações sinalizadas como fraude
    - pct_alertas: proporção de alertas sobre o total
    - fraudes_capturadas: verdadeiros positivos
    - fraudes_perdidas: falsos negativos
    - precision, recall no threshold adotado
    """
    y_true = np.asarray(y_true).astype(int)
    y_proba = np.asarray(y_proba).astype(float)
    y_pred = (y_proba >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

    alertas_totais = int(tp + fp)
    total = int(len(y_true))
    pct_alertas = float(alertas_totais / total) if total else float("nan")

    precision = float(precision_score(y_true, y_pred, zero_division=0))
    recall = float(recall_score(y_true, y_pred, zero_division=0))

    return {
        "alertas_totais": alertas_totais,
        "pct_alertas": pct_alertas,
        "fraudes_capturadas": int(tp),
        "fraudes_perdidas": int(fn),
        "precision": precision,
        "recall": recall,
    }


def tradeoff_table(
    y_true: np.ndarray,
    proba_by_model: Dict[str, np.ndarray],
    threshold: float = 0.5,
) -> pd.DataFrame:
    """
    Gera tabela comparativa de trade-off operacional entre modelos, no mesmo padrão
    usado para relatório.

    Parâmetros
    ----------
    y_true : array
        Target do holdout.
    proba_by_model : dict
        Mapeia nome do modelo -> probabilidades no holdout.
    threshold : float
        Threshold fixo para comparação.

    Retorno
    -------
    DataFrame com colunas:
    ['modelo','alertas_totais','pct_alertas','fraudes_capturadas','fraudes_perdidas','precision','recall']
    """
    rows = []
    for model_name, y_proba in proba_by_model.items():
        stats = operational_tradeoff(y_true=y_true, y_proba=y_proba, threshold=threshold)
        rows.append({"modelo": model_name, **stats})

    df = pd.DataFrame(rows)
    return df.sort_values(by="pct_alertas", ascending=False).reset_index(drop=True)

