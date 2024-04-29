import numpy as np
import matplotlib.pyplot as plt

# Time parameters
t = np.linspace(0, 1, 500)

acc_time = 0.2 # Time for acceleration
dec_time = 0.2  # Time for deceleration
const_time = 1 - (acc_time + dec_time)  # Time for constant velocity

T = 1

s_curve = np.piecewise(t, 
                       [t < acc_time, 
                        (t >= acc_time) & (t < acc_time + const_time), 
                        (t >= acc_time + const_time) & (t < T)],
                       [lambda t: np.sin((np.pi / 2) * (t / acc_time)), 
                        1,  # Constant phase at the peak of the sine wave
                        lambda t: np.sin((np.pi / 2) * ((T - t) / dec_time))])

plt.figure(figsize=(10, 6))
plt.plot(t, s_curve, label='Skibidi')
plt.title('Sin MP')
plt.xlabel('t val')
plt.ylabel('voltage (normalized)')
plt.grid(True)
plt.legend()
plt.show()