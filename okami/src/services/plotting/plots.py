
from typing import List

import plotly.express as px
import plotly.graph_objects as go

from okami.src.domain.entities.room import Room
from okami.src.domain.entities.sensor import Sensor


def plot_room(room: Room) -> None:
    x = room.grid[0]
    y = room.grid[1]

    fig = px.scatter(x = x, y = y)

    x_s = [sensor.x for sensor in room.sensors]
    y_s = [sensor.y for sensor in room.sensors]
    x_p = [source.x for source in room.sources]
    y_p = [source.y for source in room.sources]
    x_v = [vertix[0] for vertix in room.vertices]
    y_v = [vertix[1] for vertix in room.vertices]

    fig.add_trace(go.Scatter(x = x_s, y = y_s, text = ["Sensor 1", "Sensor 2", "Sensor 3", "Sensor 4"], mode = "markers", name = "Sensors"))
    fig.add_trace(go.Scatter(x = x_v, y = y_v, text = ["Vertix 1", "Vertix 2", "Vertix 3", "Vertix 4"], mode = "markers", name = "Vertices"))

    if x_p is not [] and y_p is not []:
        fig.add_trace(go.Scatter(x = x_p, y = y_p, text = ["Source 1", "Source 2", "Source 3", "Source 4"], mode = "markers", name = "Sources"))
    
    fig.show()


def plot_single_sensor_vision(sensor: Sensor) -> None:
    X, Y = np.meshgrid(sensor.vision.index.tolist(), sensor.vision.columns)
    
    fig = go.Figure(data = [go.Surface(x = np.array(sensor.vision.index.tolist()), y = np.array(sensor.vision.columns),
                                        z = sensor.vision.T.values, colorscale = "viridis", opacity = 0.75)])
    
    # fig = go.Figure(data=[go.Surface(z = self.vision.values,
    #                                  colorscale = "viridis", opacity = 0.75)])
    fig.update_traces(contours_z = dict(show = True, usecolormap = True,
                                        highlightcolor = "limegreen", project_z = True))

    fig.add_scatter3d(x = [sensor.x], y = [sensor.y], z = [sensor.value], mode = "markers")
    
    fig.update_layout(title = "Sensor Ambient Vision", autosize = False,
                        margin = dict(l = 50, r = 50, b = 10, t = 50))
    fig.show()



def plot_sensors_vision(sensors: List[Sensor]) -> None:
    pass