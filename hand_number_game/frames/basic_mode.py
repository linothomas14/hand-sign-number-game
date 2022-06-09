import tkinter as tk
from hand_number_game.helper.utils import Utils
import hand_number_game.helper.HandTrackingModule as htm
import cv2
from random import randint
from PIL import Image, ImageTk
from playsound import playsound


class BasicMode(tk.Frame):
    def __init__(self, parent, controller):
        self.MainMenu = None
        self.activeCam = False
        self.answered = 0
        tk.Frame.__init__(self, parent)

        self.imgLabel = tk.Label(self)
        self.imgLabel.pack(fill="both", expand="yes")

        self.answered_label = tk.Label(self,
                                       text=f"Jumlah Skor : {self.answered}")
        self.answered_label.pack()

        # TODO: Utils dideclare dua kali
        self.utils = Utils

        self.highestScore = self.utils.readHighestScore()

        self.highestScore_label = tk.Label(
            self, text=f"Skor Tertinggi : {self.highestScore}")
        self.highestScore_label.pack()

        play = tk.Button(self, text="Play", command=self.main)
        play.pack()

        button1 = tk.Button(
            self,
            text="Back to Home",
            command=lambda: controller.show_frame(self.MainMenu))
        button1.pack()

    def mainMenu(self):
        self.activeCam = False

    def main(self):
        wCam, hCam = 800, 380
        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)
        x = 40

        detector = htm.handDetector(detectionCon=0.75)
        # Ini juga
        utils = Utils(detector=detector)

        fingers_list = utils.fingers_list
        self.answered = 0
        number = str(randint(1, 10))

        self.activeCam = False if self.activeCam is True else True
        while self.activeCam:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img, handsType = detector.findHands(img)
            fingers = utils.get_shown_fingers(img=img, hands_type=handsType)

            cv2.rectangle(img, (40, 400), (600, 430), (0, 255, 0), 3)

            # To check match finger with number displayed
            for i in fingers_list:
                if fingers_list[i] == fingers and i == number and x < 600:
                    x += 20
            if x >= 600:
                x = 70
                number = str(randint(1, 10))
                num = str(randint(1, 10))
                playsound('./assets/click.wav', block=False)
                playsound("./assets/sounds/"+self.utils.getSound(num), block=False)
                self.answered += 1
                if self.answered > self.highestScore:
                    # self.highestScore = answered
                    self.highestScore_label[
                        'text'] = f"Skor Tertinggi : {self.answered}"
                    self.utils.updateHighestScore(self.answered)

            # Green-bar
            cv2.rectangle(img, (40, 400), (x, 430), (0, 255, 0), cv2.FILLED)

            cv2.putText(img, number, (310, 70), cv2.FONT_HERSHEY_PLAIN, 4,
                        (0, 255, 0), 5)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(img))

            self.imgLabel["image"] = img
            self.answered_label['text'] = f"Correct answers: {self.answered}"
            self.update()
