import tkinter as tk   
import tkinter as tk
from config import LARGE_FONT
from random import randint
import tkinter as tk
from PIL import Image, ImageTk
import cv2
from helper.utils import Utils, readHighestScore, updateHighestScore
import helper.HandTrackingModule as htm
from playsound import playsound


LARGE_FONT= ("Verdana", 12)

class NumberGame(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.geometry("1000x700")
        container.pack(pady=50,side="top", fill="both", expand = True)
        text = "123"
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.activeCam = False
        self.answered = 0
        self.frames = {}

        for F in (MainMenu, BasicMode, LearnMaterial):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, cont):
        
        global activeCam, answered
        answered = 0
        activeCam = False
        frame = self.frames[cont]
        frame.tkraise()

class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Permainan Pengenalan Angka", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        startButton = tk.Button(self, text="Mulai Bermain",
                            command=lambda : controller.show_frame(BasicMode))
        startButton.pack(ipadx=5, ipady=5, pady=10)

        learnButton = tk.Button(self, text="Gambar Angka",
                            command=lambda: controller.show_frame(LearnMaterial))
        learnButton.pack(ipadx=5, ipady=5, pady=10)

        tutorialButton = tk.Button(self, text="Cara Bermain",
                            command=lambda: controller.show_frame(LearnMaterial))
        tutorialButton.pack(ipadx=10, ipady=5, pady=10)


    def activatedCam(self,controller):
        controller.show_frame(BasicMode)


class BasicMode(tk.Frame):
    print('masuk')
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global answered
        answered = 0

        self.imgLabel = tk.Label(self)
        self.imgLabel.pack(fill="both", expand="yes")

        self.answered_label = tk.Label(self,
            text=f"Jumlah Skor : {answered}")
        self.answered_label.pack()

        self.highestScore = readHighestScore()

        self.highestScore_label = tk.Label(self,text=f"Skor Tertinggi : {self.highestScore}")
        self.highestScore_label.pack()

        play = tk.Button(self, text="Play", command=self.main)
        play.pack()

        button1 = tk.Button(self,
                            text="Back to Home",
                            command=lambda: controller.show_frame(MainMenu))
        button1.pack()



    def mainMenu(self):
        global activeCam, answered
        activeCam = False
        answered = 0
        

    def main(self):
        wCam, hCam = 800, 380
        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)
        x = 40
        detector = htm.handDetector(detectionCon=0.75)
        utils = Utils(detector=detector)

        fingers_list = utils.fingers_list

        number = str(randint(1, 10))

        global activeCam, answered
        answered = 0
        activeCam = False if activeCam == True else True
        while activeCam:
            print("helo")
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
                playsound('./assets/click.wav', block=False)
                answered += 1
                if answered > self.highestScore:
                    #self.highestScore = answered
                    self.highestScore_label['text'] = f"Skor Tertinggi : {answered}"
                    updateHighestScore(answered)

            # Green-bar
            cv2.rectangle(img, (40, 400), (x, 430), (0, 255, 0), cv2.FILLED)
            # print(x)
           
            cv2.putText(img, number, (310, 70), cv2.FONT_HERSHEY_PLAIN, 4,
                        (0, 255, 0), 5)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(img))

            self.imgLabel["image"] = img
            self.answered_label['text'] = f"Correct answers: {answered}"
            self.update()



class LearnMaterial(tk.Frame):

    #Importing Photos
    dir = "assets/"
    image_list=[]
    text_list = []
    for i in range(10):
        img = dir + str(i+1) + '.png'
        text_list.append(str(i+1))    
        image_list.append(img)

    current = 0
        
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.label = tk.Label(self, text="Gambar Angka", font=LARGE_FONT)
        self.label.pack(pady=10,padx=10)

        self.imgWrapper = tk.Label(self, compound=tk.TOP)
        self.imgWrapper.pack()

        self.buttonWrapper = tk.Frame(self)
        self.buttonWrapper.pack(pady=15)

        tk.Button(self.buttonWrapper, text='Previous', command=lambda: self.move(-1)).grid(padx=5,row=0,column=0)
        tk.Button(self.buttonWrapper, text='Next', command=lambda: self.move(+1)).grid(padx=5,ipadx=15,row=0,column=1)
        backToMainMenuButton = tk.Button(self, text="Main menu",
                            command=lambda: controller.show_frame(MainMenu))
        backToMainMenuButton.pack(ipadx=5,ipady=5,pady=10, side = tk.TOP)
        self.move(0)
    
    def move(self,Rd):

        if not (0 <= self.current + Rd < len(self.image_list)):
            return
        self.current += Rd
        image = Image.open(self.image_list[self.current])
        photo = ImageTk.PhotoImage(image)
        self.imgWrapper['text'] = "Angka " + self.text_list[self.current]
        self.imgWrapper['image'] = photo
        self.imgWrapper.photo = photo
    
          

app = NumberGame()

app.mainloop()

    
