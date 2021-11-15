
from typing import Any, Dict, List, Tuple, Optional

import numpy as np
from pydantic import BaseModel
import pandas as pd
from pandas import DataFrame
import plotly.graph_objects as go


class Sensor(BaseModel):

    value: float = 400

    x: float
    y: float
    z: float = 0
    
    vision  : Any
    

    def read_value(self):
        pass

    
    def decay(self, x: float, y: float) -> float:

        distance = pow(pow(x - self.x, 2) + pow(y - self.y, 2), 1/2)
        result   = self.value/pow(np.e, -pow(distance, 2)/ 1.5)
        if result > 10000:
            return None
        else:
            return result


    def compute_vision(self, x: List[float], y: List[float]):
        
        data = pd.DataFrame(columns = np.unique(y), index = np.unique(x))

        for x_value, y_value in zip(x, y):
            data.loc[x_value, y_value] = self.decay(x_value, y_value)
        
        self.vision = data

      
    def plot_vision(self):

        fig = go.Figure(data=[go.Surface(z = self.vision, colorscale = "viridis")])
        fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                        highlightcolor="limegreen", project_z=True))
        fig.update_layout(title='Sensor Ambient Vision', autosize=False,
                        width=500, height=500,
                        margin=dict(l=65, r=50, b=65, t=90))
        fig.show()