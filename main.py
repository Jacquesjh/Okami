
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