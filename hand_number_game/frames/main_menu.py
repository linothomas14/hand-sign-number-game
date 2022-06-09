import tkinter as tk
from hand_number_game.helper.config import LARGE_FONT
from hand_number_game.frames.basic_mode import BasicMode
from hand_number_game.frames.learn_material import LearnMaterial
from hand_number_game.frames.tutorial import Tutorial

class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self,
                         text="Permainan Pengenalan Angka",
                         font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        startButton = tk.Button(
            self,
            text="Mulai Bermain",
            command=lambda: controller.show_frame(BasicMode))
        startButton.pack(ipadx=5, ipady=5, pady=10)

        learnButton = tk.Button(
            self,
            text="Gambar Angka",
            command=lambda: controller.show_frame(LearnMaterial))
        learnButton.pack(ipadx=5, ipady=5, pady=10)

        tutorialButton = tk.Button(
            self,
            text="Cara Bermain",
            command=lambda: controller.show_frame(Tutorial))
        tutorialButton.pack(ipadx=10, ipady=5, pady=10)

    def activatedCam(self, controller):
        controller.show_frame(BasicMode)
