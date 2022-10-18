from PIL import Image, ImageTk
from tkinter import *
import requests
from io import BytesIO
import pandas as pd
import time


df = pd.read_csv("data.csv")

# Create an instance of tkinter window
win = Tk()

# Define the geometry of the window
win.geometry("700x500")

frame = Frame(win, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

for url in df["post_url"]:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    # Create a Label Widget to display the text or Image
    label = Label(frame, image=img)
    label.pack()

win.mainloop()



