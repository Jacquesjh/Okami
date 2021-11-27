
from typing import Any, Dict, List

import numpy as np
from pydantic import BaseModel

class Source(BaseModel):
    
    value: float
    x    : float
    y    : float
    z    : float = 0
    
    vision  : Any
    

    def read_value(self):
        pass

    
    def _decay(self, x: float, y: float) -> float:

        distance = pow(pow(x - self.x, 2) + pow(y - self.y, 2), 1/2)
        result   = self.value*pow(np.e, -pow(distance, 2)/ 1.5)

        if result > 10000:
            return None
        
        else:
            return result


    def compute_vision(self, x: List[float], y: List[float]) -> None:

        data = pd.DataFrame(columns = np.unique(y), index = np.unique(x))

        for x_value, y_value in zip(x, y):
            data.loc[x_value, y_value] = self._decay(x_value, y_value)

        self.vision = data

      
    def plot_vision(self) -> None:

        X, Y = np.meshgrid(self.vision.index.tolist(), self.vision.columns)
        
        fig = go.Figure(data=[go.Surface(x = np.array(self.vision.index.tolist()), y = np.array(self.vision.columns), z = self.vision.T.values,
                                         colorscale = "viridis", opacity = 0.75)])

        # fig = go.Figure(data=[go.Surface(z = self.vision.values,
        #                                  colorscale = "viridis", opacity = 0.75)])
        fig.update_traces(contours_z = dict(show = True, usecolormap = True,
                                            highlightcolor = "limegreen", project_z = True))

        fig.add_scatter3d(x = [self.x], y = [self.y], z = [self.value], mode = "markers")

        fig.update_layout(title = "Sensor Ambient Vision", autosize = False,
                          margin = dict(l = 50, r = 50, b = 10, t = 50))
        fig.show()
