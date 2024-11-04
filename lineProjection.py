import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import random

class BezierCurve:
    def __init__(self, P0, P1, P2, P3, numpoints, numcones):
        self.P0 = np.array(P0)
        self.P1 = np.array(P1)
        self.P2 = np.array(P2)
        self.P3 = np.array(P3)
        self.points = np.array([self.P0])  
        self.left = np.empty((0, 2))       
        self.right = np.empty((0, 2))      
        self.discretize(numpoints, numcones)

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

    def discretize(self, num_points, num_cones):
        total_length = self.compute_total_length()

        for i in range(1, num_points):
            target_length = (i / num_points) * total_length
            t = self.find_t_for_length(target_length, total_length)
            point = self.bezier_curve(t)

            # Append points to arrays
            self.points = np.vstack([self.points, point])
        for i in range(1, num_cones):
            target_length = (i / num_cones) * total_length
            t = self.find_t_for_length(target_length, total_length)
            point = self.bezier_curve(t)
            self.left = np.vstack([self.left, self.get_norm_norm(t, 1, 1.5) + point])
            self.right = np.vstack([self.right, self.get_norm_norm(t, -1, 1.5) + point])

    
    def index_wrapper(self, index, len_list):
        if(index >= 0 and index < len_list):
            return index
        if(index >= len_list):
            return index - (len_list)
        return len_list + index
    

    
    def project_vector_mag(self, v, u):
        return abs(np.dot(v, u) / np.linalg.norm(u))
    
    def sort_cone_points_helper(self, list : np.array):
        sorted_cone_list = [] #this is the list that will contain all the cone points, will be sorted at the end
        for cone_point in list: #iterate through all cone points, find the closest point on the center line then project
            minDistance = 99999999
            minDistanceIndex = -1
            otherEndIndex = -1
            if(cone_point[0] == 2.582099133578116):
                print("stop")
            for i in range(0, len(self.points)):
                midpoint = self.points[i]
                if(minDistance > np.linalg.norm(cone_point - midpoint)):
                    minDistance = np.linalg.norm(cone_point - midpoint)
                    minDistanceIndex = i
                    index_minus = self.index_wrapper(i - 1, len(self.points))
                    index_plus = self.index_wrapper(i + 1, len(self.points))
                    if(np.linalg.norm(cone_point - self.points[index_plus]) > np.linalg.norm(cone_point - self.points[index_minus])):
                        otherEndIndex = index_minus
                    else:
                        otherEndIndex = index_plus
            
            if(minDistanceIndex > otherEndIndex):
                comp = self.project_vector_mag(cone_point - self.points[otherEndIndex], self.points[minDistanceIndex] - self.points[otherEndIndex])
                sorted_cone_list.append((cone_point, otherEndIndex, comp))
            else:
                comp = self.project_vector_mag(cone_point - self.points[minDistanceIndex], self.points[otherEndIndex] - self.points[minDistanceIndex])
                sorted_cone_list.append((cone_point, minDistanceIndex, comp))
            
        #sort the cone list
        return  [item[0] for item in sorted(sorted_cone_list, key=lambda x: (x[1], x[2]))]

    
    def test(self):
        original_left_list, original_right_list = self.left, self.right
        print("Original Lists: ")
        print("Left List: ")
        for point in self.left:
            print("(" + str(point[0]) + ", " + str(point[1]) + ")")
        print()
        print("Right List: ")
        for point in self.right:
            print("(" + str(point[0]) + ", " + str(point[1]) + ")")
        
        #np.random.shuffle(self.left)
        #np.random.shuffle(self.right)
        print()
        print("Shuffled Left List: ")
        for point in self.left:
            print("(" + str(point[0]) + ", " + str(point[1]) + ")")
        print()
        print("Shuffled Right List: ")
        for point in self.right:
            print("(" + str(point[0]) + ", " + str(point[1]) + ")")
        
        sorted_left_list, sorted_right_list = self.sort_cone_points_helper(self.left), self.sort_cone_points_helper(self.right)
        print()
        print("Sorted Left List: ")
        for point in sorted_left_list:
            print("(" + str(point[0]) + ", " + str(point[1]) + ")")
        print()
        print("Sorted Right List: ")
        for point in sorted_right_list:
            print("(" + str(point[0]) + ", " + str(point[1]) + ")")
        
        self.plot_points(sorted_left_list, sorted_right_list, self.left, self.right)
        #test
        for i in range(len(self.left)):
            if np.array_equal(original_left_list[i], sorted_left_list[i][0]) or np.array_equal(original_right_list[i], sorted_right_list[i][0]):
                return False
        return True

    def plot_points(self, in_order_points, in_order_points2, out_of_order_points, out_of_order_points2):
        # Create a figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        t_values = np.linspace(0, 1, 1000)
        curve_points = np.array([self.bezier_curve(t) for t in t_values])

        # Plot out-of-order points and out-of-order points 2
        ax1.scatter(*zip(*out_of_order_points), color='blue', label='Out-of-order 1')
        ax1.scatter(*zip(*out_of_order_points2), color='yellow', label='Out-of-order 2')
        ax1.set_title("Out-of-order Points")
        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")
        for idx, (x, y) in enumerate(out_of_order_points):
            ax1.annotate(str(idx), (x, y), textcoords="offset points", xytext=(5, 5), ha='center')
        for idx, (x, y) in enumerate(out_of_order_points2):
            ax1.annotate(str(idx), (x, y), textcoords="offset points", xytext=(5, -10), ha='center')  # Offset for visibility

        # Plot in-order points and in-order points 2
        ax2.scatter(*zip(*in_order_points), color='blue', label='In-order 1')
        ax2.scatter(*zip(*in_order_points2), color='yellow', label='In-order 2')
        ax2.set_title("In-order Points")
        ax2.set_xlabel("X")
        ax2.set_ylabel("Y")
        for idx, (x, y) in enumerate(in_order_points):
            ax2.annotate(str(idx), (x, y), textcoords="offset points", xytext=(5, 5), ha='center')
        for idx, (x, y) in enumerate(in_order_points2):
            ax2.annotate(str(idx), (x, y), textcoords="offset points", xytext=(5, -10), ha='center')  # Offset for visibility

        # Add legends for clarity
        ax1.legend()
        ax2.legend()
        ax1.plot(curve_points[:, 0], curve_points[:, 1], label="Bézier Curve", color='blue')
        ax1.scatter(self.points[:, 0], self.points[:, 1], color='red', label="Discretized Points", zorder=5)
        ax2.plot(curve_points[:, 0], curve_points[:, 1], label="Bézier Curve", color='blue')
        ax2.scatter(self.points[:, 0], self.points[:, 1], color='red', label="Discretized Points", zorder=5)

        # Adjust layout and show the plot
        plt.tight_layout()
        plt.show()

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
    #P0 = [0, 0]
    #P1 = [3.6, 28.4]
    #P2 = [8, 15]
    #P3 = [9, 6]

    #P0 = [0, 0]
    #P1 = [0.27, 19.42]
    #P2 = [6.7, 23.2]
    #P3 = [4.65, 3.35]

    P0 = [0, 0]
    P1 = [-6.4, 62.4]
    P2 = [88, 11.3]
    P3 = [0, 0]

    bezier = BezierCurve(P0, P1, P2, P3, 27, 40)
    print(bezier.test())
    
    