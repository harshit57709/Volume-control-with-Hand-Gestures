from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from detecting_hands import DetectHand
import cv2
import mediapipe as mp
import math
import numpy

#setting up pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#---------------------------------------------------------------------

cap = cv2.VideoCapture(0)
detector = DetectHand(min_detection_confidence = 0.7)
while(cap.isOpened()):
    success, frame = cap.read()
    image = detector.detect_hands(frame, draw = 0)
    length = detector.get_coordinates(image, draw = 1)
    vol = numpy.interp(length, [25, 150], [-65.25, 0])
    cv2.rectangle(image, (20, 40), (30, 105), (0,255, 0), 1)
    cv2.rectangle(image, (20, int(40 - vol)), (30, 105), (0, 255, 0), -1)
    volume.SetMasterVolumeLevel(float(vol), None)
    cv2.imshow("hands", image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
            
cap.release()





