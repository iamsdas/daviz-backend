from enum import Enum
from pydantic import BaseModel


class DataType(str, Enum):
    TRENDS = "trends"
    COMPARISION = "comparision"
    COMPOSITION = "composition"
    DISTRIBUTION = "distribution"


class TimeSeriesInput(BaseModel):
    series: list[float]
