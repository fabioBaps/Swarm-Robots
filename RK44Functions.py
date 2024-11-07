################## IMPORTS
from numpy import array

def phi(y, dest, h, f, angle):
    k1 = f(y, dest, angle)
    k2 = f(y + (h/2)*k1, dest, angle)
    k3 = f(y + (h/2)*k2, dest, angle)
    k4 = f(y + h*k3, dest, angle)
    return 1/6*(k1 + 2*k2 + 2*k3 + k4)

################## RUNGE KUTTA 4TH ORDER METHOD
def oneStepMethod(y0, dest, n, f, angle):
    y_n = [array(y0)]
    h = 1/n
    for _ in range(n):
        y_n.append(y_n[-1] + h*phi(y_n[-1], dest, h, f, angle))
    return y_n[-1]