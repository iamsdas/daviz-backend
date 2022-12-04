from io import StringIO

from pandas import read_csv
from fastapi import HTTPException, UploadFile

from utils.models import DataType


class ParseUtils:
    def __init__(
        self,
        data_type: DataType,
        csv_file: UploadFile,
        x_axis: str | None = None,
        y_axes: list[str] | None = None,
    ):
        self.x_axis = x_axis
        self.y_axes = y_axes
        self.data_type = data_type
        self.df = read_csv(
            StringIO(str(csv_file.file.read(), "utf-8")), encoding="utf-8"
        )

        if not self.x_axis or not self.y_axes:
            self.x_axis = self.df.columns[0]
            self.y_axes = self.df.columns[1:]

        self.df.dropna(inplace=True)

    def get_parsed_data(self):
        if self.data_type == DataType.COMPARISION:
            return self.parse_data_for_comparision()
        elif self.data_type == DataType.DISTRIBUTION:
            return self.parse_data_for_distribution()
        elif self.data_type == DataType.COMPOSITION:
            return self.parse_data_for_composition()
        elif self.data_type == DataType.TRENDS:
            return self.parse_data_for_trends()
        else:
            raise HTTPException(status_code=404, detail="Invalid data type")

    def get_json_data(self):
        labels = self.df[self.x_axis].values

        return {
            "data": {
                "labels": list(labels),
                "datasets": [
                    {"data": list(self.df[column].values), "label": labels[index]}
                    for index, column in enumerate(self.y_axes)
                ],
            },
        }

    def parse_data_for_comparision(self):
        return self.get_json_data()

    def parse_data_for_distribution(self):
        self.y_axes = [self.y_axes[0]] if len(self.y_axes) > 1 else self.y_axes
        return self.get_json_data()

    def parse_data_for_composition(self):
        return self.get_json_data()

    def parse_data_for_trends(self):
        return self.get_json_data()
