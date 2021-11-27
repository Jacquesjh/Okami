# %%

import pandas as pd
import plotly.graph_objects as go


from src.domain.entities.room import Room
from src.domain.entities.sensor import Sensor
from src.utils.functions import artificial_source, ajust_sensors


room = Room()
vertix1 = (0, 0)
vertix2 = (0, 4)
vertix3 = (4, 4)
vertix4 = (4, 0)

vertices = [vertix1, vertix2, vertix3, vertix4]
room.set_vertixes(vertices = vertices)

sensor1 = Sensor(x = 0.75, y = 1, z = 1.5)
sensor2 = Sensor(x = 1.25, y = 2.75, z = 1.5)
sensor3 = Sensor(x = 3, y = 3, z = 1.5)
sensor4 = Sensor(x = 2.75, y = 1, z = 1.5)
sensors = [sensor1, sensor2, sensor3, sensor4]
room.set_sensors(sensors = sensors)

room.create_grid()
room.plot_grid()

# %%

room.compute_visions()
room.sensors[0].plot_vision()

# %%

coords, values = artificial_source()

room.search_sources()


# %%

fig = go.Figure(data=[go.Surface(x = X, y = Y, z = Z)])

fig.update_layout(title='Mt Bruno Elevation', autosize=False,
                  width=500, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))

fig.show()
