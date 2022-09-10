
class Source:

    value: float
    x    : float
    y    : float
    z    : float


    def __init__(self, value: float, x: float, y: float) -> None:
        self.value = value
        self.x     = x
        self.y     = y
        self.z     = 0