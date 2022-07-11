import tkinter as tk
from PIL import Image, ImageTk
from hand_number_game.helper.config import LARGE_FONT, REGULAR_FONT


class LearnMaterial(tk.Frame):

    # Importing Photos
    dir = "assets/hand-images/"
    image_list = []
    text_list = []
    for i in range(10):
        img = dir + str(i + 1) + '.png'
        text_list.append(str(i + 1))
        image_list.append(img)

    current = 0

    def __init__(self, parent, controller):
        self.MainMenu = None
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text="Gambar Angka", font=LARGE_FONT)
        self.label.pack(pady=10, padx=10)

        self.imgWrapper = tk.Label(self, font=REGULAR_FONT, compound=tk.TOP)
        self.imgWrapper.pack()

        self.buttonWrapper = tk.Frame(self)
        self.buttonWrapper.pack(pady=15)

        tk.Button(self.buttonWrapper,
                  text='Previous', font=REGULAR_FONT,
                  command=lambda: self.move(-1)).grid(padx=5, row=0, column=0)
        tk.Button(self.buttonWrapper,
                  text='Next', font=REGULAR_FONT,
                  command=lambda: self.move(+1)).grid(padx=5,
                                                      ipadx=15,
                                                      row=0,
                                                      column=1)
        backToMainMenuButton = tk.Button(
            self,
            text="Main menu", font=REGULAR_FONT,
            command=lambda: controller.show_frame(self.MainMenu))
        backToMainMenuButton.pack(ipadx=5, ipady=5, pady=10, side=tk.TOP)
        self.move(0)

    def move(self, Rd):

        if not (0 <= self.current + Rd < len(self.image_list)):
            return
        self.current += Rd
        image = Image.open(self.image_list[self.current])
        photo = ImageTk.PhotoImage(image)
        self.imgWrapper['text'] = "Angka " + self.text_list[self.current]
        self.imgWrapper['image'] = photo
        self.imgWrapper.photo = photo
