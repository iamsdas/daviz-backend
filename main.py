from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from utils.models import DataType
from utils.csv_util import CsvUtils

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api")
def get_config(
    csv_file: UploadFile,
    data_type: DataType = Form(),
    x_axis: str | None = Form(default=None),
    y_axes: list[str] | None = Form(default=None),
):
    return CsvUtils(data_type, csv_file, x_axis, y_axes).get_parsed_data()
