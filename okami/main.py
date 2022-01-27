
from typing import List, Tuple

import numpy as np

from okami.src.domain.entities.room import Room
from okami.src.domain.entities.sensor import Sensor
from okami.src.domain.entities.source import Source
from okami.src.domain.entities.variogram import Variogram

from okami.src.services.operation.operation import Operator


class Okami:

    sensors  : List[Sensor]
    room     : Room
    sources  : List[Source]
    variogram: Variogram
    grid_map : np.ndarray


    def __init__(self, vertices: List[Tuple[float, float]], sensors: List[Sensor], res: float) -> None:
        self.sensors = sensors
        self.room    = Room(vertices = vertices, sensors = self.sensors, resolution = res)


    def run_cycle(self) -> None:
        operator = Operator()

        self.sensors   = operator.read_values(sensors = self.sensors)
        self.variogram = operator.get_variogram(sensors = self.sensors)
        self.sources   = operator.locate_sources(sensors = self.sensors, room = self.room)
        self.grid_map  = operator.krigit(sensors = self.sensors, room = self.room, sources = self.sources)


    def show_map(self):
        pass