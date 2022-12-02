import pandas as pd


def parse_time_series_data(
    df: pd.DataFrame, x_axis: str | None = None, y_axes: list[str] | None = None
):
    x_axis = x_axis or df.columns[0]
    y_axes = y_axes or df.columns[1:]

    df.dropna(inplace=True)
    df.sort_values(by=x_axis, inplace=True)
    labels = df[x_axis].values

    return {
        "labels": list(labels),
        "datasets": [
            {"data": list(df[column].values), "label": labels[index]}
            for index, column in enumerate(y_axes)
        ],
    }
