
from typing import List, Tuple
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from okami.main import Okami

from okami.src.domain.entities.room import Room
from okami.src.domain.entities.sensor import Sensor
from okami.src.domain.entities.source import Source
from okami.src.domain.entities.variogram import Variogram

from okami.src.services.operation.operation import Operator

from okami.src.utils.functions import artificial_source


class Demo(Okami):

    sensors  : List[Sensor]
    room     : Room
    sources  : List[Source]
    variogram: Variogram

    fake_data: List[np.ndarray]

    grid_map : np.ndarray
    real_map : pd.DataFrame
    
    ts: int

    
    def __init__(self, vertices: List[Tuple[float, float]], sensors: List[Sensor], res: float, num_sources: int, time_steps: int) -> None:
        self.sensors = sensors
        self.sources = []
        self.room    = Room(vertices = vertices, sensors = self.sensors, resolution = res)
        self._generate_fake_sources_data(num_sources = num_sources, time_steps = time_steps)
        self.ts = 0
        
        self.operator = Operator()
        
    
    @staticmethod
    def _decay_function(distance: float, value: float) -> float:
        y = pow(np.e, -pow(distance, 2)/1.5)*value

        return y


    def _permeate_space(self) -> None:
        grid   = self.room.grid
        ts     = self.ts        
        values = []

        for x, y in zip(grid[0], grid[1]):
            aprox = []

            for source in self.fake_data:
                distance = pow(pow(x - source[0, ts], 2) + pow(y - source[1, ts], 2), 0.5)
                aprox.append(self._decay_function(distance = distance, value = source[2, ts]))
                
            values.append(sum(aprox) + 400)

        df = pd.DataFrame(columns = np.unique(grid[0]), index = np.unique(grid[1])[::-1])

        for i in range(len(grid[0])):
            df[grid[0, i]].loc[grid[1, i]] = values[i]

        self.real_map = df


    def read_values(self, sensors) -> None:
        self._permeate_space()

        for sensor in sensors:
            sensor.value = self.real_map[sensor.x].loc[sensor.y]
            sensor.cache = np.append(sensor.cache, sensor.value)[1: ]

        return sensors


    def _generate_fake_sources_data(self, num_sources: int, time_steps: int) -> None:
        sources = []

        for num in range(num_sources):
            sources.append(artificial_source(time_steps = time_steps))

        self.fake_data = sources


    def run_cycle(self) -> None:
        operator = self.operator
        
        self.sources   = []
        self.variogram = None
        
        tm = datetime(2022, 1, 1, 12) + timedelta(seconds = 30*self.ts)
        print(tm)

        self.sensors   = self.read_values(sensors = self.sensors)
        self.variogram = operator.get_variogram(sensors = self.sensors)

        # self.sources   = operator.locate_sources(sensors = self.sensors, room = self.room)

        if self.variogram is not None:
            # self.sources = operator.locate_sources(sensors = self.sensors, room = self.room, variogram = self.variogram)

            krigig_inter = operator.krigit(sensors = self.sensors, room = self.room, variogram = self.variogram, sources = self.sources)
            simple_inter = operator.simple_interpolation(sensors = self.sensors, room = self.room, sources = self.sources)

            self.grid_map = (0.5*simple_inter + 0.5*krigig_inter)

        else:
            simple_inter = operator.simple_interpolation(sensors = self.sensors, room = self.room, sources = self.sources)
            self.grid_map = simple_inter

        
        self.ts += 1