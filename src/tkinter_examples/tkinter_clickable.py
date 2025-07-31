import tkinter as tk
from tkinter import messagebox

class MyGUI:
    # constructor to initialize the GUI
    def __init__(self):
        self.root = tk.Tk()

        # for a menu bar at the top of the window
        self.menubar = tk.Menu(self.root)
        # sub-menus
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        # only one Tk() instance can be created at once so look into tk.Toplevel() for creating new windows
        # self.filemenu.add_command(label="New Window", command=self.new_window)
        # self.filemenu.add_separator()
        self.filemenu.add_command(label="Close", command=self.on_closing)
        # the problem with that command is that it closes every open tabs if you have previosuly clicked on 'New Window'
        self.filemenu.add_command(label="Kill whole process", command=exit)

        # adding the sub-menus to the main menu bar
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # actually adding the menu bar to the window?
        self.root.config(menu=self.menubar)

        self.root.geometry("800x180")

        # am i supposed to use '' or ""? i thought that '' were only for characters
        self.text = tk.Label(self.root, text='Write below:', font=('Arial', 10))
        self.text.pack(padx=20, pady=10)

        self.textbox = tk.Text(self.root, height=3, font=('Arial', 10))
        # for the textbox to be checked or not with keyboard keys (as well as clicking it)
        # should that be binded to the textbox or else?
        # problem here is that everytime I would click the letter 'u' it would actually add 'u' to the textbox
        # if I make it Ctrl + u then it would not add 'u' to the textbox BUT the event state would different based on user's OS
        self.textbox.bind("<KeyPress>", self.shortcut)
        self.textbox.pack(padx=20, pady=5)

        # the variable which contains the bool state of the checkbox (clicked or not)
        # why IntVar instead of BoolVar?
        self.is_checkbox_checked = tk.BooleanVar()

        self.checkbox = tk.Checkbutton(self.root, text='Display on the screen?', font=('Arial', 10), variable=self.is_checkbox_checked)
        self.checkbox.place(x=267, y=120)

        self.button = tk.Button(self.root, text="Run", font=('Arial', 10), command=self.show_message)
        self.button.place(x=533, y=120)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def show_message(self):
        if self.is_checkbox_checked.get():
            messagebox.showinfo(title="Message", message=self.textbox.get(1.0, tk.END))
        else:
            print(self.textbox.get("1.0", tk.END))

        # go through the difference between 1.0 and 2.0 + what the possible endings are (essentially go through the possible paramaters)
        # self.textbox.get("1.0", tk.END)

    def shortcut(self, event):
        print(event.keysym)
        #print(event.state)

        # but the state is differnt based on user's OS
        if event.keysym.lower() == 'u' and (event.state & 0x4):
            self.show_message()


    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            print("Thank you for using the McGill Chemistry application!")
            self.root.destroy()

    def new_window(self):
        MyGUI()  # Create a new instance of MyGUI to open a new window


MyGUI()
