import tkinter as tk
from tkinter import ttk


class HomeWindow(tk.Frame):
    def __init__(self, parent, show_screen_callback):
        """
        Create the root window for the application.

        Finish docstrings.
        """
        super().__init__(parent)
        self.show_screen_callback = show_screen_callback

        # Labels
        label_lab = ttk.Label(self, text="MOITESSIER LABORATORY\nMCGILL UNIVERSITY",
                          font=("Helvetica Black", 12, "bold"), justify="right")
        label_app_name = ttk.Label(self, text="GATE", font=("Helvetica Black", 52, "bold"))

        # Main button frame
        button_frame = ttk.Frame(self)
        button_frame.columnconfigure(0)
        button_frame.columnconfigure(1)
        button_frame.columnconfigure(2)

        # Main buttons
        button_pre_docking = ttk.Button(button_frame, text="PRE-DOCKING", style="Accent.TButton", command=lambda: self.show_screen_callback("pre_docking"))
        button_post_docking = ttk.Button(button_frame, text="POST-DOCKING", style="Accent.TButton", command=lambda: self.show_screen_callback("post_docking"))
        button_misc = ttk.Button(button_frame, text="MISCELLANEOUS", style="Accent.TButton", command=lambda: self.show_screen_callback("misc"))

        # Secondary buttons
        button_credits = ttk.Button(self, text="Credits", command=lambda: self.show_screen_callback("credits"))

        # Window layout
        label_lab.place(relx=1.0, x=-20, y=20, anchor="ne")
        label_app_name.pack(pady=(230, 40))

        button_frame.pack()

        button_pre_docking.grid(row=0, column=0, ipadx=15, ipady=15, padx=30, sticky="ew")
        button_post_docking.grid(row=0, column=1, ipadx=15, ipady=15, padx=30, sticky="ew")
        button_misc.grid(row=0, column=2, ipadx=15, ipady=15, padx=30, sticky="ew")

        button_credits.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")


    def show_screen_callback(self, window_class):
        """
        Switch frame to a designated window class.

        Args:
            window_class: The class of the window to go to.
        """


# To test:
if __name__ == "__main__":
    app = type('App', (), {})()  # Create a simple object to hold the root
    HomeWindow()
    # This will create and display the root window with the specified theme.