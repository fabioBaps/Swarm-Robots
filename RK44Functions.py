################## IMPORTS
from numpy import array

def phi(coordsVels, dest, h, f):
    k1 = f(coordsVels, dest)
    k2 = f(coordsVels + (h/2)*k1, dest)
    k3 = f(coordsVels + (h/2)*k2, dest)
    k4 = f(coordsVels + h*k3, dest)
    return 1/6*(k1 + 2*k2 + 2*k3 + k4)

################## RUNGE KUTTA 4TH ORDER METHOD
def oneStepMethod(c0v0, dest, n, f):
    y_n = [array(c0v0)]
    h = 1/n
    for _ in range(n):
        y_n.append(y_n[-1] + h*phi(y_n[-1], dest, h, f))
    return y_n[-1]