
from pydantic import BaseModel, Field


class Variogram(BaseModel):

    nugget : float = Field(gt = 0)
    sill   : float = Field(gt = 0)
    e_range: float = Field(gt = 0)

    
    def variance(self, distance: float) -> float:
        y = self.nugget + self.sill(1.5*(distance/self.e_range) - 0.5*pow(distance/self.e_range, 3))
        return y