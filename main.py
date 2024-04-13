import numpy as np
import cv2
import PanelInfo
import math


cap = cv2.VideoCapture(0)
panel_info = PanelInfo.PanelInfo()
screen_width, screen_height = panel_info.get_screen_resolution()

# Naming a window 
cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL) 
# Using resizeWindow() 
cv2.resizeWindow("Resized_Window", screen_width, screen_height) 


# Get Haar cascades
face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_eye.xml')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()  # ret = 1 if the video is captured; frame is the image
    frame = cv2.flip(frame, 1)

    # Rectangle on center
    frame_width = math.floor(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = math.floor(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    center_x, center_y = panel_info.get_frame_center(frame_width, frame_height)
    #cv2.rectangle(frame, (center_x - 100, center_y - 100), (center_x + 100, center_y + 100), (0,255,0), 2)


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    if(len(face) > 0):
        (x, y, w, h) = face[0]
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            eye_roi_gray = roi_gray[ey:ey+eh, ex:ex+ew]
            eye_roi_color = roi_color[ey:ey+eh, ex:ex+ew]
            _, eye_thresh = cv2.threshold(eye_roi_gray, 50, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(eye_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                pupil = max(contours, key=cv2.contourArea)
                x1, y1, w1, h1 = cv2.boundingRect(pupil)
                center = (int(x1 + w1/2), int(y1 + h1/2))
                cv2.circle(eye_roi_color, center, 3, (255, 0, 0),-1)
    
    # Display the resulting image
    cv2.imshow('Resized_Window',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
        break
        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()