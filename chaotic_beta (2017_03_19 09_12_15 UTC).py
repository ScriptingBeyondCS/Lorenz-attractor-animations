import numpy as np
from scipy import integrate

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

import time
# import os, sys
# # 'C:\Program Files\ImageMagick'
# # ff_path = os.path.join('C:/', 'Program Files', 'ImageMagick-7.0.5-Q16', 'ffmpeg.exe')
# # plt.rcParams['animation.ffmpeg_path'] = ff_path
# # if ff_path not in sys.path: sys.path.append(ff_path)

# # imgk_path = os.path.join('C:/', 'Program Files', 'ImageMagick-7.0.5-Q16', 'convert.exe')
# # plt.rcParams['animation.convert_path'] = imgk_path
# # if ff_path not in sys.path: sys.path.append(imgk_path)

# plt.rcParams['animation.ffmpeg_path'] = r'C:\ffmpeg'

N_trajectories = 30



def lorentz_deriv(coord, t0, sigma=10., beta=8./3, rho=28.0):
    """Compute the time-derivative of a Lorentz system."""
    x = coord[0]
    y = coord[1]
    z = coord[2]
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


# Choose random starting points, uniformly distributed from -15 to 15
np.random.seed(1)
x0 = -15 + 30 * np.random.random((N_trajectories, 3))
# print(x0)
sigma = -15 + 30 * np.random.random((N_trajectories, 1))
# print(sigma)
beta = -5 + 8 * np.random.random((N_trajectories, 1))
rho = -15 + 30 * np.random.random((N_trajectories, 1))



# Solve for the trajectories
t = np.linspace(0, 1, 6000)
# trajectory_list = []
# for i in range(N_trajectories):
#     parameters = (sigma[i],beta[i],rho[i])
#     x0i = x0[0]
#     trajectory_list.append([integrate.odeint(lorentz_deriv,x0i,t,args=parameters)])
# x_t = np.asarray(trajectory_list)
x_t = np.asarray([integrate.odeint(lorentz_deriv, (1,1,1), t, args=(10., beta[k][0], 28.0))
                  for k in range(N_trajectories)])

# Set up figure & 3D axis for animation
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('off')

# choose a different color for each trajectory
colors = plt.cm.jet(np.linspace(0, 1, N_trajectories))

# set up lines and points
lines = sum([ax.plot([], [], [], '-', c=c)
             for c in colors], [])
pts = sum([ax.plot([], [], [], 'o', c=c)
           for c in colors], [])

# prepare the axes limits
ax.set_xlim((-25, 25))
ax.set_ylim((-35, 35))
ax.set_zlim((5, 100))

# set point-of-view: specified by (altitude degrees, azimuth degrees)
ax.view_init(30, 0)

# initialization function: plot the background of each frame
def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])
        line.set_3d_properties([])

        pt.set_data([], [])
        pt.set_3d_properties([])
    return lines + pts

# animation function.  This will be called sequentially with the frame number
def animate(i):
    # we'll step two time-steps per frame.  This leads to nice results.
    steps = 4
    i = (steps * i) % x_t.shape[1]
    for line, pt, xi in zip(lines, pts, x_t):
        x, y, z = xi[:i].T
        line.set_data(x, y)
        line.set_3d_properties(z)

        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])
    ax.view_init(30, 0.3 * i)
    fig.canvas.draw()
    return lines + pts
start_time = time.time()
# instantiate the animator.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=2000, interval=30, blit=True)


mywriter = animation.FFMpegWriter()
anim.save('chaotic_beta.mp4', writer='ffmpeg', fps=60, extra_args=['-vcodec', 'libx264'], bitrate=4000)
print("saved the file!")
plt.show()
print("runtime is", time.time()-start_time)