import math

#curvature of a pose and a point
#aka, finds the equation of the circle given 2 points and the tangent line at one point
#useful in robotics algorithms involving dynamic carrot point following
def circle_equation(x1, y1, x2, y2, angle):
    m = 1 / math.tan(angle)
    if((y2 - y1) / (x2 - x1) == m):
        print("inf")
        
    h_value = (m*x1**2 - m*x2**2 - m*y1**2 + 2*m*y1*y2 - m*y2**2 - 2*x1*y1 + 2*x1*y2) / (2*m*x1 - 2*m*x2 - 2*y1 + 2*y2)
    k_value = (2*m*x1*y1 - 2*m*x2*y1 + x1**2 - 2*x1*x2 + x2**2 - y1**2 + y2**2) / (2*m*x1 - 2*m*x2 - 2*y1 + 2*y2)

    r_squared = ((-x1**2 + 2*x1*x2 - x2**2 - y1**2 + 2*y1*y2 - y2**2)**2 + (m*x1**2 - 2*m*x1*x2 + m*x2**2 + m*y1**2 - 2*m*y1*y2 + m*y2**2)**2) / (4*(m*x1 - m*x2 - y1 + y2)**2)
    return (h_value, k_value, r_squared**0.5)


x1, y1 = 12, 23  # First point on the circle
x2, y2 = 32, 41  # Second point on the circle
angle = math.pi / 3 #heading of the robot (or something else) on the first point on the circle

# Get the equation of the circle
h, k, r = circle_equation(x1, y1, x2, y2, angle)
print(f"Center: ({h}, {k}), Radius: {r}")