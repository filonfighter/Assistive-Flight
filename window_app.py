# importing libraries
import tkinter as tk
from tkinter import *
import pyglet
from PIL import Image, ImageTk
from datetime import datetime
import requests
import time

# creating main window 
root = tk.Tk()
root.title("Assitive Flight")
root.geometry("700x700")
root.iconbitmap("icon.ico")
root.resizable(False, False)

# importing font
font_file = "Paperboard.ttf"
font_name = "Paperboard"
pyglet.font.add_file(font_file)

"""# get the current time
now = datetime.now()
current_time = now.strftime("%H:%M")
print("Current Time =", current_time)
"""

# creating gradient label
def create_gradient_label(canvas, text, font, x, y, width, height, start_color, end_color):
    
    # Create a gradient from start_color to end_color
    for i in range(width):

        # getting the rgb values of the start and end colors
        r1, g1, b1 = canvas.winfo_rgb(start_color)
        r2, g2, b2 = canvas.winfo_rgb(end_color)
        
        # changing the color
        r = int(r1 + (r2 - r1) * i / width)
        g = int(g1 + (g2 - g1) * i / width)
        b = int(b1 + (b2 - b1) * i / width)
        
        # creating the color
        color = f'#{r>>8:02x}{g>>8:02x}{b>>8:02x}'
        canvas.create_line(x + i, y, x + i, y + height, fill=color)

    # Add text to the canvas
    canvas.create_text(x + width // 2, y + height // 2, text=text, fill="white", font=font)



canvas = tk.Canvas(root, width=700, height=700)
canvas.pack()

create_gradient_label(canvas, text=" ", font=(font_name, 17, "bold"), x=0, y=0, width=700, height=700, start_color="blue", end_color="#a300cc")

"""label2 = Label(root, height=70, width=3, bg="blue")
label2.place(x=0, y=2)
label3 = Label(root, height=70, width=6, bg="#a300cc")
label3.place(x=670, y=2)"""

"""
Label5 = Label(root,text="Money Saved: ", bd=4, width=15, font=(font_name,16, "bold"))
Label5.place(x=100, y=100)
Label6 = Label(root,text="14.197.12💸", bd=4, width=15, font=(font_name,16, "bold"))
Label6.place(x=100, y=150)
"""


"""
Label8 = Label(root,text="Time Saved: ", bd=4, width=10, font=(font_name,16, "bold"))
Label8.place(x=450, y=100)
Label6 = Label(root,text="2861h⌛", bd=4, width=10, font=(font_name,16, "bold"))
Label6.place(x=450, y=150)
"""
# entry - text input
Entry = tk.Entry(root, bd="4", width=10, font="Hervelica 12 bold")
Entry.place(x=140, y=290)

# labels
Label4 = Label(root,text="Insert time [HH:MM]: ", bg="white", bd=4, width=15, font="Hervelica 12 bold")
Label4.place(x=116, y=260)

# small white background
small_canvas = tk.Canvas(canvas, width=300, height=350, bg="white")
small_canvas.place(x=40, y=230)

# mapka
mapka = tk.Canvas(canvas, width=300, height=350, bg="white")
mapka.place(x=370, y=230)

# gates on map
A1 =  Label(canvas, text="A1", bg="white", font="Helvetica 13 bold", fg="green")
A1.place(x=382, y=500)

A2 =  Label(canvas, text="A2", bg="white", font="Helvetica 13 bold", fg="green")
A2.place(x=637, y=500)

B1 =  Label(canvas, text="B1", bg="white", font="Helvetica 13 bold", fg="purple")
B1.place(x=382, y=370)

B2 =  Label(canvas, text="B2", bg="white", font="Helvetica 13 bold", fg="purple")
B2.place(x=637, y=370)

B1 =  Label(canvas, text="C1", bg="white", font="Helvetica 13 bold", fg="red")
B1.place(x=382, y=240)

C2 =  Label(canvas, text="C2", bg="white", font="Helvetica 13 bold", fg="red")
C2.place(x=637, y=240)

# people on map
guy = Label(canvas, bg="red", width=1, height=1)
guy.place(x=560, y=400)

guy2 = Label(canvas, bg="green", width=1, height=1)
guy2.place(x=470, y=290)
           
guy3 = Label(canvas, bg="purple", width=1, height=1)
guy3.place(x=470, y=510)

# creating function for sending data
def Send():

    #print("Button Clicked")
    
    # Defining channel Write API Key
    api_key = "QGIU9SDZRRQQRG4O"
    
    # Defining channel ID
    channel_id = "2553609"

    # Defining the base URL for the ThinkSpeak API
    base_url = f"https://api.thingspeak.com/update?api_key={api_key}"

    def send_data(field1):
        
        # Creating the URL with the data fields to be sent
        url = f"{base_url}&field1={field1}"
        response = requests.get(url)
        if response.status_code == 200:
            print("Data sent successfully.")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    print("Time: " + Entry.get())
    entered_time_str = Entry.get()
    now = datetime.now()
    current_time_str = now.strftime("%H:%M")
        
    # Parsing the entered time
    entered_time = datetime.strptime(entered_time_str, "%H:%M")
        
    # Converting entered time to current day's datetime for comparison
    entered_time = now.replace(hour=entered_time.hour, minute=entered_time.minute, second=0, microsecond=0)
        
    # Calculating the time difference in minutes
    time_difference = (entered_time - now).total_seconds() / 60
    time_difference = int(time_difference)
        
    print(f"Time Difference in minutes: {time_difference}")

    for i in range(1, time_difference):
        time.sleep(60)
        print(time_difference - i)
        send_data(time_difference - i)

    # sending gates informations
    send_data(time_difference)
    if CheckVar.get() == 1:
        print("A1")
        send_data("A1")
    if CheckVar2.get() == 1:
        print("Gr.1")
        send_data("Gr.1")
    if CheckVar3.get() == 1:
        print("Gr.2")
        send_data("Gr.2")
    if CheckVar4.get() == 1:
        print("Gr.3")
        send_data("Gr.3")
    if CheckVar5.get() == 1:
        print("B1")
        send_data("B1")
    if CheckVar6.get() == 1:
        print("Gr.1")
        send_data("Gr.1")
    if CheckVar7.get() == 1:
        print("Gr.2")
        send_data("Gr.2")
    if CheckVar8.get() == 1:
        print("Gr.3")
        send_data("Gr.3")
    if CheckVar9.get() == 1:
        print("C1")
        send_data("C1")
    if CheckVar10.get() == 1:
        print("Gr.1")
        send_data("Gr.1")
    if CheckVar11.get() == 1:
        print("Gr.2")
        send_data("Gr.2")
    if CheckVar12.get() == 1:
        print("Gr.3")
        send_data("Gr.3")

# creating binding functions
def on_enter(e):
    button['background'] = 'blue'
    button['foreground'] = 'white'
     
def on_leave(e):
    button['background'] = 'white'
    button['foreground'] = 'black'

def on_enter2(e):
    button2['background'] = 'purple'
    button2['foreground'] = 'white'
     
def on_leave2(e):
    button2['background'] = 'white'
    button2['foreground'] = 'black'

# creating variables for checkboxes
CheckVar= IntVar()
CheckVar2 = IntVar()
CheckVar3= IntVar()
CheckVar4 = IntVar()
CheckVar5= IntVar()
CheckVar6 = IntVar()

CheckVar7 = IntVar()
CheckVar8 = IntVar()
CheckVar9 = IntVar()
CheckVar10 = IntVar()
CheckVar11 = IntVar()
CheckVar12 = IntVar()
CheckVar13 = IntVar()
CheckVar14 = IntVar()


# creating checkboxes
c1 = Checkbutton(root, text="A1", variable=CheckVar, onvalue=1, offvalue=0, height=3, width=3, bg="white", fg="green", font="Helvetica 12 bold")
c1.place(x=70, y=360)

c2 = Checkbutton(root, text="Gr.1", variable=CheckVar2, onvalue=1, offvalue=0, height=3, width=3, bg="white", fg="green", font="Helvetica 10 bold")
c2.place(x=70, y=420)
c3 = Checkbutton(root, text="Gr.2", variable=CheckVar3, onvalue=1, offvalue=0, height=3, width=3, bg="white", fg="green", font="Helvetica 10 bold")
c3.place(x=70, y=470)
c4 = Checkbutton(root, text="Gr.3", variable=CheckVar4, onvalue=1, offvalue=0, height=3, width=3, bg="white", fg="green", font="Helvetica 10 bold")
c4.place(x=70, y=520)

c5 = Checkbutton(root, text="B1", variable=CheckVar5, onvalue=1, offvalue=0, height=3, width=3, bg="white", fg="purple", font="Helvetica 12 bold")
c5.place(x=170, y=360)

c6 = Checkbutton(root, text="Gr.1", variable=CheckVar6, onvalue=1, offvalue=0, height=3, width=3, bg="white", fg="purple",  font="Helvetica 10 bold")
c6.place(x=170, y=420)
c7 = Checkbutton(root, text="Gr.2", variable=CheckVar7, onvalue=1, offvalue=0, height=3, width=3, bg="white", fg="purple",  font="Helvetica 10 bold")
c7.place(x=170, y=470)
c8 = Checkbutton(root, text="Gr.3", variable=CheckVar8, onvalue=1, offvalue=0, height=3, width=3, bg="white", fg="purple",  font="Helvetica 10 bold")
c8.place(x=170, y=520)


c9 = Checkbutton(root, text="C1", variable=CheckVar9, onvalue=1, offvalue=0, height=3, width=3, bg="white", fg="red", font="Helvetica 12 bold")
c9.place(x=270, y=360)

c10 = Checkbutton(root, text="Gr.1", variable=CheckVar10, onvalue=1, offvalue=0, height=3, width=3, bg="white", fg="red",  font="Helvetica 10 bold")
c10.place(x=270, y=420)

c11 = Checkbutton(root, text="Gr.2", variable=CheckVar11, onvalue=1, offvalue=0, height=3, width=3, bg="white", fg="red",  font="Helvetica 10 bold")
c11.place(x=270, y=470)

c12 = Checkbutton(root, text="Gr.3", variable=CheckVar12, onvalue=1, offvalue=0, height=3, width=3, bg="white", fg="red",  font="Helvetica 10 bold")
c12.place(x=270, y=520)

# creating buttons and binding them
button = tk.Button(root, command=Send, text="Submit", padx=20, pady=10, fg="black", bg="white", font="Hervelica 12 bold")
button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)
button.place(x=135, y=600)

button2= tk.Button(root, text="Map", padx=20, pady=10, fg="black", bg="white", font="Hervelica 12 bold")
button2.bind("<Enter>", on_enter2)
button2.bind("<Leave>", on_leave2)
button2.place(x=480, y=600)

# title label
text = Label(root, text="Assistive Flight", font=(font_name, 17,"bold"), bg="#5900b3", fg="white", height=2, width=53)
text.place(x=2, y=2)


# running the main loop
root.mainloop()

