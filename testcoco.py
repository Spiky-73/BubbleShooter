

import tkinter

def lancer(event: tkinter.Event):
    print("lancer")

def mouvement_souris(event: tkinter.Event):
    print(event.x, event.y)

root = tkinter.Tk()
root.bind("<Button-1>", lancer)
root.bind("<Motion>", mouvement_souris)

root.mainloop()