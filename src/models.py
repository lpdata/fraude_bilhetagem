"""
models.py

Módulo responsável pela definição dos modelos supervisionados utilizados
no projeto de detecção de fraude em bilhetagem eletrônica.

Este arquivo centraliza:
- criação dos estimadores
- definição de hiperparâmetros base
- construção de pipelines com pré-processamento
- utilitários para treino e predição

Os modelos aqui definidos refletem exatamente os modelos avaliados
nos notebooks, priorizando interpretabilidade e controle operacional.
"""

from __future__ import annotations

from typing import Dict, Any

import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from src.features import FEATURES_NUMERICAS, FEATURES_CATEGORICAS


# =========================
# Pré-processamento comum
# =========================

def build_preprocessor(
    scale_numeric: bool = False,
) -> ColumnTransformer:
    """
    Constrói o ColumnTransformer padrão do projeto.

    Parâmetros
    ----------
    scale_numeric : bool
        Define se as variáveis numéricas devem ser padronizadas.
        Utilizado principalmente para modelos lineares.

    Retorno
    -------
    ColumnTransformer
    """
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
                    sparse_output=False,
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, FEATURES_NUMERICAS),
            ("cat", categorical_transformer, FEATURES_CATEGORICAS),
        ],
        remainder="drop",
    )

    return preprocessor


# =========================
# Modelos
# =========================

def build_logistic_regression(
    random_state: int = 42,
) -> Pipeline:
    """
    Regressão Logística como baseline interpretável.

    Configuração alinhada ao notebook:
    - regularização L2
    - class_weight balanceado
    - número elevado de iterações
    """
    preprocessor = build_preprocessor(scale_numeric=True)

    estimator = LogisticRegression(
        penalty="l2",
        C=1.0,
        class_weight="balanced",
        solver="lbfgs",
        max_iter=2000,
        random_state=random_state,
    )

    return Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", estimator),
        ]
    )


def build_decision_tree(
    random_state: int = 42,
) -> Pipeline:
    """
    Árvore de Decisão com regularização explícita para controle de overfitting.
    """
    preprocessor = build_preprocessor(scale_numeric=False)

    estimator = DecisionTreeClassifier(
        max_depth=6,
        min_samples_split=100,
        min_samples_leaf=50,
        random_state=random_state,
    )

    return Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", estimator),
        ]
    )


def build_random_forest(
    random_state: int = 42,
) -> Pipeline:
    """
    Random Forest como ensemble para redução de variância.

    Configuração base alinhada ao notebook.
    """
    preprocessor = build_preprocessor(scale_numeric=False)

    estimator = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_split=100,
        min_samples_leaf=50,
        n_jobs=-1,
        random_state=random_state,
    )

    return Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", estimator),
        ]
    )


# =========================
# Fábrica de modelos
# =========================

def get_models(random_state: int = 42) -> Dict[str, Pipeline]:
    """
    Retorna um dicionário com todos os modelos avaliados no projeto.
    """
    return {
        "Regressão Logística": build_logistic_regression(random_state),
        "Árvore de Decisão": build_decision_tree(random_state),
        "Random Forest": build_random_forest(random_state),
    }


# =========================
# Utilitários
# =========================

def fit_model(
    model: Pipeline,
    X_train,
    y_train,
) -> Pipeline:
    """
    Ajusta o pipeline no conjunto de treino.
    """
    model.fit(X_train, y_train)
    return model


def predict_proba(
    model: Pipeline,
    X,
) -> np.ndarray:
    """
    Retorna as probabilidades da classe positiva (fraude).
    """
    if not hasattr(model, "predict_proba"):
        raise AttributeError("Modelo não suporta predict_proba.")
    return model.predict_proba(X)[:, 1]

