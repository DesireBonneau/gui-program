import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter as ctk
from textwrap import wrap

# Tooltips (same approach as Misc)
try:
    from idlelib.tooltip import Hovertip
except Exception:
    Hovertip = None

import os

def read_tool_description(input_path: str) -> str | None:
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


class PreDockingWindow(tk.Frame):
    def __init__(self, parent, show_screen_callback, tool_configs, buttons_per_row=3, max_chars_per_line=20):
        """
        Create the PRE-DOCKING window with auto-generated buttons.

        Args:
            parent: Tk parent
            show_screen_callback: function(str) -> None to swap frames
            tool_configs: list[dict] like:
                {
                  "button_label": "...",
                  "window_name": "unique_name",
                  "toolwindow_kwargs": {
                      "tool_name": "...",
                      "tool_category": "pre",
                      "tool_inputs": "file.txt",
                      "path_to_code": "tools/pre_docking/some_tool.py"
                  },
                  "description": "Tooltip text here"
                }
        """
        super().__init__(parent)
        self.show_screen_callback = show_screen_callback
        self.tool_configs = tool_configs or []

        # Header UI
        house_image = Image.open("data/images/house_icon.png").resize((32, 34))
        self.house_img = ImageTk.PhotoImage(house_image)

        home_button = tk.Button(
            self, image=self.house_img,
            command=lambda: show_screen_callback("home"),
            borderwidth=4, relief="raised", highlightthickness=0
        )

        label_lab = ttk.Label(self, text="MOITESSIER LABORATORY\nMCGILL UNIVERSITY",
                              font=("Helvetica Black", 12, "bold"), justify="right")
        label_app_name = ttk.Label(self, text="PROGRAM", font=("Helvetica Black", 12, "bold"))
        label_title = ttk.Label(self, text="PRE-DOCKING", font=("Helvetica Black", 35, "bold"))

        # Scrollable grid like Misc
        scrollable_tool_frame = ctk.CTkScrollableFrame(self, width=1000, height=600, corner_radius=0, fg_color="transparent")
        for c in range(5):
            scrollable_tool_frame.columnconfigure(c, weight=1 if c in (0, 4) else 0)

        # Build buttons in rows of N
        for row_start in range(0, len(self.tool_configs), buttons_per_row):
            row_tools = self.tool_configs[row_start:row_start + buttons_per_row]
            labels_wrapped = []
            max_lines = 1

            for tool in row_tools:
                lines = wrap(tool["button_label"], max_chars_per_line)
                labels_wrapped.append(lines)
                max_lines = max(max_lines, len(lines))

            for col, (tool, lines) in enumerate(zip(row_tools, labels_wrapped)):
                padded_label = "\n".join(lines + [""] * (max_lines - len(lines)))
                padx = (75, 50) if col == 0 else 50

                btn = ttk.Button(
                    scrollable_tool_frame,
                    text=padded_label,
                    style="Accent.TButton",
                    width=18,
                    command=lambda wn=tool["window_name"]: show_screen_callback(wn),
                )

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
                    ipadx=25, ipady=10 * max_lines,
                    padx=padx, pady=(0, 25) if row_start == 0 else 25
                )

        # Layout
        home_button.place(relx=0.0, x=20, y=20, anchor="nw")
        label_app_name.place(relx=0.0, x=65, y=25, anchor="nw")
        label_lab.place(relx=1.0, x=-20, y=20, anchor="ne")
        label_title.pack(pady=(120, 30))
        scrollable_tool_frame.pack(pady=20)
