# %%

from src.domain.entities.room import Room
from src.domain.entities.sensor import Sensor


room = Room()
vertix1 = (0, 0)
vertix2 = (0, 4)
vertix3 = (3, 3.5)
vertix4 = (4, 0)

vertices = [vertix1, vertix2, vertix3, vertix4]
room.set_vertixes(vertices = vertices)
sensor1 = Sensor(x = 2, y = 1, z = 1.5)
sensor2 = Sensor(x = 2, y = 1, z = 1.5)
sensor3 = Sensor(x = 3, y = 2, z = 1.5)
sensor4 = Sensor(x = 2, y = 3, z = 1.5)
sensors = [sensor1, sensor2, sensor3, sensor4]
room.set_sensors(sensors = sensors)
room.create_grid()
room.plot_grid()

# %%

room.compute_visions()
room.sensors[3].plot_vision()

# %%

def decay(x: float, y: float) -> float:
    r = pow(x*x + y*y, 1/2)

    result = pow(np.e, -pow(r, 2)/ 1.5)
    if 1/result > 100:
        return None
    else:
        return 400/result

# %%

import pandas as pd
import numpy as np

data = pd.DataFrame(columns = np.unique(room.y), index = np.unique(room.x))

# %%


for x, y in zip(room.x, room.y):
    data.loc[x, y] = decay(x, y)

# %%
import plotly.graph_objects as go

import pandas as pd

fig = go.Figure(data=[go.Surface(z=data, colorscale = "twilight")])
fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                  highlightcolor="limegreen", project_z=True))
fig.update_layout(title='Mt Bruno Elevation', autosize=False,
                  width=500, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))
fig.show()
# %%
