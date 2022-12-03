import pandas as pd


def parse_continuous_data(
    df: pd.DataFrame, x_axis: str | None = None, y_axes: list[str] | None = None
):

    labels = df[x_axis].values

    return {
        "labels": list(labels),
        "datasets": [
            {"data": list(df[column].values), "label": labels[index]}
            for index, column in enumerate(y_axes)
        ],
    }


def parse_discrete_data(
    df: pd.DataFrame, x_axis: str | None = None, y_axes: list[str] | None = None
):
    labels = df[x_axis].values
    return {
        "labels": list(labels),
        "datasets": [
            {"data": list(df[column].values), "label": labels[index]}
            for index, column in enumerate(y_axes)
        ],
    }


def parse_categorical_data(
    df: pd.DataFrame, x_axis: str | None = None, y_axes: list[str] | None = None
):
    labels = df[x_axis].values
    return {
        "labels": list(labels),
        "datasets": [
            {"data": list(df[column].values), "label": labels[index]}
            for index, column in enumerate(y_axes)
        ],
    }
