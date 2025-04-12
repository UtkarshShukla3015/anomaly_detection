from tkinter.filedialog import askopenfilename
import cv2
def detect_anomalies(video_path):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return
    ret, frame_prev = cap.read()
    anomaly_detected = False
    
    while True:
        ret, frame = cap.read()        
        if not ret:
            break        
        gray_prev = cv2.cvtColor(frame_prev, cv2.COLOR_BGR2GRAY)
        gray_curr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_diff = cv2.absdiff(gray_prev, gray_curr)
        _, thresh = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            anomaly_detected = True
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('Anomaly Detection', frame)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    if anomaly_detected:
        print("Anomaly detected in the video.")
    else:
        print("No anomaly detected in the video.")
    cap.release()
    cv2.destroyAllWindows()
video_file_path = askopenfilename()
detect_anomalies(video_file_path)