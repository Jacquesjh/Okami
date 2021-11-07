# %%
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from pydantic import BaseModel
from shapely.geometry import Polygon, Point
from shapely import speedups
import plotly.express as px

from sensor import Sensor
from source import Source

class Room(BaseModel):

    sensors : Optional[List[Sensor]]
    sources : Optional[List[Source]]

    grid    : Optional[List[List[float]]]

    vertices: Optional[List[Tuple[float, float]]]
    
    def plot_grid(self) -> None:
        fig = px.scatter(x = self.x, y = self.y)
        fig.show()


    @classmethod
    def create_grid(cls) -> None:

        if speedups.enabled == False:
            speedups.enable()

        valid_points = []

        vertices = cls._vertices
        points   = [Point(vertix[0], vertix[1]) for vertix in vertices]

        # determine maximum edges
        polygon = Polygon(points)
        latmin, lonmin, latmax, lonmax = polygon.bounds
        resolution = 0.1

        points = []
        for lat in np.arange(latmin, latmax, resolution):
            for lon in np.arange(lonmin, lonmax, resolution):
                points.append(Point((round(lat,4), round(lon,4))))

        # validate if each point falls inside shape
        valid_points.extend([i for i in points if polygon.contains(i)])
        new_polygon = Polygon(valid_points)

        x = [point.coords.xy[0][0] for point in valid_points]
        y = [point.coords.xy[1][0] for point in valid_points]

        cls.polygon = Polygon(valid_points)
        cls.x = x
        cls.y = y

    @classmethod
    def enter_vertices(cls) -> None:

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
        
        cls.vertices = vertices

    @classmethod
    def enter_sensors(cls) -> None:
        
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
        
        cls.sensors = sensors

# %%

room = Room()

# %%

room.enter_vertices()
# %%


room.create_grid()
# %%
room.plot_grid()
# %%
