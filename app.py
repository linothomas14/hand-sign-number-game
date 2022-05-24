import tkinter as tk
from PIL import Image, ImageTk
import cv2
import play
LARGE_FONT= ("Verdana", 12)
con = False

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.geometry("1000x700")
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, BasicMode, LearnMaterial):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
    
    def play(self):
        self.destroy()
        play.main()
    


        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Play",
                            command=lambda : self.activatedCam(controller))
        button.pack()

        button2 = tk.Button(self, text="Learn Material",
                            command=lambda: controller.show_frame(LearnMaterial))
        button2.pack()

    def activatedCam(self,controller):
        print("masuk func")
        global con
        con = True
        print("con sebelum : ", con)
        controller.show_frame(BasicMode)
    # def play(self):
    #     super.destroy()
    #     import play


class BasicMode(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.imgLabel = tk.Label(self)
        self.imgLabel.pack(fill="both", expand="yes")

        self.mainMenuButton = tk.Button(self,text="Play",
                                command=self.mainMenu)
        self.mainMenuButton.pack()
        
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(LearnMaterial))
        button2.pack()


        imgLabel = tk.Label()
        global con
        while con:
            print("pass")
            # self.main()

    def mainMenu(self):
        self.destroy()
        import app

    def main(self):
        pTime = 0
        wCam, hCam = 800, 380
        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)
        global con
        print(con)
        while con :
            print("helo")
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image = Image.fromarray(img))
            
            self.imgLabel['image'] = img
            self.update()

        



class LearnMaterial(tk.Frame):

    #Importing Photos
    dir = "assets/"
    image_list=[]
    text_list = []
    for i in range(5):
        img = dir + str(i+1) + '.png'
        text_list.append(str(i+1))    
        image_list.append(img)

    current = 0
        
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        label = tk.Label(self, text="Learn Material", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        self.imgWrapper = tk.Label(self, compound=tk.TOP)
        self.imgWrapper.pack()
        tk.Button(self, text='Previous picture', command=lambda: self.move(-1)).pack(side=tk.BOTTOM)
        tk.Button(self, text='Next picture', command=lambda: self.move(+1)).pack(side=tk.BOTTOM)
        button1 = tk.Button(self, text="Back to Main menu",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        self.move(0)
        print('test')
    
    def move(self,Rd):

        if not (0 <= self.current + Rd < len(self.image_list)):
            return
        self.current += Rd
        image = Image.open(self.image_list[self.current])
        photo = ImageTk.PhotoImage(image)
        self.imgWrapper['text'] = "Number " + self.text_list[self.current]
        self.imgWrapper['image'] = photo
        self.imgWrapper.photo = photo




            


app = SeaofBTCapp()

# cap = cv2.VideoCapture(0)

app.mainloop()
# while True :
    # print('halo')
    # success, img = cap.read()
    # img = cv2.flip(img, 1)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = ImageTk.PhotoImage(Image.fromarray(img))
    # app.frames["BasicMode"].imgLabel['image'] = img
# app.update()
    
