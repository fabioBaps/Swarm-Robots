################## IMPORTS
from numpy import array

def phi(y, dest, dt, f):
    k1 = f(y, dest)
    k2 = f(y + dt/2*k1, dest)
    k3 = f(y + dt/2*k2, dest)
    k4 = f(y + dt*k3, dest)
    return 1/6*(k1 + 2*k2 + 2*k3 + k4)

################## RUNGE KUTTA 4TH ORDER METHOD
def oneStepMethod(y0, dest, n, f):
    y_n = [array(y0)]
    h = 1/n
    for _ in range(n):
        y_n.append(y_n[-1] + h*phi(y_n[-1], dest, h, f))
    return y_n[-1]