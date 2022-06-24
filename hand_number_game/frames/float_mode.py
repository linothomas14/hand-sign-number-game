import tkinter as tk
import time
from hand_number_game.helper.config import REGULAR_FONT
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

        self.answered_label = tk.Label(self, text=f"Jumlah Skor : {self.answered}", font=REGULAR_FONT)
        self.answered_label.pack()

        # TODO: Utils dideclare dua kali
        self.utils = Utils

        self.highestScore = self.utils.readHighestScore()

        self.highestScore_label = tk.Label(
            self, text=f"Skor Tertinggi : {self.highestScore}", font=REGULAR_FONT
        )
        self.highestScore_label.pack()

        play = tk.Button(self, text="Play", font=REGULAR_FONT, command=self.main)
        play.pack()

        button1 = tk.Button(
            self,
            text="Back to Home", font=REGULAR_FONT,
            command=lambda: controller.show_frame(self.MainMenu))
        button1.pack()

    # Buat pop up window, tapi belum work
    def pop_up(self, parent, controller):
        pop = tk.Toplevel(parent)
        pop.geometry("250x150")

        pop_label = tk.Label(pop,text="Kamu kurang cepat, coba lagi")
        pop_label.pack(pady=10)

        back_button = tk.Button(pop, text="Kembali", command=lambda: controller.show_frame(self.MainMenu))
        back_button.pack()
 
    def main(self):
        # pTime = 0
        wCam, hCam = 800, 380
        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)
        x = 40

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

            # If number pass over the camera
            if ynum <= 0:
                x = 40
                number = str(randint(1, 10))
                print("Kamu kalah")
                # pop = tk.Toplevel(self)
                # pop.geometry("250x150")

                # pop_label = tk.Label(pop,text="Kamu kurang cepat, coba lagi")
                # pop_label.pack(pady=10)

                # back_button = tk.Button(pop, text="Kembali")
                # back_button.pack()
                ynum = 500
                xnum = randint(50, 400)



            # Green-bar
            cv2.rectangle(img, (40, 400), (600, 450), (0, 255, 0), 3)
            cv2.rectangle(img, (40, 400), (x, 450), (0, 255, 0), cv2.FILLED)

            # Number Text
            cv2.putText(
                img, number, (xnum, ynum), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 0), 5
            )

            # Return from BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(img))
            self.imgLabel["image"] = img
            self.answered_label["text"] = f"Jumlah Skor : {self.answered}"
            self.update()

