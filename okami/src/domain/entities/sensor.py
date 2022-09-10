
import numpy as np
import pandas as pd


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