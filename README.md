# Camera Calibration and Image Viewer

## Overview
These Python scripts serves a dual purpose: capturing images for camera calibration and providing a graphical interface to view and calibrate a camera.

## Features

### Image Capture

- Chessboard Detection: Captures images from a camera feed when a 9x6 chessboard pattern is detected.
- Image Saving: Saves detected chessboard frames for camera calibration.

### Camera Calibration Viewer

- Image Viewer: Allows users to view and check images for camera calibration.
- Image Addition: Adds images with detected chessboard patterns to the calibration dataset.
- Camera Calibration: Performs camera calibration using the collected image dataset.
- Save Calibration: Saves the camera calibration parameters to a file.


## Requirements
- Python 3.x
- OpenCV
- Pillow (PIL)
- Tkinter
- Numpy
- Pickle

## Usage
Clone the repository or download the scripts.

Install the required dependencies:

- `pip install -r requirements.txt`

Run the scripts:

- `python camera_calibration_capture.py`

- `python camera_calibration_viewer.py`

Follow on-screen instructions:

- Press 'Next' to view the next image.
- Press 'Check' to detect and display the chessboard in the current image.
- Press 'Add' to add the detected chessboard to the calibration dataset.
- Press 'Calibrate' to perform camera calibration.
- Press 'Save' to save the camera calibration parameters.

## Configuration
The script assumes a folder named 'data' containing images for calibration. Update the folder_path variable if your images are stored elsewhere.
File Structure
The captured images and camera calibration parameters are saved in the script directory.
Notes
This script is designed for camera calibration using a chessboard pattern.
Ensure a sufficient number of images with varying chessboard poses for accurate calibration.