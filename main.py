# %%

import plotly.express as px
import numpy as np

from okami.demo import Demo
from okami.src.domain.entities.sensor import Sensor

vertix1 = (0, 0)
vertix2 = (0, 3)
vertix3 = (4, 5)
vertix4 = (5, 0)

vertices = [vertix1, vertix2, vertix3, vertix4]

cache_size = 10

sensor1 = Sensor(id = "sensors_1", x = 0.5, y = 0.5, z = 1.5, cache_size = cache_size)
sensor2 = Sensor(id = "sensors_2", x = 1.25, y = 3, z = 1.5, cache_size = cache_size)
sensor3 = Sensor(id = "sensors_3", x = 3.25, y = 4, z = 1.5, cache_size = cache_size)
sensor4 = Sensor(id = "sensors_4", x = 0.75, y = 3.75, z = 1.5, cache_size = cache_size)
sensors = [sensor1, sensor2, sensor3, sensor4]

demo = Demo(vertices = vertices, sensors = sensors, res = 0.25, num_sources = 2, time_steps = 60)
# %%


for i in range(30):
    demo.run_cycle()

# %%
def variance(sensors):
    rows      = int(np.math.factorial(len(sensors))/(np.math.factorial(2)*np.math.factorial(len(sensors) - 2)))
    variances = np.zeros(shape = (rows, 2))

    temp  = sensors.copy()
    index = 0

    for sensor in sensors:
        aux = temp.copy()
        aux.remove(sensor)
        
        for pair_sensor in aux:
            mean_variance = (pow(sensor.cache - pair_sensor.cache, 2)/2).mean()
            distance      = pow(pow(sensor.x - pair_sensor.x, 2) + pow(sensor.y - pair_sensor.y, 2) + pow(sensor.z - pair_sensor.z, 2), 0.5)

            variances[index, 0] = distance
            variances[index, 1] = mean_variance
            index += 1

        temp.remove(sensor)
        
    fig = px.scatter(x = variances[:, 0], y = variances[:, 1])
    fig.show()

    for sensor in sensors:
        print(sensor.cache)

variance(sensors = demo.sensors)

# %%

xr = room.x
yr = room.y


def create_grid(x_grid, y_grid, coord_source, values_source):
    
    instant = []

    for value, x, y in zip(values_source, coord_source[0], coord_source[1]):
        
        data = pd.DataFrame(columns = np.unique(y_grid), index = np.unique(x_grid))

        for xg, yg in zip(x_grid, y_grid):
            dist = pow(pow(xg - x, 2) + pow(yg - y, 2), 0.5)
            data.loc[xg, yg] = value*pow(np.e, -pow(dist, 2)/1.5)
        
        instant.append(data)

    return instant

grid_values = create_grid(xr, yr, coords, values)

# %%
i = 0

for grid in grid_values:

    fig = go.Figure(data=[go.Surface(x = grid.index.tolist(), y = grid.columns, z = grid.T.values,
                                            colorscale = "viridis", cmin = 0, cmax = max(values))])
    fig.update_traces(contours_z = dict(show = True, usecolormap = True,
                                        highlightcolor = "limegreen", project_z = True))

    fig.update_layout(autosize = False, margin = dict(l = 50, r = 50, b = 10, t = 50))
    fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"})

    fig.data[0].colorbar.x = -0.1

    fig.update_layout(scene = dict(xaxis = dict(showbackground = False, showticklabels = False),
                                   yaxis = dict(showbackground = False, showticklabels = False),
                                   zaxis = dict(nticks = 10, range=[0, max(values)], showbackground = False, showticklabels = False)))

    if len(str(i)) == 1:
        ind = "00" + str(i)

    if len(str(i)) == 2:        
        ind = "0" + str(i)

    if len(str(i)) == 3:
        ind = str(i)
   
    fig.write_image(f"images/fig{ind}.png")

    print(ind)
    i += 1

# %%

import os
import moviepy.video.io.ImageSequenceClip

image_folder = "C:/Users/Joao/Okami/okami/images"
fps = 40

image_files = [image_folder + '/' + img for img in os.listdir(image_folder) if img.endswith('.png')]
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps = fps)
clip.write_videofile('C:/Users/Joao/Okami/okami/movie.mp4', fps = fps)  

# %%










# %%


def variance(sensors):
    rows      = int(np.math.factorial(len(sensors))/(np.math.factorial(2)*np.math.factorial(len(sensors) - 2)))
    variances = np.zeros(shape = (rows, 2))

    temp  = sensors.copy()
    index = 0

    for sensor in sensors:
        aux = temp.copy()
        aux.remove(sensor)
        
        for pair_sensor in aux:
            mean_variance = (pow(sensor.cache - pair_sensor.cache, 2)/2).mean()
            distance      = pow(pow(sensor.x - pair_sensor.x, 2) + pow(sensor.y - pair_sensor.y, 2) + pow(sensor.z - pair_sensor.z, 2), 0.5)

            variances[index, 0] = distance
            variances[index, 1] = mean_variance
            index += 1

        temp.remove(sensor)
        
    fig = px.scatter(x = variances[:, 0], y = variances[:, 1])
    fig.show()