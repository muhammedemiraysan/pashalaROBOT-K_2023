import cv2

class cam:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.window_name = "Camera Preview"
    
    def ShowCamera(self):
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                print("Error: Failed to capture video.")
                break

            cv2.imshow(self.window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.video_capture.release()
        cv2.destroyAllWindows()