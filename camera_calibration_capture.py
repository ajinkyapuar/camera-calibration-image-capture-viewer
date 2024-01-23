import os
import cv2
import time

def chessboard_detection(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    retc, corners = cv2.findChessboardCorners(gray, (9, 6), None)
    if retc:
        return True
    return False

def capture_image_on_detect():
    cap = cv2.VideoCapture(0)  # Accessing the camera (change the index if needed)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        ret, frame = cap.read()
        display_frame = frame.copy()
        display_frame = cv2.resize(display_frame, (320, 180))

        detected = chessboard_detection(frame)

        if detected:
            filename = str(time.time()) + '.png'
            cv2.imwrite(os.path.join(data_dir, filename), frame)

        cv2.putText(display_frame, f'Detected: {detected}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Camera Calibration Capture', display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit loop
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    data_dir = './data'
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    capture_image_on_detect()
