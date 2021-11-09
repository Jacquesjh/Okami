# %%
from typing import Any, Dict, List, Tuple

import numpy as np
from pydantic import BaseModel

class Sensor(BaseModel):

    x: float
    y: float
    z: float = 0
    
    vision  : Optional[List[List[float]]]
    
# %%


sensor = Sensor(location = (0.5, 1.5))

# %%
