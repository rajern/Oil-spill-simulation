import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tri

# Example mesh data (points and cells)
points = [
    (0, 0),  # Point 0
    (1, 0),  # Point 1
    (1, 1),  # Point 2
    (0, 1),  # Point 3
]

# Triangle cells (indices of points forming each triangle)
cells = [
    (0, 1, 2),  # Triangle 1
    (0, 2, 3),  # Triangle 2
]

# U values representing oil amounts for each cell
U_values = [5, 10]  # Oil distribution values for each triangle (cell)

# Extract x and y coordinates from points
x_points, y_points = zip(*points)

# Create a Triangulation object
triang = tri.Triangulation(x_points, y_points, cells)

# Create the plot
fig, ax = plt.subplots()

# Plot the triangles with color based on U values
# Directly pass U_values to tripcolor
ax.tripcolor(triang, facecolors=U_values, cmap='viridis', edgecolors='k')  # Color the triangles

# Add a color bar to show the distribution of oil values
cbar = plt.colorbar(ax.collections[0], ax=ax, label='Oil Distribution (U)')

# Set axis labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Oil Distribution in the Mesh')

# Show the plot
plt.show()
