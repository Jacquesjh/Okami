
from typing import List, Tuple

import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point
from shapely import speedups

from okami.src.domain.entities.sensor import Sensor
from okami.src.domain.entities.source import Source


class Room:

    sensors   : List[Sensor]
    sources   : List[Source]
    grid      : List[List[float]]
    vertices  : List[Tuple[float, float]]
    resolution: float
    

    def __init__(self, vertices: List[Tuple[float, float]], sensors: List[Sensor], resolution: float = 0.25) -> None:
        self.resolution = resolution
        self.vertices   = vertices
        self.sensors    = sensors
        self.sources    = []

        if speedups.enabled == False:
            speedups.enable()

        self._create_grid()


    def _create_grid(self) -> None:
        valid_points = []

        vertices = self.vertices
        points   = [Point(vertix[0], vertix[1]) for vertix in vertices]

        polygon = Polygon(points)
        latmin, lonmin, latmax, lonmax = polygon.bounds
        resolution = 0.25

        points = []
        for lat in np.arange(latmin, latmax, resolution):
            for lon in np.arange(lonmin, lonmax, resolution):
                points.append(Point((round(lat, 4), round(lon, 4))))

        valid_points.extend([i for i in points if polygon.contains(i)])
        new_polygon = Polygon(valid_points)

        x = [point.coords.xy[0][0] for point in valid_points]
        y = [point.coords.xy[1][0] for point in valid_points]

        self.polygon = Polygon(valid_points)
        self.grid = np.array([x, y])


    def compute_visions(self) -> None:
        for sensor in self.sensors:
            sensor.compute_vision(self.grid[0], self.grid[1])


    def search_sources(self) -> None:
        self.compute_visions()

        sensors_list = self.sensors.copy()

        for sensor in sensors_list:
            sensors_list.remove(sensor)
            aux_list = sensors_list.copy()

            for pair_sensor in aux_list:
                dt = sensor.vision - pair_sensor.vision
                dt.applymap(self._rectify_vision)

                for row in dt.index.tolist():
                    for column in dt.columns:
                        if dt.loc[row, column] == 1:
                            value = (sensor.loc[row, column] + pair_sensor.loc[row, column])/2

                            new_source = Source(x = row, y = column, value = value)
                            self.sources.append(new_source)


    @staticmethod
    def _rectify_vision(value: float) -> int:
        if abs(value) > 100 or pd.isna(value):
            return 0

        else:
            return 1