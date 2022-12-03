from io import StringIO

import pandas as pd
from fastapi import FastAPI, UploadFile, Form

from utils import parse_time_series_data

app = FastAPI()


@app.post("/api")
def get_config(
    csv_file: UploadFile,
    data_type: str = Form(),
    x_axis: str | None = Form(default=None),
    y_axes: list[str] | None = Form(default=None),
):
    df = pd.read_csv(StringIO(str(csv_file.file.read(), "utf-8")), encoding="utf-8")
    if data_type == "time_series":
        return parse_time_series_data(df, x_axis, y_axes)
    return "invalid data type"
