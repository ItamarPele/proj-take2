from server.back_end_algo.modulo_int import *


class Data:
    def __init__(self, x, y):
        self.x = MD(x)
        self.y = MD(y)

    def __repr__(self):
        return f"(x:{self.x}, y:{self.y})"

    @classmethod
    def from_repr(cls, repr_str):
        # Assuming repr_str is in the format "(x:value_x, y:value_y)"
        parts = repr_str.strip('()').split(', ')
        x = int(parts[0].split(':')[1])
        y = int(parts[1].split(':')[1])
        return cls(x, y)


# function to interpolate the given data points
# using Lagrange's formula
# xi -> corresponds to the new data point
# whose value is to be obtained
# n -> represents the number of known data points
def interpolate(f: list, xi: MD, n: MD) -> MD:
    # Initialize result
    result = MD(0)
    for i in range(n.value):

        # Compute individual terms of above formula
        term = f[i].y
        # print(n.value - i)
        for j in range(n.value):
            if j != i:
                term = term * (xi - f[j].x) / (f[i].x - f[j].x)

        # Add current term to result
        result += term

    return result
