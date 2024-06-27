import cv2
import mediapipe as mp
import math
import time
from kit import LineMag, distance, R_Sq, get_swipe_direction
from memory_profiler import profile
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

wCam, hCam = 640, 480
cam = cv2.VideoCapture(0)
cam.set(3, wCam)
cam.set(4, hCam)
pTime = 0

SKIP = True

PATH = []

with mp_hands.Hands(
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.3,
        min_tracking_confidence=0.3) as hands:

    CENTER_FLAG = False
    while cam.isOpened():
        success, image = cam.read()
        if not success:
            break
        image = cv2.flip(image, 1)

        if not SKIP:
            SKIP = True

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

            lmList = []
            if results.multi_hand_landmarks:
                myHand = results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])

            if len(lmList) != 0:
                x1, y1 = lmList[8][1], lmList[8][2]
                x2, y2 = lmList[12][1], lmList[12][2]
                if distance([x1, y1], [x2, y2]) < 90:
                    PATH.append([x1, y1])
                if len(PATH) > 6:
                    PATH.pop(0)
                if len(PATH) > 5 and distance(PATH[0], PATH[-1]) > 240:
                    print(340, R_Sq(PATH))
                    if R_Sq(PATH) > 0.68:
                        get_swipe_direction(PATH)

                    PATH = []
                elif LineMag(PATH) > 340:
                    PATH.pop(0)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(image, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 2)
        cv2.imshow('handDetector', image)
        SKIP = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cam.release()
cv2.destroyAllWindows()
