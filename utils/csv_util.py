from io import StringIO

import numpy as np
from fastapi import HTTPException, UploadFile
from pandas import read_csv

from utils.models import DataType


class CsvUtils:
    def __init__(
        self,
        data_type: DataType,
        csv_file: UploadFile,
        x_axis: str | None = None,
        y_axes: str | None = None,
    ):
        self.x_axis = x_axis
        self.y_axes = (
            [y_axis.strip() for y_axis in y_axes.split(",")] if y_axes else None
        )
        self.data_type = data_type
        self.load_data(csv_file)

    def load_data(self, csv_file: UploadFile):
        self.df = read_csv(
            StringIO(str(csv_file.file.read(), "utf-8")), encoding="utf-8"
        )

        if not self.x_axis or not self.y_axes:
            self.x_axis = self.df.columns[0]
            self.y_axes = self.df.columns[1:]

        self.df.drop(
            columns=self.df.columns.difference(self.y_axes + [self.x_axis]),
            inplace=True,
        )
        self.analytics = self.get_analytics()
        self.df.dropna(inplace=True)
        self.df.drop_duplicates(inplace=True)

    def get_analytics(self):
        result = [
            {
                "name": "Total",
                "invalids": int(self.df.isna().sum().sum()),
                "rows": len(self.df),
                "duplicates": int(self.df.duplicated().sum()),
            }
        ]
        for column in self.df.columns:
            column_analytics = {
                "name": column,
                "invalids": int(self.df[column].isna().sum()),
                "unique": int(self.df[column].nunique()),
            }
            try:
                column_analytics["min"] = self.df[column].min()
                column_analytics["max"] = self.df[column].max()
                column_analytics["mean"] = self.df[column].mean()
                column_analytics["median"] = self.df[column].median()
                column_analytics["std"] = self.df[column].std()
                column_analytics["var"] = self.df[column].var()
                column_analytics["skew"] = self.df[column].skew()
                column_analytics["mode"] = self.df[column].mode().to_list()
                column_analytics["kurtosis"] = self.df[column].kurtosis()
            except TypeError:
                pass
            for key, value in column_analytics.items():
                if isinstance(value, np.generic):
                    column_analytics[key] = value.item()
            result.append(column_analytics)
        return result

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
                    {"data": list(self.df[column].values), "label": column}
                    for index, column in enumerate(self.y_axes)
                ],
            },
            "analytics": self.analytics,
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
