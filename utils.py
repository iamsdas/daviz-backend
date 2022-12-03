from io import StringIO

import pandas as pd
from fastapi import UploadFile


class ParseUtils:
    def __init__(
        self,
        data_type: str,
        csv_file: UploadFile,
        x_axis: str | None = None,
        y_axes: list[str] | None = None,
    ):
        self.x_axis = x_axis
        self.y_axes = y_axes
        self.data_type = data_type
        self.df = pd.read_csv(
            StringIO(str(csv_file.file.read(), "utf-8")), encoding="utf-8"
        )
        self.df.dropna(inplace=True)

        if not self.x_axis or not self.y_axes:
            self.x_axis = self.df.columns[0]
            self.y_axes = self.df.columns[1:]

    def get_parsed_data(self):
        if self.data_type == "comparision":
            return self.parse_data_for_comparision()
        elif self.data_type == "distribution":
            return self.parse_data_for_distribution()
        elif self.data_type == "composition":
            return self.parse_data_for_composition()
        elif self.data_type == "trends":
            return self.parse_data_for_trends()
        else:
            return "invalid data type"

    def parse_data_for_comparision(self):
        labels = self.df[self.x_axis].values

        return {
            "labels": list(labels),
            "datasets": [
                {"data": list(self.df[column].values), "label": labels[index]}
                for index, column in enumerate(self.y_axes)
            ],
        }

    def parse_data_for_distribution(self):
        if len(self.y_axes) > 1:
            self.y_axes = [self.y_axes[0]]
        labels = self.df[self.x_axis].values

        return {
            "labels": list(labels),
            "datasets": [
                {"data": list(self.df[column].values), "label": labels[index]}
                for index, column in enumerate(self.y_axes)
            ],
        }

    def parse_data_for_composition(self):
        labels = self.df[self.x_axis].values

        return {
            "labels": list(labels),
            "datasets": [
                {"data": list(self.df[column].values), "label": labels[index]}
                for index, column in enumerate(self.y_axes)
            ],
        }

    def parse_data_for_trends(self):
        labels = self.df[self.x_axis].values

        return {
            "labels": list(labels),
            "datasets": [
                {"data": list(self.df[column].values), "label": labels[index]}
                for index, column in enumerate(self.y_axes)
            ],
        }
