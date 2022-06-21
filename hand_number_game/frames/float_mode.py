import tkinter as tk
import time
from hand_number_game.helper.utils import Utils
import hand_number_game.helper.HandTrackingModule as htm
import cv2
from random import randint
from PIL import Image, ImageTk
from playsound import playsound


class FloatMode(tk.Frame):
    def __init__(self, parent, controller):
        self.MainMenu = None
        self.activeCam = False
        self.answered = 0
        tk.Frame.__init__(self, parent)

        self.imgLabel = tk.Label(self)
        self.imgLabel.pack(fill="both", expand="yes")

        self.answered_label = tk.Label(self, text=f"Jumlah Skor : {self.answered}")
        self.answered_label.pack()

        # TODO: Utils dideclare dua kali
        self.utils = Utils

        self.highestScore = self.utils.readHighestScore()

        self.highestScore_label = tk.Label(
            self, text=f"Skor Tertinggi : {self.highestScore}"
        )
        self.highestScore_label.pack()

        play = tk.Button(self, text="Play", command=self.main)
        play.pack()

        button1 = tk.Button(
            self,
            text="Back to Home",
            command=lambda: controller.show_frame(self.MainMenu),
        )
        button1.pack()

    def main(self):
        # pTime = 0
        wCam, hCam = 1000, 480
        x = 60
        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)

        detector = htm.handDetector(detectionCon=0.75)
        utils = Utils(detector=detector)

        fingers_list = utils.fingers_list
        ynum = 500
        xnum = 310
        number = str(randint(1, 10))

        self.activeCam = False if self.activeCam is True else True
        while True:
            # To capture frame from camera device and process it with HandTrackingModule
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img, handsType = detector.findHands(img)
            fingers = utils.get_shown_fingers(img=img, hands_type=handsType)

            ynum -= 7

            # To check match finger with number displayed
            for i in fingers_list:
                if fingers_list[i] == fingers and i == number and x < 600:
                    x += 40

            if x >= 600:
                x = 40
                number = str(randint(1, 10))
                self.answered += 1
                ynum = 500
                xnum = randint(50, 400)

            # Green-bar
            cv2.rectangle(img, (40, 400), (600, 450), (0, 255, 0), 3)
            cv2.rectangle(img, (40, 400), (x, 450), (0, 255, 0), cv2.FILLED)

            # FPS Text
            # cTime = time.time()
            # fps = 1 / (cTime - pTime)
            # pTime = cTime
            # cv2.putText(
            #     img,
            #     f"FPS: {int(fps)}",
            #     (10, 20),
            #     cv2.FONT_HERSHEY_PLAIN,
            #     2,
            #     (0, 0, 0),
            #     1,
            # )

            # Number Text
            cv2.putText(
                img, number, (xnum, ynum), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 0), 5
            )

            # Return from BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(img))
            self.imgLabel["image"] = img
            self.answered_label["text"] = f"Correct answers: {self.answered}"
            self.update()
