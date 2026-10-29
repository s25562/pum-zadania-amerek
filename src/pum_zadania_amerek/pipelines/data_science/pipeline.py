"""
This is a boilerplate pipeline 'data_science'
generated using Kedro 1.7.0
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    prepare_titanic,
    prepare_orders,
    train_titanic,
    train_orders,
    evaluate_model,
)


def create_pipeline(**kwargs) -> Pipeline:
    titanic = pipeline([
        node(
            func=prepare_titanic,
            inputs=["titanic_train", "params:titanic"],
            outputs="titanic_train_primary",
            name="prepare_titanic",
        ),
        node(
            func=train_titanic,
            inputs=["titanic_train_primary", "params:titanic"],
            outputs=["titanic_train_model", "titanic_X_test", "titanic_y_test"],
            name="train_titanic",
        ),
        node(
            func=evaluate_model,
            inputs=["titanic_train_model", "titanic_X_test", "titanic_y_test"],
            outputs=["titanic_train_metrics", "titanic_train_confusion_matrix"],
            name="evaluate_titanic",
        ),
    ])

    orders = pipeline([
        node(
            func=prepare_orders,
            inputs=["datasets_orders", "params:orders"],
            outputs="datasets_orders_primary",
            name="prepare_orders",
        ),
        node(
            func=train_orders,
            inputs=["datasets_orders_primary", "params:orders"],
            outputs=["datasets_orders_model", "orders_X_test", "orders_y_test"],
            name="train_orders",
        ),
        node(
            func=evaluate_model,
            inputs=["datasets_orders_model", "orders_X_test", "orders_y_test"],
            outputs=["datasets_orders_metrics", "datasets_orders_confusion_matrix"],
            name="evaluate_orders",
        ),
    ])

    return titanic + orders
