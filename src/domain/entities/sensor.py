# %%
from typing import Any, Dict, List, Tuple

import numpy as np
from pydantic import BaseModel

class Sensor(BaseModel):

    location: Tuple[float, float]
    _search : List[List[float]]
    
# %%


sensor = Sensor(location = (0.5, 1.5))

# %%
