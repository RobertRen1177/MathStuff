import math
#rotates line around a pivot point on the line by theta degrees
def rotate_line(m, b, x0, y0, theta):
    # Convert theta from degrees to radians
    theta_rad = math.radians(theta)
    
    cos_theta = math.cos(theta_rad)
    sin_theta = math.sin(theta_rad)
    
    # Rotate the point where the line intersects the y-axis (0, b)
    x1, y1 = 0 - x0, b - y0  # Translate to origin
    x1_rotated = x1 * cos_theta - y1 * sin_theta
    y1_rotated = x1 * sin_theta + y1 * cos_theta
    x1_rotated += x0  # Translate back
    y1_rotated += y0
    print(x1_rotated, y1_rotated)
    
    x2_rotated = x0  #shitty code ik bro
    y2_rotated = y0
    
    # Calculate new slope and y-intercept
    if(x2_rotated - x1_rotated == 0):
        return 99999999, y1_rotated - 99999999 * x1_rotated #scuffed infinity
    new_m = (y2_rotated - y1_rotated) / (x2_rotated - x1_rotated)
    new_b = y1_rotated - new_m * x1_rotated
    
    return new_m, new_b

m, b = 1, 2  
x0, y0 = 3, 5
theta = -30
print(rotate_line(m, b, x0, y0, theta))