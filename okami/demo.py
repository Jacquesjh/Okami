
from typing import List, Tuple
from datetime import datetime, timedelta

import numpy as np

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
    real_map : np.ndarray

    ts: int

    
    def __init__(self, vertices: List[Tuple[float, float]], sensors: List[Sensor], res: float, num_sources: int, time_steps: int) -> None:
        self.sensors = sensors
        self.room    = Room(vertices = vertices, sensors = self.sensors, resolution = res)
        self._generate_fake_sources_data(num_sources = num_sources, time_steps = time_steps)
        self.ts = 0
        

    @staticmethod
    def _decay_function(distance: float, value: float) -> float:
        c0 = 1200
        c1 = 50000
        a  = 2.5

        y = c0 + c1*((1.5*distance/a) - 0.5*pow(distance/a, 3))
        r = value - pow(2*abs(y), 0.5)

        if distance > 2.5 or r < 0:
            return 0

        else:
            return r


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

        self.real_map = np.array([grid[0], grid[1], values])


    def read_values(self, sensors) -> None:
        self._permeate_space()

        for sensor in sensors:
            x = round(sensor.x/self.room.resolution)
            y = round(sensor.y/self.room.resolution)
            
            sensor.value = self.real_map[2, x*y]
            sensor.cache = np.append(sensor.cache, sensor.value)[1: ]

        return sensors


    def _generate_fake_sources_data(self, num_sources: int, time_steps: int) -> None:
        sources = []

        for num in range(num_sources):
            sources.append(artificial_source(time_steps = time_steps))

        self.fake_data = sources

    
    def generate_fake_map(self, num_sources: int, time_steps: int) -> None:
        self._generate_sources_data(num_sources = num_sources, time_steps = time_steps)


    def run_cycle(self) -> None:
        operator = Operator()
        
        tm = datetime(2022, 1, 1, 12) + timedelta(seconds = 30*self.ts)
        print(tm)

        self.sensors = self.read_values(sensors = self.sensors)
        # self.variogram = operator.get_variogram(sensors = self.sensors)
        # self.sources   = operator.locate_sources(sensors = self.sensors, room = self.room)
        # self.grid_map  = operator.krigit(sensors = self.sensors, room = self.room, sources = self.sources)

        self.ts += 1
