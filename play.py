from PIL import Image, ImageTk
import cv2
# from tkinter import *
import tkinter as tk


class Play(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x700")
        self.imgLabel = tk.Label(self)
        self.imgLabel.pack(fill="both", expand="yes")

        self.mainMenuButton = tk.Button(self,text="Play",
                                command=self.mainMenu)
        self.mainMenuButton.pack()
        
            
    def mainMenu(self):
        self.destroy()
        import app

def main():
    pTime = 0
    wCam, hCam = 800, 380
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    app = Play()
    while True :
        print("helo")
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(image = Image.fromarray(img))
        
        app.imgLabel['image'] = img
        app.update()

