
from typing import Dict, List

import numpy as np
import pandas as pd

from okami.src.domain.entities.room import Room
from okami.src.domain.entities.sensor import Sensor
from okami.src.domain.entities.source import Source
from okami.src.domain.entities.variogram import Variogram


class Operator:


    def __init__(self) -> None:
        pass
    

    def _get_connection(self):
        return TimeseriesRepo()

        
    def read_values(self, sensors: List[Sensor]) -> List[Sensor]:
        connection = self._get_connection()

        for sensor in sensors:
            sensor.read_value(connection = connection)

        return sensors


    def get_variogram(self, sensors: List[Sensor]) -> Variogram:
        variances  = self._get_variances(sensors = sensors)
        parameters = self._fit_espherical_variogram(variances)

        variogram = Variogram(nugget = parameters["nugget"], shill = parameters["shill"],
                              e_range = parameters["e_range"])

        return variogram


    @staticmethod
    def _get_variances(sensors: List[Sensor]) -> np.ndarray:
        rows      = int(np.math.factorial(len(sensors))/(np.math.factorial(2)*np.math.factorial(len(sensors) - 2)))
        variances = np.zeros(shape = (rows, 2))

        temp  = sensors.copy()
        index = 0

        for sensor in sensors:            
            aux = temp.copy()
            aux.remove(sensor)

            for pair_sensor in aux:
                mean_variance = (pow(sensor.cache - pair_sensor.cache, 2)/2).mean()
                distance = pow(pow(sensor.x - pair_sensor.x, 2) + pow(sensor.y - pair_sensor.y, 2) + pow(sensor.z - pair_sensor.z, 2), 0.5)

                variances[index, 0] = distance
                variances[index, 1] = round(mean_variance)
                index += 1
                
            temp.remove(sensor)
        
        return variances


    def _fit_espherical_variogram(self):
        pass


    def locate_sources(self, sensors: List[Sensor], room: Room) -> List[Source]:
        pass


    def krigit(self, sensors: List[Sensor], room: Room, sources: List[Source] = []) -> Dict[str, np.ndarray]:
        pass