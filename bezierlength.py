import numpy as np
import time
import math
import random
begin = time.time()
#Legendre-Gauss arc length approximation for a cubic bezier
#for motion profiling initial distnace
P0, P1, P2, P3 = np.array([-12, -36]), np.array([-12, -52]), np.array([-26, -36]), np.array([-36, -60])
60
def derivative_cubic_bezier(t, P0, P1, P2, P3):
    return 3*(1-t)**2 * (P1 - P0) + 6*(1-t)*t * (P2 - P1) + 3*t**2 * (P3 - P2)

def cubic_bezier_curve(t, P0, P1, P2, P3):
    return (1-t)**3 * P0 + 3 * (1-t)**2 * t * P1 + 3 * (1-t) * t**2 * P2 + t**3 * P3

coefficent_24 = [
    (0.1279381953467522, -0.0640568928626056),
    (0.1279381953467522, 0.0640568928626056),
    (0.1258374563468283, -0.1911188674736163),
    (0.1258374563468283, 0.1911188674736163),
    (0.1216704729278034, -0.3150426796961634),
    (0.1216704729278034, 0.3150426796961634),
    (0.1155056680537256, -0.4337935076260451),
    (0.1155056680537256, 0.4337935076260451),
    (0.1074442701159656, -0.5454214713888396),
    (0.1074442701159656, 0.5454214713888396),
    (0.0976186521041139, -0.6480936519369755),
    (0.0976186521041139, 0.6480936519369755),
    (0.0861901615319533, -0.7401241915785544),
    (0.0861901615319533, 0.7401241915785544),
    (0.0733464814110803, -0.8200019859739029),
    (0.0733464814110803, 0.8200019859739029),
    (0.0592985849154368, -0.8864155270044011),
    (0.0592985849154368, 0.8864155270044011),
    (0.0442774388174198, -0.9382745520027328),
    (0.0442774388174198, 0.9382745520027328),
    (0.0285313886289337, -0.9747285559713095),
    (0.0285313886289337, 0.9747285559713095),
    (0.0123412297999872, -0.9951872199970213),
    (0.0123412297999872, 0.9951872199970213),
]


def integrand(t, P0, P1, P2, P3):
    derivative = derivative_cubic_bezier(t, P0, P1, P2, P3)
    return np.sqrt(np.sum(derivative**2))

def bezier_arclength(P0, P1, P2, P3, t1=0, t2=1):
    begin = time.time()
    n = len(coefficent_24)
    length = 0
    for i in range(n):
        t = 0.5 * (coefficent_24[i][1] + 1) * (t2 - t1) + t1
        weight = coefficent_24[i][0] * (t2 - t1) / 2
        length += weight * integrand(t, P0, P1, P2, P3)
    return length

def distance(P0, P1):
    return math.sqrt((P0[0] - P1[0]) * (P0[0] - P1[0]) +  (P0[1] - P1[1]) * (P0[1] - P1[1]))

def bezier_real_arc_len(P0, P1, P2, P3, t1 = 0, t2 = 1):
    begin = time.time()
    counter = t1
    prevPoint = cubic_bezier_curve(counter, P0, P1, P2, P3)
    total_distance = 0
    while(counter < t2):
        counter += 1/100
        current_point = cubic_bezier_curve(counter, P0, P1, P2, P3)
        total_distance += distance(prevPoint, current_point)
        prevPoint = current_point
    return total_distance
        

arc_length = bezier_arclength(P0, P1, P2, P3, 0.5, 0.7)
real_arc_length = bezier_real_arc_len(P0, P1, P2, P3, 0.5, 0.7)
print(arc_length, real_arc_length)