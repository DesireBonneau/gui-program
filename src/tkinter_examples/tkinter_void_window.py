import tkinter as tk

# to create a window
root = tk.Tk()


root.geometry("800x350")

# sets a title for the window
root.title("My First GUI")

# creates a label widget
label = tk.Label(root, text="Hello World!", font=('Arial', 24))
# shows the label on the window? The pading is the space around the label (pady is vertical spacing - starting from under the last widget)
label.pack(padx=20, pady=10)

# literally a basic textbox
textbox = tk.Text(root, height=3, font=('Arial', 16))
textbox.pack()

# single entry field (like a single line textbox)
myentry = tk.Entry(root, font=('Arial', 10))
myentry.pack(padx=20, pady=10)

# creates a button widget
mybutton = tk.Button(root, text="GO!", font=('Arial', 10))
mybutton.pack(padx=20, pady=10)

# actually for the grid layout for the tool cells USE THIS
buttonframe = tk.Frame(root)
# add a line for each of the columns
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)
buttonframe.columnconfigure(2, weight=1)

btn1 = tk.Button(buttonframe, text="1", font=('Arial', 10))
btn1.grid(row=0, column=0)

btn2 = tk.Button(buttonframe, text="2", font=('Arial', 10))
btn2.grid(row=0, column=1)

btn3 = tk.Button(buttonframe, text="3", font=('Arial', 10))
btn3.grid(row=0, column=2)

btn4 = tk.Button(buttonframe, text="4", font=('Arial', 10))
btn4.grid(row=1, column=0)

btn5 = tk.Button(buttonframe, text="5", font=('Arial', 10))
btn5.grid(row=1, column=1)

buttonframe.pack(fill='x')

anotherbutton = tk.Button(root, text="TEST")
anotherbutton.place(x=200, y=300)

# stack is for placing stuff relative to the last widget
# place is for placing stuff at a specific position (x, y) in the window


# for the window to open (needs to be at the end)
root.mainloop()