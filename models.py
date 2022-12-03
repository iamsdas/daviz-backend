from enum import Enum


class DataType(str, Enum):
    TRENDS = "trends"
    COMPARISION = "comparision"
    COMPOSITION = "composition"
    DISTRIBUTION = "distribution"
