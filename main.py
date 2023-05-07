from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from utils.time_series import TimeSeriesGenerator
from utils.models import DataType, TimeSeriesInput
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
    y_axes: str | None = Form(default=None),
    identifier: str | None = Form(default=None),
):
    return CsvUtils(data_type, csv_file, x_axis, y_axes, identifier).get_parsed_data()


@app.post("/api/predict")
def get_prediction(data: TimeSeriesInput):
    time_series = TimeSeriesGenerator(data.series)
    return time_series.predict().tolist()
