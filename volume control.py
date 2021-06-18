from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from detecting_hands import DetectHand
import cv2
import mediapipe as mp
import math

#setting up pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
print(volume.GetVolumeRange())
#---------------------------------------------------------------------

cap = cv2.VideoCapture(0)
detector = DetectHand(min_detection_confidence = 0.7)
while(cap.isOpened()):
    success, frame = cap.read()
    image = detector.detect_hands(frame, draw = 0)
    length = detector.get_coordinates(image, draw = 1)
    if(length>120):
        volume.SetMasterVolumeLevel(0, None)
    if (length < 54.75 and length >=0):
        volume.SetMasterVolumeLevel(-65.25, None)
    if(length >= 54.75 and length <= 120.0):
        volume.SetMasterVolumeLevel(length-120, None)
    print(volume.GetMasterVolumeLevel())
    cv2.imshow("hands", image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
            
cap.release()





#volume.SetMasterVolumeLevel(-20.0, None)


print(volume.GetMasterVolumeLevel())
print(volume.GetVolumeRange())
