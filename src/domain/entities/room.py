
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import numpy as np
from pydantic import BaseModel
from shapely.geometry import Polygon, Point
from shapely import speedups
import plotly.express as px
import plotly.graph_objects as go

from src.domain.entities.sensor import Sensor
from src.domain.entities.source import Source


class Room:

    sensors   : List[Sensor]
    sources   : List[Source] = []
    grid      : List[List[float]]
    vertices  : List[Tuple[float, float]]
    resolution: float
    

    def __init__(self, resolution: float = 0.25):
        self.resolution = resolution


    def plot_grid(self) -> None:
        
        x = self.x
        y = self.y
        
        fig = px.scatter(x = x, y = y)
        
        x_s = [sensor.x for sensor in self.sensors]
        y_s = [sensor.y for sensor in self.sensors]
        x_p = [source.x for source in self.sources]
        y_p = [source.y for source in self.sources]
        x_v = [vertix[0] for vertix in self.vertices]
        y_v = [vertix[1] for vertix in self.vertices]
        
        fig.add_trace(go.Scatter(x = x_s, y = y_s, text = ["Sensor 1", "Sensor 2", "Sensor 3", "Sensor 4"], mode = "markers", name = "text"))
        
        if x_p is not [] and y_p is not []:
            fig.add_trace(go.Scatter(x = x_p, y = y_p, text = ["Source 1", "Source 2", "Source 3", "Source 4"], mode = "markers", name = "text"))
        
        fig.add_trace(go.Scatter(x = x_v, y = y_v, text = ["Vertix 1", "Vertix 2", "Vertix 3", "Vertix 4"], mode = "markers", name = "text"))
        fig.show()


    def create_grid(self) -> None:

        if speedups.enabled == False:
            speedups.enable()

        valid_points = []

        vertices = self.vertices
        points   = [Point(vertix[0], vertix[1]) for vertix in vertices]

        # determine maximum edges
        polygon = Polygon(points)
        latmin, lonmin, latmax, lonmax = polygon.bounds
        resolution = 0.25

        points = []
        for lat in np.arange(latmin, latmax, resolution):
            for lon in np.arange(lonmin, lonmax, resolution):
                points.append(Point((round(lat,4), round(lon,4))))

        # validate if each point falls inside shape
        valid_points.extend([i for i in points if polygon.contains(i)])
        new_polygon = Polygon(valid_points)

        x = [point.coords.xy[0][0] for point in valid_points]
        y = [point.coords.xy[1][0] for point in valid_points]

        self.polygon = Polygon(valid_points)
        self.x = x
        self.y = y


    def set_vertixes(self, vertices: List[Tuple[float, float]]) -> None:

        self.vertices = vertices


    def enter_vertices(self) -> None:

        print(" ------- Please enter the vertices of the room ------- ")
        print(" ------- Use the following notation: 'x, y' -------")
        
        vertices = []
        while True:
            try:
                vertix = input()
                vertix = (float(vertix[0]), float(vertix[3]))
                vertices.append(vertix)
            except:
                break
        
        self.vertices = vertices


    def set_sensors(self, sensors: List[Sensor]) -> None:

        self.sensors = sensors


    def enter_sensors(self) -> None:

        print(" ------- Please enter the position of the sensors ------- ")
        print(" ------- Use the following notation: 'x, y' -------")

        sensors = []

        while True:
            try:
                sensor = input()
                sensor = (float(sensor[0]), float(sensor[3]))
                sensors.append(sensor)

            except:
                break

        self.sensors = sensors


    def compute_visions(self):

        for sensor in self.sensors:
            sensor.compute_vision(self.x, self.y)

        for source in self.sources:
            source.compute_vision(self.x, self.y)


    def search_sources(self):

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
            


    def _rectify_vision(self, value: float) -> int:

        if abs(value) > 100 or pd.isna(value):
            return 0

        else:
            return 1