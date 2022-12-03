from fastapi import FastAPI, Form, UploadFile

from utils import ParseUtils

app = FastAPI()


@app.post("/api")
def get_config(
    csv_file: UploadFile,
    data_type: str = Form(),
    x_axis: str | None = Form(default=None),
    y_axes: list[str] | None = Form(default=None),
):
    return ParseUtils(data_type, csv_file, x_axis, y_axes).get_parsed_data()
