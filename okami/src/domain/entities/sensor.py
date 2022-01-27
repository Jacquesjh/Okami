
from typing import Any, List

import numpy as np
from pydantic import BaseModel
import pandas as pd

# from okami.src.core.repositories.timescale.interface import ITimescaleRepository


class Sensor:


    id   : str
    value: float
    cache: np.ndarray
    x    : float
    y    : float
    z    : float


    def __init__(self, id: str, x: float, y: float, z: float = 0, cache_size: int = 10) -> None:
        self.id    = id
        self.value = 400
        self.cache = np.array([400]*cache_size)
        self.x     = x
        self.y     = y
        self.z     = z
        

    # def compute_vision(self, x: List[float], y: List[float]) -> None:
    #     data = pd.DataFrame(columns = np.unique(y), index = np.unique(x))

    #     for x_value, y_value in zip(x, y):
    #         data.loc[x_value, y_value] = self._decay(x_value, y_value)

    #     self.vision = data