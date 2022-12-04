from fastapi import FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from utils.parse_utils import ParseUtils

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
    data_type: str = Form(),
    x_axis: str | None = Form(default=None),
    y_axes: list[str] | None = Form(default=None),
):
    return ParseUtils(data_type, csv_file, x_axis, y_axes).get_parsed_data()
