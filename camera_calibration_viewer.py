import os
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
import pickle

class ImageViewer:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.image_list = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        self.current_index = 0

        self.corners = []
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.pts = np.zeros((6 * 9, 3), np.float32)
        self.pts[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)
        self.frame = None


        self.obj_points = []  # 3d point in real world space
        self.img_points = []  # 2d points in image plane.
        self.frames = []

        self.cam_calib = {'mtx': np.eye(3), 'dist': np.zeros((1, 5))}

        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Add buttons
        next_button = tk.Button(self.root, text="Next", command=self.next_image)
        next_button.pack(side=tk.LEFT)

        check_button = tk.Button(self.root, text="Check", command=self.check_image)
        check_button.pack(side=tk.LEFT)

        add_button = tk.Button(self.root, text="Add", command=self.add_image)
        add_button.pack(side=tk.LEFT)

        calib_button = tk.Button(self.root, text="Calibrate", command=self.calibrate_camera)
        calib_button.pack(side=tk.LEFT)

        save_button = tk.Button(self.root, text="Save", command=self.save_cam_calib)
        save_button.pack(side=tk.LEFT)


        # delete_button = tk.Button(self.root, text="Delete", command=self.delete_image)
        # delete_button.pack(side=tk.RIGHT)

        self.original_photo = None  # Initialize original_photo

        self.load_images()

        self.root.mainloop()

    def load_images(self):
        if not self.image_list:
            # No images left, destroy the window
            self.root.destroy()
            return

        original_path = os.path.join(self.folder_path, self.image_list[self.current_index])
        original_image = Image.open(original_path)
        original_image = original_image.resize((640, 360), Image.LANCZOS)
        self.original_photo = ImageTk.PhotoImage(original_image)

        self.canvas.config(width=self.original_photo.width() * 2, height=self.original_photo.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.original_photo)

        self.root.title(f"Image Viewer - {self.image_list[self.current_index]}")
        self.root.update_idletasks()
        self.root.update()

    def next_image(self):
        self.current_index = (self.current_index + 1) % len(self.image_list)
        self.load_images()

    # def delete_image(self):
    #     if not self.image_list:
    #         # No images left, destroy the window
    #         self.root.destroy()
    #         return

    #     image_path = os.path.join(self.folder_path, self.image_list[self.current_index])
    #     os.remove(image_path)
    #     del self.image_list[self.current_index]
    #     if self.current_index >= len(self.image_list):
    #         self.current_index = 0
    #     self.load_images()

    def check_image(self):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        if not self.image_list:
            # No images left, destroy the window
            self.root.destroy()
            return

        checked_path = os.path.join(self.folder_path, self.image_list[self.current_index])
        # checked_image = Image.open(checked_path)


        bgr = cv2.imread(checked_path)
        bgr_copy = bgr.copy()
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        retc, corners = cv2.findChessboardCorners(gray, (9, 6), None)
        if retc:
            cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            # Draw and display the corners
            cv2.drawChessboardCorners(bgr_copy, (9, 6), corners, True)
            # cv2.imshow("BGR", bgr_copy)
            self.corners = corners
            self.frame = bgr

        rgb = cv2.cvtColor(bgr_copy, cv2.COLOR_BGR2RGB)
        checked_image = Image.fromarray(rgb)

        checked_image = checked_image.resize((640, 360), Image.LANCZOS)
        self.checked_photo = ImageTk.PhotoImage(checked_image)

        self.canvas.create_image(self.original_photo.width(), 0, anchor=tk.NW, image=self.checked_photo)
        print(f"Checked: {self.image_list[self.current_index]}")

    def add_image(self):
        self.img_points.append(self.corners)
        self.obj_points.append(self.pts)
        self.frames.append(self.frame)
        print(len(self.img_points), len(self.obj_points), len(self.frames))

    def calibrate_camera(self):
        # compute calibration matrices
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.obj_points, self.img_points, self.frames[0].shape[0:2], None, None)

        # check
        error = 0.0
        for i in range(len(self.frames)):
            proj_imgpoints, _ = cv2.projectPoints(self.obj_points[i], rvecs[i], tvecs[i], mtx, dist)
            error += (cv2.norm(self.img_points[i], proj_imgpoints, cv2.NORM_L2) / len(proj_imgpoints))
        print("Camera calibrated! total re-projection error: %f" % (error / len(self.frames)))

        self.cam_calib['mtx'] = mtx
        self.cam_calib['dist'] = dist
        print("Camera parameters:")
        print(self.cam_calib)

    def save_cam_calib(self):
        pickle.dump(self.cam_calib, open("calib_cam.pkl", "wb"))




if __name__ == "__main__":
    folder_path = "./data"  # Replace with the path to your image folder
    viewer = ImageViewer(folder_path)
