import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

class BezierCurve:
    def __init__(self, P0, P1, P2, P3, numpoints):
        self.P0 = np.array(P0)
        self.P1 = np.array(P1)
        self.P2 = np.array(P2)
        self.P3 = np.array(P3)
        self.points = np.array([self.P0])  
        self.left = np.empty((0, 2))       
        self.right = np.empty((0, 2))      
        self.discretize(numpoints)

    def bezier_curve(self, t):
        return (1 - t)**3 * self.P0 + 3 * (1 - t)**2 * t * self.P1 + 3 * (1 - t) * t**2 * self.P2 + t**3 * self.P3

    def bezier_derivative(self, t):
        return 3 * (1 - t)**2 * (self.P1 - self.P0) + 6 * (1 - t) * t * (self.P2 - self.P1) + 3 * t**2 * (self.P3 - self.P2)

    def arc_length(self, t):
        derivative = self.bezier_derivative(t)
        return np.linalg.norm(derivative)

    def compute_total_length(self):
        total_length, _ = quad(self.arc_length, 0, 1)
        return total_length

    def find_t_for_length(self, target_length, total_length):
        left, right = 0, 1
        while right - left > 1e-6:
            mid = (left + right) / 2.0
            current_length, _ = quad(self.arc_length, 0, mid)
            if current_length < target_length:
                left = mid
            else:
                right = mid
        return (left + right) / 2.0

    def get_norm_norm(self, t, direction, strength):
        derivative = self.bezier_derivative(t)
        norm_derivative = derivative / np.linalg.norm(derivative)
        if(direction < 0):
            return np.array([-norm_derivative[1], norm_derivative[0]])
        return np.array([norm_derivative[1], -norm_derivative[0]])

    def discretize(self, num_points):
        total_length = self.compute_total_length()

        for i in range(1, num_points):
            target_length = (i / num_points) * total_length
            t = self.find_t_for_length(target_length, total_length)
            point = self.bezier_curve(t)

            # Append points to arrays
            self.points = np.vstack([self.points, point])
            self.left = np.vstack([self.left, self.get_norm_norm(t, 1, 1.5) + self.bezier_curve(t)])
            self.right = np.vstack([self.right, self.get_norm_norm(t, -1, 1.5) + self.bezier_curve(t)])

        # Add the last point
        self.points = np.vstack([self.points, self.P3])
    
    def project_vector_mag(self, v, u):
        return abs(np.dot(v, u) / np.linalg.norm(u))
    
    def sortConePointsHelper(self, list : np.array):
        sorted_cone_list = [] #this is the list that will contain all the cone points, will be sorted at the end
        for cone_point in list: #iterate through all cone points, find the closest point on the center line then project
            minDistance = 99999999
            minDistanceIndex = -1
            otherEndIndex = -1
            for i in range(1, len(self.points) - 1):
                midpoint = self.points[i]
                if(minDistance > np.linalg.norm(cone_point - midpoint)):
                    minDistance = np.linalg.norm(cone_point - midpoint)
                    minDistanceIndex = i
                    if(np.linalg.norm(cone_point - self.points[i + 1]) > np.linalg.norm(cone_point - self.points[i - 1])):
                        otherEndIndex = i - 1
                    else:
                        otherEndIndex = i + 1
            
            if(minDistanceIndex > otherEndIndex):
                comp = self.project_vector_mag(cone_point - self.points[otherEndIndex], self.points[minDistanceIndex] - self.points[otherEndIndex])
                sorted_cone_list.append((otherEndIndex, comp))
            else:
                comp = self.project_vector_mag(cone_point - self.points[minDistanceIndex], self.points[otherEndIndex] - self.points[minDistanceIndex])
                sorted_cone_list.append((minDistanceIndex, comp))
            
        #sort the cone list
        return sorted(sorted_cone_list, key=lambda x: (x[0], x[1]))

            

                


    def plot(self, num_curve_points=100):
        # Plot the original Bézier curve
        t_values = np.linspace(0, 1, num_curve_points)
        curve_points = np.array([self.bezier_curve(t) for t in t_values])

        plt.plot(curve_points[:, 0], curve_points[:, 1], label="Bézier Curve", color='blue')

        plt.scatter(self.points[:, 0], self.points[:, 1], color='red', label="Discretized Points", zorder=5)
        plt.scatter(self.left[:, 0], self.left[:, 1], color='green', label="Left Points", zorder=5)
        plt.scatter(self.right[:, 0], self.right[:, 1], color='orange', label="Right Points", zorder=5)

        plt.legend()
        plt.title("Cubic Bézier Curve and Discretized Points")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        plt.axis("equal")
        plt.show()
    

# Example usage
if __name__ == "__main__":
    P0 = [0, 0]
    P1 = [7, 30]
    P2 = [41, -3]
    P3 = [44, 27]

    bezier = BezierCurve(P0, P1, P2, P3, 10)
    bezier.plot(num_curve_points=100)
    bezier.sortConePointsHelper([(13, 15)])