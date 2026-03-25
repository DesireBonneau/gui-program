import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class CreditsWindow(tk.Frame):
    def __init__(self, parent, show_screen_callback, all_tools=None):
        """
        This window is for displaying the credits of the program and the different tools.

        :param parent:
        :param show_screen_callback:
        """
        super().__init__(parent)
        self.show_screen_callback = show_screen_callback

        file_content = ""
        # Load the credits text from a file
        try:
            with open('data/texts/credits.txt', 'r', encoding='utf-8') as file:
                file_content = file.read()
        except FileNotFoundError:
            file_content = "Error: The file 'credits.txt' was not found.\n"
        except Exception as e:
            file_content = f"An error occurred: {e}\n"

        if all_tools:
            file_content += "\n\n" + ("=" * 40) + "\nINDIVIDUAL TOOL CREDITS\n" + ("=" * 40) + "\n\n"
            for tool in all_tools:
                credits_text = tool.get("credits")
                if credits_text:
                    file_content += f"[{tool.get('button_label', 'Unnamed Tool')}]\n"
                    file_content += f"{credits_text}\n\n"

        # Load the home image
        house_image = Image.open("data/images/house_icon.png").resize((32, 34))
        self.house_img = ImageTk.PhotoImage(house_image)

        # Home button
        home_button = tk.Button(self, image=self.house_img, command=lambda: show_screen_callback("home"), borderwidth=4, relief="raised", highlightthickness=0)

        # Labels
        label_lab = ttk.Label(self, text="MOITESSIER LABORATORY\nMCGILL UNIVERSITY",
                              font=("Helvetica Black", 12, "bold"), justify="right")
        label_app_name = ttk.Label(self, text="PROGRAM", font=("Helvetica Black", 12, "bold"))
        label_credits = ttk.Label(self, text="CREDITS", font=("Helvetica Back", 35, "bold"))

        # Credits textbox
        credits_displayed_text = tk.Text(self, width=60, font=("Helvetica", 10), wrap="word", borderwidth=0, highlightthickness=0, relief="flat")

        # Button to go back to previous page
        # button_back = ttk.Button(text="BACK", command=lambda: self.show_screen_callback("home"))

        # Window layout
        home_button.place(relx=0.0, x=20, y=20, anchor="nw")
        label_app_name.place(relx=0.0, x=65, y=25, anchor="nw")
        label_lab.place(relx=1.0, x=-20, y=20, anchor="ne")
        label_credits.pack(pady=(120, 30))

        credits_displayed_text.pack(pady=(0, 20))
        credits_displayed_text.tag_configure("center", justify="center")
        credits_displayed_text.insert(tk.END, file_content, "center")
        credits_displayed_text.config(state=tk.DISABLED)
