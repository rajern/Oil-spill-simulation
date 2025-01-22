import pytest
import os
import shutil
import numpy as np
import cv2 
from packages.simulation.plot_animation import plot, animation  # Replace 'your_module' with the actual module name

# Mocked classes for testing
class MockSimMesh:
    def __init__(self, cells, points_inside_area):
        self._cells = cells
        self._points_inside_area = points_inside_area

    def update_oil(self, delta_t):
        pass

class MockSimTriangle:
    def __init__(self, coordinates, oil_amount):
        self._coordinates = coordinates
        self._oil_amount = oil_amount

    def get_amount_of_oil(self):
        return self._oil_amount

def test_plot():
    mock_cells = [
        MockSimTriangle([(0, 0), (1, 0), (0, 1)], 0.5)
    ]
    mock_mesh = MockSimMesh(mock_cells, [0])

    destination_folder = "test_plot_output"
    nr_of_pics = 1
    timesteps = 1
    delta_t = 0.1

    if os.path.exists(destination_folder):
        shutil.rmtree(destination_folder)

    plot(mock_mesh, destination_folder, nr_of_pics, timesteps, delta_t)

    images_folder = os.path.join(destination_folder, "images")

    assert os.path.exists(images_folder), "Images folder not created."
    assert len(os.listdir(images_folder)) == nr_of_pics, "Incorrect number of images saved."

    shutil.rmtree(destination_folder)

def test_animation():
    folder = "test_animation_output"
    img_name = "frame_"
    nr_of_pics = 1

    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(os.path.join(folder, "images"))

    # Create a dummy image
    dummy_image_path = os.path.join(folder, "images", f"{img_name}0.png")
    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.imwrite(dummy_image_path, dummy_image)

    animation(folder, img_name, nr_of_pics)

    assert os.path.exists("video.AVI"), "Video file not created."

    # Clean up
    shutil.rmtree(folder)
    os.remove("video.AVI")

# Run tests
if __name__ == "__main__":
    pytest.main()
