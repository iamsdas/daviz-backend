from io import StringIO

import pandas as pd
from fastapi import FastAPI, UploadFile, Form

from utils import parse_continuous_data, parse_categorical_data, parse_discrete_data

app = FastAPI()


@app.post("/api")
def get_config(
    csv_file: UploadFile,
    data_type: str = Form(),
    x_axis: str | None = Form(default=None),
    y_axes: list[str] | None = Form(default=None),
):
    df = pd.read_csv(StringIO(str(csv_file.file.read(), "utf-8")), encoding="utf-8")
    df.dropna(inplace=True)
    if x_axis is None or x_axis == "" or y_axes is None or y_axes == []:
        x_axis = df.columns[0]
        y_axes = df.columns[1:]
    df.sort_values(by=x_axis, inplace=True)

    if data_type == "continuous":
        return parse_continuous_data(df, x_axis, y_axes)
    if data_type == "discrete":
        return parse_discrete_data(df, x_axis, y_axes)
    if data_type == "categorical":
        return parse_categorical_data(df, x_axis, y_axes)

    return "invalid data type"
