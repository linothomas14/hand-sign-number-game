import threading
import tkinter as tk
from hand_number_game.helper.config import REGULAR_FONT
from hand_number_game.helper.media import Media
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
                                       text=f"Jumlah Skor : {self.answered}", font=REGULAR_FONT)
        self.answered_label.pack()

        self.media = Media

        self.highestScore = self.media.readHighestScore("basic")

        self.highestScore_label = tk.Label(
            self, text=f"Skor Tertinggi : {self.highestScore}", font=REGULAR_FONT)
        self.highestScore_label.pack()

        play = tk.Button(self, text="Play",
                         bg="green",
                         fg="white",
                         font=REGULAR_FONT, command=self.main)
        play.pack(pady=5, ipadx=20)

        back_button = tk.Button(
            self,
            text="Back to Home", font=REGULAR_FONT,
            command=lambda: controller.show_frame(self.MainMenu))
        back_button.pack()

    def main(self):
        wCam, hCam = 640, 480
        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)
        x = 40

        detector = htm.HandTrackingModule(detectionCon=0.75)

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

            # To check match finger with number displayed
            for i in fingers_list:
                if fingers_list[i] == fingers and i == number and x < 600:
                    x += 35
            if x >= 600:
                x = 40
                number = str(randint(1, 10))
                num = str(randint(1, 10))
                threading.Thread(target=playsound, args=(
                    './assets/sounds/click.wav',), daemon=True).start()
                threading.Thread(target=playsound, args=(
                    './assets/sounds/'+self.media.getSound(num),), daemon=True).start()
                # playsound('./assets/sounds/click.wav', block=False)
                # playsound("./assets/sounds/"+self.media.getSound(num), block=False)
                self.answered += 1
                if self.answered > self.highestScore:
                    self.highestScore_label[
                        'text'] = f"Skor Tertinggi : {self.answered}"
                    self.media.updateHighestScore(self.answered, "basic")

            # Green-bar
            cv2.rectangle(img, (40, 400), (600, 430), (0, 255, 0), 3)
            cv2.rectangle(img, (40, 400), (x, 430), (0, 255, 0), cv2.FILLED)

            cv2.putText(img, number, (300, 70), cv2.FONT_HERSHEY_PLAIN, 4,
                        (0, 255, 0), 5)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(img))

            self.imgLabel["image"] = img
            self.answered_label['text'] = f"Jumlah Skor : {self.answered}"
            self.update()
