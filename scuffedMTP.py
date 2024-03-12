import pygame
import numpy as np
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
TARGET_POINT = np.array([WIDTH // 1.3, HEIGHT // 2])
R_INITIAL = 600.0
DESIRED_ANGLE = 0  # 45 degrees
BACKGROUND_COLOR = (255, 255, 255)
TARGET_COLOR = (255, 0, 0)
ROBOT_COLOR = (0, 0, 255)
CARROT_COLOR = (0, 255, 0)
AXIS_COLOR = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Initial positions
current_position = np.array([WIDTH // 4, HEIGHT // 4]) 
carrot_point = TARGET_POINT - R_INITIAL * np.array([np.cos(DESIRED_ANGLE), np.sin(DESIRED_ANGLE)])
D_INITIAL = np.linalg.norm(current_position - carrot_point) + np.linalg.norm(carrot_point - TARGET_POINT)
dragging = False  

def angle_between_vectors(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)

    angle = np.arctan2(np.sqrt(np.clip(magnitude_a**2 * magnitude_b**2 - dot_product**2, 0, None)), dot_product)

    return angle
# Function to draw axes
def draw_axes():
    # Draw horizontal line
    pygame.draw.line(screen, AXIS_COLOR, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 1)
    # Draw vertical line
    pygame.draw.line(screen, AXIS_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 1)
    # Draw arrowheads
    pygame.draw.polygon(screen, AXIS_COLOR, [(WIDTH - 10, HEIGHT // 2 - 5), (WIDTH, HEIGHT // 2), (WIDTH - 10, HEIGHT // 2 + 5)])
    pygame.draw.polygon(screen, AXIS_COLOR, [(WIDTH // 2 - 5, 10), (WIDTH // 2, 0), (WIDTH // 2 + 5, 10)])

running = True
prev_d = D_INITIAL
r = R_INITIAL

withinAngleRange = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if np.linalg.norm(current_position - np.array(event.pos)) < 20:  # 20 is the radius for click detection
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            current_position = np.array([event.pos[0], event.pos[1]])
            # Update the carrot point
            d_new = np.linalg.norm(carrot_point - current_position) + np.linalg.norm(TARGET_POINT - carrot_point)
            if(d_new > prev_d):
                continue
            angle = angle_between_vectors(TARGET_POINT - carrot_point, current_position - carrot_point)
            if(angle >= math.pi / 2):
                r *= math.pow(d_new / prev_d, 1)
                withinAngleRange = True
            else:
                r *= math.pow(d_new / prev_d, math.sin(angle))
            if withinAngleRange:
                r *= math.pow(d_new / prev_d, 1)
                
            print(d_new, prev_d, d_new / prev_d, angle)
            prev_d = d_new
            carrot_point = TARGET_POINT - r * np.array([np.cos(DESIRED_ANGLE), np.sin(DESIRED_ANGLE)])
    
    
    screen.fill(BACKGROUND_COLOR)
    draw_axes()  
    pygame.draw.circle(screen, TARGET_COLOR, TARGET_POINT, 10)  # target point
    pygame.draw.circle(screen, ROBOT_COLOR, current_position, 10)  # current poss
    pygame.draw.line(screen, CARROT_COLOR, TARGET_POINT, carrot_point, 5)  
    pygame.draw.circle(screen, CARROT_COLOR, carrot_point.astype(int), 10)  # carrot
    
    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()
