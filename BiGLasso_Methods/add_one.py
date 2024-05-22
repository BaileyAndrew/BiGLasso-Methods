import matlab.engine
import os

eng = matlab.engine.start_matlab()
path = os.path.dirname(os.path.abspath(__file__))
eng.addpath(
    f'{path}/add_one'
)



def add_one_python(x: float) -> float:
    """
    This is a troubleshooting function, to test whether you can correctly
    hook into matlab.
    """
    x = matlab.double([x])
    return eng.add_one(x)