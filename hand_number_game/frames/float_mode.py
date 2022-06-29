import threading
import tkinter as tk
from hand_number_game.helper.config import REGULAR_FONT, SMALL_FONT
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

        tk.Frame.__init__(self, parent)

        self.imgLabel = tk.Label(self)
        self.imgLabel.pack(fill="both", expand="yes")

        self.answered_label = tk.Label(self, text=f"Jumlah Skor : 0", font=REGULAR_FONT)
        self.answered_label.pack()

        # TODO: Utils dideclare dua kali
        self.utils = Utils

        self.highestScore = self.utils.readHighestScore("float")

        self.highestScore_label = tk.Label(
            self, text=f"Skor Tertinggi : {self.highestScore}", font=REGULAR_FONT
        )
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

    def pop_up(self):

        pop = tk.Toplevel()
        width = 250 # width for the Tk root
        height = 100 # height for the Tk root
        width_screen = pop.winfo_screenwidth() # width of the screen
        height_screen = pop.winfo_screenheight() # height of the screen

        x = (width_screen/2) - (width/2)
        y = ((height_screen/2) - 30) - (height/2)

        # set the dimensions of the screen 
        pop.geometry('%dx%d+%d+%d' % (width, height, x, y))

        pop_label = tk.Label(pop,text="Kamu kurang cepat, coba lagi",font=REGULAR_FONT )
        pop_label.pack(pady=10)

        back_button = tk.Button(pop, text="Kembali",font=REGULAR_FONT, command=lambda:pop.destroy())
        back_button.pack()
 
    def main(self):
        wCam, hCam = 640, 480
        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)
        x = 40
        self.answered = 0
        self.lifes = 3

        detector = htm.handDetector(detectionCon=0.75)
        utils = Utils(detector=detector)

        fingers_list = utils.fingers_list
        ynum = 500
        xnum = 310
        number = str(randint(1, 10))

        
        self.activeCam = False if self.activeCam is True else True
        while self.activeCam:
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
                num = str(randint(1, 10))
                threading.Thread(target=playsound, args=('./assets/sounds/click.wav',), daemon=True).start()
                threading.Thread(target=playsound, args=('./assets/sounds/'+self.utils.getSound(num),), daemon=True).start()
                # playsound('./assets/sounds/click.wav', block=False)
                # playsound("./assets/sounds/"+self.utils.getSound(num), block=False)
                ynum = 500
                xnum = randint(50, 400)
                self.answered += 1
                if self.answered > self.highestScore:
                    # self.highestScore = answered
                    self.highestScore_label[
                        'text'] = f"Skor Tertinggi : {self.answered}"
                    self.utils.updateHighestScore(self.answered, "float")

            # If number pass over the camera
            if ynum <= 0:
                x = 40
                self.lifes-=1
                number = str(randint(1, 10))
                
                ynum = 500
                xnum = randint(50, 400)

                if self.lifes < 0:
                    self.activeCam = False
                    self.pop_up()
                    return
            
            # Green-bar
            cv2.rectangle(img, (40, 400), (600, 450), (0, 255, 0), 3)
            cv2.rectangle(img, (40, 400), (x, 450), (0, 255, 0), cv2.FILLED)

            # Number Text
            cv2.putText(
                img, number, (xnum, ynum), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 0), 5
            )

            # Remaining lifes 
            cv2.putText(
            img, f"Nyawa : {self.lifes}",(20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2
        )

            # Return from BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(img))
            
            self.imgLabel["image"] = img
            self.answered_label["text"] = f"Jumlah Skor : {self.answered}"
            self.update()

