from hand_number_game.frames.learn_material import LearnMaterial
from hand_number_game.frames.tutorial import Tutorial
from hand_number_game.frames.basic_mode import BasicMode
from hand_number_game.frames.main_menu import MainMenu
from hand_number_game.frames.float_mode import FloatMode
import tkinter as tk


class NumberGame(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.title("Hand Sign Number Game")
        self.geometry("1000x700")
        container.pack(pady=50, side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.activeCam = False
        self.answered = 0
        self.frames = {}

        for F in (MainMenu, BasicMode, LearnMaterial, Tutorial, FloatMode):

            frame = F(container, self)
            frame.MainMenu = MainMenu

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, cont):

        self.frames[BasicMode].answered = 0
        self.frames[BasicMode].activeCam = 0

        self.frames[FloatMode].answered = 0
        self.frames[FloatMode].activeCam = 0
        frame = self.frames[cont]
        frame.tkraise()
