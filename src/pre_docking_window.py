import tkinter as tk
from tkinter import ttk, Canvas
from PIL import Image, ImageTk
from tools.prototype_tool_window import ToolWindowPrototype
import customtkinter as ctk


class PreDockingWindow(tk.Frame):
    def __init__(self, parent, show_screen_callback, tool_list=None, max_tool_width=None):
        """
        Create the pre-docking window for the application.

        Args:
            parent: The parent widget.
            show_screen_callback: Callback function to switch screens.
        """
        super().__init__(parent)
        self.show_screen_callback = show_screen_callback
        self.tool_list = tool_list
        self.max_tool_width = max_tool_width

        # Load the home image
        house_image = Image.open("data/images/house_icon.png").resize((32, 34))
        self.house_img = ImageTk.PhotoImage(house_image)

        # Home button
        home_button = tk.Button(self, image=self.house_img, command=lambda: show_screen_callback("home"), borderwidth=4, relief="raised", highlightthickness=0)

        # Labels
        label_lab = ttk.Label(self, text="MOITESSIER LABORATORY\nMCGILL UNIVERSITY",
                              font=("Helvetica Black", 12, "bold"), justify="right")
        label_app_name = ttk.Label(self, text="PROGRAM", font=("Helvetica Black", 12, "bold"))
        label_pre_docking = ttk.Label(self, text="PRE-DOCKING", font=("Helvetica Black", 35, "bold"))


        # Tool button frame
        tool_frame = ttk.Frame(self)
        tool_frame.columnconfigure(0)
        tool_frame.columnconfigure(1)
        tool_frame.columnconfigure(2)

        # Scrollable tool button frame
        scrollable_tool_frame = ctk.CTkScrollableFrame(self, width=1000, height=600, corner_radius=0, fg_color="transparent")
        scrollable_tool_frame.columnconfigure(0, weight=1)
        scrollable_tool_frame.columnconfigure(1, weight=0)
        scrollable_tool_frame.columnconfigure(2, weight=0)
        scrollable_tool_frame.columnconfigure(3, weight=0)
        scrollable_tool_frame.columnconfigure(4, weight=1)

        # Tools buttons
        # --- ADD MORE TOOLS' TITLES IN main.py ---
        # --- THIS IS WHERE YOU CAN ADD MORE TOOLS USING THE PROTOTYPE DESIGN PATTERN ---
        button_tool1 = ttk.Button(scrollable_tool_frame, text=self.tool_list[1], style="Accent.TButton", width=self.max_tool_width)
        button_tool2 = ttk.Button(scrollable_tool_frame, text=self.tool_list[2], style="Accent.TButton", width=self.max_tool_width)
        button_tool3 = ttk.Button(scrollable_tool_frame, text=self.tool_list[3], style="Accent.TButton", width=self.max_tool_width)
        button_tool4 = ttk.Button(scrollable_tool_frame, text=self.tool_list[4], style="Accent.TButton", width=self.max_tool_width)
        button_tool5 = ttk.Button(scrollable_tool_frame, text=self.tool_list[5], style="Accent.TButton", width=self.max_tool_width)
        button_tool6 = ttk.Button(scrollable_tool_frame, text=self.tool_list[6], style="Accent.TButton", width=self.max_tool_width)
        button_tool7 = ttk.Button(scrollable_tool_frame, text=self.tool_list[7], style="Accent.TButton", width=self.max_tool_width)
        button_tool8 = ttk.Button(scrollable_tool_frame, text=self.tool_list[8], style="Accent.TButton", width=self.max_tool_width)
        button_tool9 = ttk.Button(scrollable_tool_frame, text=self.tool_list[9], style="Accent.TButton", width=self.max_tool_width)
        button_tool10 = ttk.Button(scrollable_tool_frame, text=self.tool_list[10], style="Accent.TButton", width=self.max_tool_width)
        button_tool11 = ttk.Button(scrollable_tool_frame, text=self.tool_list[11], style="Accent.TButton", width=self.max_tool_width)
        button_tool12 = ttk.Button(scrollable_tool_frame, text=self.tool_list[12], style="Accent.TButton", width=self.max_tool_width)



        """
        --- TEMPLATE FOR ADDING MORE TOOLS ---
        button_tool6 = ttk.Button(scrollable_tool_frame, text=self.tool_list[6], style="Accent.TButton", width=self.max_tool_width)
        button_tool7 = ttk.Button(scrollable_tool_frame, text=self.tool_list[7], style="Accent.TButton", width=self.max_tool_width)
        button_tool8 = ttk.Button(scrollable_tool_frame, text=self.tool_list[8], style="Accent.TButton", width=self.max_tool_width)
        button_tool9 = ttk.Button(scrollable_tool_frame, text=self.tool_list[9], style="Accent.TButton", width=self.max_tool_width)
        """


        # Window layout
        home_button.place(relx=0.0, x=20, y=20, anchor="nw")
        label_app_name.place(relx=0.0, x=65, y=25, anchor="nw")
        label_lab.place(relx=1.0, x=-20, y=20, anchor="ne")
        label_pre_docking.pack(pady=(120, 30))

        scrollable_tool_frame.pack(pady=20)

        button_tool1.grid(row=0, column=1, ipadx=25, ipady=15, padx=(75,50), pady=(0, 25), sticky="ew")
        button_tool2.grid(row=0, column=2, ipadx=25, ipady=15, padx=50, pady=(0, 25), sticky="ew")
        button_tool3.grid(row=0, column=3, ipadx=25, ipady=15, padx=50, pady=(0, 25), sticky="ew")
        button_tool4.grid(row=1, column=1, ipadx=25, ipady=15, padx=(75,50), pady=25, sticky="ew")
        button_tool5.grid(row=1, column=2, ipadx=25, ipady=15, padx=50, pady=25, sticky="ew")
        button_tool6.grid(row=1, column=3, ipadx=25, ipady=15, padx=50, pady=25, sticky="ew")
        button_tool7.grid(row=2, column=1, ipadx=25, ipady=15, padx=(75, 50), pady=25, sticky="ew")
        button_tool8.grid(row=2, column=2, ipadx=25, ipady=15, padx=50, pady=25, sticky="ew")
        button_tool9.grid(row=2, column=3, ipadx=25, ipady=15, padx=50, pady=25, sticky="ew")
        button_tool10.grid(row=1, column=3, ipadx=25, ipady=15, padx=50, pady=25, sticky="ew")
        button_tool11.grid(row=2, column=1, ipadx=25, ipady=15, padx=(75, 50), pady=25, sticky="ew")
        button_tool12.grid(row=2, column=2, ipadx=25, ipady=15, padx=50, pady=25, sticky="ew")


        """
        --- TEMPLATE FOR ADDING MORE TOOLS ---
        button_tool6.grid(row=1, column=3, ipadx=25, ipady=15, padx=50, pady=25, sticky="ew")
        button_tool7.grid(row=2, column=1, ipadx=25, ipady=15, padx=(75,50), pady=25, sticky="ew")
        button_tool8.grid(row=2, column=2, ipadx=25, ipady=15, padx=50, pady=25, sticky="ew")
        button_tool9.grid(row=2, column=3, ipadx=25, ipady=15, padx=50, pady=25, sticky="ew")
        """


    #  SCROLLBAR NOTES: NOT SMOOTH UPON SCROLLING