import tkinter as tk

from numpy import spacing
from hand_number_game.helper.config import LARGE_FONT, REGULAR_FONT


class Tutorial(tk.Frame):
    def __init__(self, parent, controller):
        self.MainMenu = None
        tk.Frame.__init__(self, parent)
        stringHowTo = (
            '1. Pada menu utama tekan "Mulai Bermain", lalu tekan "Play" .\n'
            "2. Kamera akan terbuka\n"
            "3. Peragakan angka yang muncul pada layar dengan jari sampai bar hijau terisi penuh\n"
            "4. Ulangi langkah kedua untuk mendapatkan skor yang lebih tinggi"
        )

        self.title = tk.Label(self, text="Instruksi permainan", font=LARGE_FONT)
        self.title.pack(pady=10, padx=10)

        text = tk.Text(self, wrap=tk.CHAR, font=("Ubuntu", "15"))

        text.insert(tk.INSERT, stringHowTo)
        text.config(state=tk.DISABLED, spacing1=10, width=90, height=10)
        text.pack(ipady=10)
        backToMainMenuButton = tk.Button(
            self, text="Main menu",font=REGULAR_FONT, command=lambda: controller.show_frame(self.MainMenu)
        )
        backToMainMenuButton.pack(ipadx=5, ipady=5, pady=10, side=tk.BOTTOM)
