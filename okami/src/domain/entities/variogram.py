
from pydantic import BaseModel, Field
import numpy as np


class Variogram(BaseModel):

    nugget : float = Field(gt = 0)
    sill   : float = Field(gt = 0)
    e_range: float = Field(gt = 0)

    
    def variance(self, distance: float) -> float:
        self.nugget = 50000
        self.sill   = 1500
        
        y = self.nugget + self.sill*(1.5*(distance/self.e_range) - 0.5*pow(distance/self.e_range, 3)) #   ----- ESFERICO

        # y = self.nugget + self.sill*(1 - pow(np.e, (-3*pow(distance/self.e_range, 2))))                #  ----- GAUSSIANO

        # y = self.nugget + self.sill*(1 - pow(np.e, -3*distance/self.e_range))                         #   ----- EXPONENCIAL


        return y