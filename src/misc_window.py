import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter as ctk
from textwrap import wrap
import os
# At top of misc_window.py / pre_docking_window.py / post_docking_window.py
try:
    from idlelib.tooltip import Hovertip  # stdlib tooltip
except Exception:
    Hovertip = None  # fallback if not available (rare)


import os

def read_tool_description(input_path: str) -> str | None:
    # Reads first line like:  "# description: your text..."
    if not input_path:
        return None
    for candidate in (input_path, os.path.join(os.getcwd(), input_path)):
        if os.path.isfile(candidate):
            try:
                with open(candidate, "r", encoding="utf-8") as f:
                    for line in f:
                        s = line.strip()
                        if s.lower().startswith("# description:"):
                            return s.split(":", 1)[1].strip()
            except Exception:
                pass
    return None


class MiscellaneousWindow(tk.Frame):
    def __init__(self, parent, show_screen_callback, tool_configs):
        """
        Create the miscellaneous window for the application.

        Args:
            parent: The parent widget.
            show_screen_callback: Callback function to switch screens.
        """
        super().__init__(parent)
        self.show_screen_callback = show_screen_callback
        self.tool_configs = tool_configs

        # Load the home image
        house_image = Image.open("data/images/house_icon.png").resize((32, 34))
        self.house_img = ImageTk.PhotoImage(house_image)

        # Home button
        home_button = tk.Button(self, image=self.house_img, command=lambda: show_screen_callback("home"), borderwidth=4, relief="raised", highlightthickness=0)

        # Labels
        label_lab = ttk.Label(self, text="MOITESSIER LABORATORY\nMCGILL UNIVERSITY",
                              font=("Helvetica Black", 12, "bold"), justify="right")
        label_app_name = ttk.Label(self, text="PROGRAM", font=("Helvetica Black", 12, "bold"))
        label_pre_docking = ttk.Label(self, text="MISCELLANEOUS", font=("Helvetica Black", 35, "bold"))


        # Scrollable tool button frame
        scrollable_tool_frame = ctk.CTkScrollableFrame(self, width=1000, height=600, corner_radius=0, fg_color="transparent")
        scrollable_tool_frame.columnconfigure(0, weight=1)
        scrollable_tool_frame.columnconfigure(1, weight=0)
        scrollable_tool_frame.columnconfigure(2, weight=0)
        scrollable_tool_frame.columnconfigure(3, weight=0)
        scrollable_tool_frame.columnconfigure(4, weight=1)

        # Tools buttons
        # --- NEW: Add buttons automatically in grid, 3 per row ---
        buttons_per_row = 3
        max_chars_per_line = 20

        for row_start in range(0, len(self.tool_configs), buttons_per_row):
            row_tools = self.tool_configs[row_start:row_start + buttons_per_row]
            labels = []
            max_lines = 1

            # Wrap and collect lines for each button in the row
            for tool in row_tools:
                lines = wrap(tool["button_label"], max_chars_per_line)
                labels.append(lines)
                if len(lines) > max_lines:
                    max_lines = len(lines)

            # Pad labels and create buttons
            for col, (tool, lines) in enumerate(zip(row_tools, labels)):
                # Pad with blank lines so all in the row have equal height
                padded_label = '\n'.join(lines + [''] * (max_lines - len(lines)))
                padx = (75, 50) if col == 0 else 50

                btn = ttk.Button(
                    scrollable_tool_frame,
                    text=padded_label,
                    style="Accent.TButton",
                    width=18,  # Adjust width as needed to match post-docking
                    command=lambda wn=tool["window_name"]: show_screen_callback(wn),
                )

                # Decide tooltip text: prefer explicit config, else try the .txt header, else the tool name
                tooltip_text = (
                        tool.get("description")
                        or read_tool_description(tool.get("toolwindow_kwargs", {}).get("tool_inputs"))
                        or tool.get("toolwindow_kwargs", {}).get("tool_name")
                        or tool.get("button_label")
                )

                if Hovertip and tooltip_text:
                    Hovertip(btn, tooltip_text, hover_delay=500)

                btn.grid(
                    row=row_start // buttons_per_row, column=col + 1,
                    ipadx=25, ipady=10 * max_lines,  # More vertical space for multiline
                    padx=padx, pady=(0, 25) if row_start == 0 else 25,
                )


        # Window layout
        home_button.place(relx=0.0, x=20, y=20, anchor="nw")
        label_app_name.place(relx=0.0, x=65, y=25, anchor="nw")
        label_lab.place(relx=1.0, x=-20, y=20, anchor="ne")
        label_pre_docking.pack(pady=(120, 30))

        scrollable_tool_frame.pack(pady=20)


    #  SCROLLBAR NOTES: NOT SMOOTH UPON SCROLLING