
import random
from typing import List, Tuple

from src.domain.entities.room import Room


def ajust_sensors(room: Room, coord: Tuple[float, float], value: float) -> None:

    for sensor in room.sensors:
        
        distance = pow(pow(coord[0] - sensor.x, 2) + pow(coord[1] - sensor.y, 2), 1/2)
        sensor.value = value*pow(np.e, -pow(distance, 2)/ 1.5)


def random_timeseries(initial_value: float, volatility: float, count: int) -> List[float]:
    
    time_series = [initial_value, ]
    
    for i in range(count):
        time_series.append(time_series[-1] + initial_value*random.gauss(0, 1)*volatility)
    
    return time_series


def standardize(timeseries: List[float]) -> List[float]:

    timeseries = [num + abs(min(timeseries)) for num in timeseries]
    timeseries = [num/max(timeseries) for num in timeseries]
    
    return timeseries


def artificial_source() -> List[Tuple[float, float], float]:

    xseries = random_timeseries(1.25, 0.5, 1000)
    xseries = standardize(xseries)

    yseries = random_timeseries(1.25, 0.5, 1000)
    yseries = standardize(yseries)

    values  = random_timeseries(1.25, 0.25, 1000)
    values  = standardize(values)
    values  = [2000*v + 500 for v in values]

    return (xseries, yseries), values
