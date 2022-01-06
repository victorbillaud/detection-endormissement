import numpy as np
import cv2
from pygame import mixer

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

first_read = True
compteur = 0

cap = cv2.VideoCapture(0)
ret, img = cap.read()


# Starting the mixer
mixer.init()

# Loading the song
mixer.music.load("file.mp3")

# Setting the volume
mixer.music.set_volume(0.7)

while (ret):
    ret, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.bilateralFilter(gray, 5, 1, 1)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(20, 20))
    if (len(faces) > 0):
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_face = gray[y:y + h, x:x + w]
            roi_face_clr = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_face, 1.3, 5, minSize=(50, 50))

            cv2.putText(img,
                        "nb click" + str(compteur),
                        (300, 300),
                        cv2.FONT_HERSHEY_PLAIN, 3,
                        (0, 255, 0), 2)

            if (len(eyes) >= 2):

                if (first_read):
                    mixer.music.pause()
                    cv2.putText(img,
                                "Eye detected press s to begin",
                                (70, 70),
                                cv2.FONT_HERSHEY_PLAIN, 3,
                                (0, 255, 0), 2)
                else:
                    cv2.putText(img,
                                "Eyes open!", (70, 70),
                                cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 255, 255), 2)
            else:
                if (first_read):
                    mixer.music.play()
                    cv2.putText(img,
                                "No eyes detected", (70, 70),
                                cv2.FONT_HERSHEY_PLAIN, 3,
                                (0, 0, 255), 2)
                else:

                    print("Blink detected--------------")
                    cv2.waitKey(3000)
                    first_read = True
                    compteur=compteur+1

    else:
        cv2.putText(img,
                    "No face detected", (100, 100),
                    cv2.FONT_HERSHEY_PLAIN, 3,
                    (0, 255, 0), 2)

    cv2.imshow('img', img)
    a = cv2.waitKey(1)
    if (a == ord('q')):
        break
    elif (a == ord('s') and first_read):

        first_read = False

cap.release()
cv2.destroyAllWindows()