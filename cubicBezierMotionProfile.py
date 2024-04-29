import numpy as np
import matplotlib.pyplot as plt
import math
import bezierlength
def cubic_bezier(t, P):
    """Calculate position on a cubic Bezier curve."""
    return (1 - t)**3 * P[0] + 3 * (1 - t)**2 * t * P[1] + 3 * (1 - t) * t**2 * P[2] + t**3 * P[3]

def cubic_bezier_first_derivative(t, P):
    return 3 * (1 - t)**2 * (P[1] - P[0]) + 6 * (1 - t) * t * (P[2] - P[1]) + 3 * t**2 * (P[3] - P[2])

def cubic_bezier_second_derivative(t, P):
    return 6 * (1 - t) * (P[2] - 2 * P[1] + P[0]) + 6 * t * (P[3] - 2 * P[2] + P[1])

def curvature(t, P):
    d1 = cubic_bezier_first_derivative(t, P)
    d2 = cubic_bezier_second_derivative(t, P)
    numerator = np.abs(d1[0] * d2[1] - d1[1] * d2[0])
    denominator = (d1[0]**2 + d1[1]**2)**1.5
    return numerator / max(denominator, 1e-6) 


P = [np.array([-2.5, -4.14]), np.array([-3.8, 24.4]), np.array([33.6, 23.3]), np.array([33.8, -3.6])]  # Control points
curve_length = bezierlength.bezier_arclength(P[0], P[1], P[2], P[3])
deltaDistance = curve_length / 200
totalDistanceTravelled = 0
a_max = 33 # Maximum acceleration
deaccel_max = 10
v_max = 50  # Maximum velocity
t = 0

v_forward = []


v = 0  # Start at rest
while(t <= 1):
    first_deriv = cubic_bezier_first_derivative(t, P)
    
    #distance / velocity, to estimate t
    t += deltaDistance / math.sqrt(first_deriv[0] * first_deriv[0] + first_deriv[1] * first_deriv[1])
    
    k = curvature(t, P)
    v_curvature = math.sqrt(0.8 * 9.8 * 1.0/k) #sqrt(urg) to not slip around corners
    v_max_accel = math.sqrt(v * v + 2 *a_max * deltaDistance) #cant accelerate too fast
    v_max_deaccel = math.sqrt(2 * deaccel_max * (curve_length - totalDistanceTravelled))#deaccleration phase, have to be able to slow down to 0 before the end at a maximum acceleration
    v = max(min(v_max, v_curvature, v_max_accel, v_max_deaccel), math.sqrt(max(v * v - 2 * deaccel_max * deltaDistance, 0))) #min to find the speed
    v_forward.append(v)
    totalDistanceTravelled += deltaDistance #update distance
    
plt.figure(figsize=[12, 6])
plt.plot(v_forward)
plt.legend()
plt.grid(True)
plt.show()