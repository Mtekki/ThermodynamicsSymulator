import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Grid size
Nx, Ny, Nz = 20, 20, 20
dx = dy = dz = 1.0 / Nx
alpha = 0.01
dt = 0.001
Nt = 200  # Number of time steps


# Initialize 3D temperature array
T = np.zeros((Nx, Ny, Nz))
T[Nx//2, Ny//2, Nz//2] = 100  # Heat source in the center


# Function to update temperature
def update(T):
    T_new = T.copy()
    for i in range(1, Nx - 1):
        for j in range(1, Ny - 1):
            for k in range(1, Nz - 1):
                T_new[i, j, k] = T[i, j, k] + alpha * dt / dx**2 * (
                    T[i+1, j, k] + T[i-1, j, k] +
                    T[i, j+1, k] + T[i, j-1, k] +
                    T[i, j, k+1] + T[i, j, k-1] - 6*T[i, j, k]
                )
    return T_new


# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


# Get initial surface
X, Y = np.meshgrid(np.arange(Nx), np.arange(Ny))
Z = T[:, :, Nz//2]  # Slice in the middle


surf = ax.plot_surface(X, Y, Z, cmap="inferno")


# Directory to save PNG images
import os
if not os.path.exists('frames'):
    os.makedirs('frames')


def animate(i):
    global T
    T = update(T)
    ax.clear()
    Z = T[:, :, Nz//2]  # Middle slice
    ax.plot_surface(X, Y, Z, cmap="inferno")
    ax.set_zlim(0, 100)
   
    # Save the current frame as PNG
    plt.savefig(f'frames/frame_{i:03d}.png')


# Create animation
ani = animation.FuncAnimation(fig, animate, frames=Nt, interval=50)


# Show the animation
plt.show()