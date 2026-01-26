"""
preprocessing.py

Módulo de pré-processamento para o projeto de detecção de fraude.

Este arquivo fornece componentes reutilizáveis e consistentes com o que foi
implementado no notebook de modelagem:
- definição do ColumnTransformer padrão (numérico + categórico)
- suporte a padronização numérica quando necessário (modelos lineares)
- utilitários para inspeção de nomes pós-encoding (interpretabilidade)

Observação:
A engenharia de features bruta foi realizada nos notebooks e exportada para
data/processed. Aqui lidamos apenas com preparação para modelagem.
"""

from __future__ import annotations

from typing import List, Tuple

import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from src.features import FEATURES_NUMERICAS, FEATURES_CATEGORICAS


# =========================
# Construção do preprocessador
# =========================

def build_preprocessor(
    numeric_features: List[str] | None = None,
    categorical_features: List[str] | None = None,
    scale_numeric: bool = False,
    ohe_sparse: bool = False,
) -> ColumnTransformer:
    """
    Constrói o ColumnTransformer padrão do projeto.

    Parâmetros
    ----------
    numeric_features : list[str] | None
        Lista de features numéricas. Se None, usa a lista oficial do projeto.
    categorical_features : list[str] | None
        Lista de features categóricas. Se None, usa a lista oficial do projeto.
    scale_numeric : bool
        Se True, aplica StandardScaler nas variáveis numéricas.
        Recomendado para modelos lineares.
    ohe_sparse : bool
        Se True, produz matriz esparsa no OneHotEncoder.
        Por padrão (False), retorna denso para facilitar interpretabilidade
        e extração de coeficientes.

    Retorno
    -------
    ColumnTransformer
    """
    numeric_features = numeric_features or FEATURES_NUMERICAS
    categorical_features = categorical_features or FEATURES_CATEGORICAS

    numeric_steps = [
        ("imputer", SimpleImputer(strategy="median")),
    ]
    if scale_numeric:
        numeric_steps.append(("scaler", StandardScaler()))
    numeric_transformer = Pipeline(steps=numeric_steps)

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=ohe_sparse,
                ),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


# =========================
# Utilitários de interpretabilidade
# =========================

def get_feature_names_after_preprocessing(
    preprocessor: ColumnTransformer,
) -> List[str]:
    """
    Recupera os nomes das features após o pré-processamento
    (incluindo nomes pós one-hot encoding).

    Requisitos:
    - o preprocessor precisa estar ajustado (fit) antes.
    """
    if not hasattr(preprocessor, "get_feature_names_out"):
        raise AttributeError("O preprocessor não suporta get_feature_names_out.")

    names = preprocessor.get_feature_names_out()
    return [str(n) for n in names]


def split_feature_groups(
    X_columns: List[str],
    categorical_features: List[str] | None = None,
) -> Tuple[List[str], List[str]]:
    """
    Função utilitária para separar automaticamente features categóricas e numéricas
    a partir da lista de colunas de X.

    Isso ajuda a manter consistência caso o dataset mude levemente.

    Parâmetros
    ----------
    X_columns : list[str]
        Lista de colunas presentes em X.
    categorical_features : list[str] | None
        Lista de categóricas oficiais. Se None, usa a lista do projeto.

    Retorno
    -------
    (categoricas, numericas)
    """
    categorical_features = categorical_features or FEATURES_CATEGORICAS

    cats = [c for c in X_columns if c in categorical_features]
    nums = [c for c in X_columns if c not in cats]
    return cats, nums


def check_missing_ratio(
    X,
    threshold: float = 0.3,
):
    """
    Retorna um DataFrame com taxa de nulos por coluna e um filtro
    para colunas com taxa acima do threshold.

    Útil para diagnósticos rápidos antes da modelagem.
    """
    import pandas as pd

    if not hasattr(X, "isna"):
        raise TypeError("X precisa ser um pandas DataFrame para checagem de nulos.")

    missing = X.isna().mean().sort_values(ascending=False)
    df = pd.DataFrame({"missing_ratio": missing})
    df["above_threshold"] = df["missing_ratio"] > threshold
    return df

