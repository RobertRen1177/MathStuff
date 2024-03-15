import numpy as np
import matplotlib.pyplot as plt

# Time parameters
t = np.linspace(0, 30, 500)

acc_time = 8 # Time for acceleration
const_time = 10  # Time for constant velocity
dec_time = 8  # Time for deceleration
T = acc_time + const_time + dec_time

s_curve = np.piecewise(t, 
                       [t < acc_time, 
                        (t >= acc_time) & (t < acc_time + const_time), 
                        (t >= acc_time + const_time) & (t < T)],
                       [lambda t: np.sin((np.pi / 2) * (t / acc_time)), 
                        1,  # Constant phase at the peak of the sine wave
                        lambda t: np.sin((np.pi / 2) * ((T - t) / dec_time))])

plt.figure(figsize=(10, 6))
plt.plot(t, s_curve, label='Skibidi')
plt.title('I have to be clean now')
plt.xlabel('Time (s)')
plt.ylabel('Position (normalized)')
plt.grid(True)
plt.legend()
plt.show()