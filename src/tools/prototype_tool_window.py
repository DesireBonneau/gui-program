import tkinter as tk
import tkinter.messagebox
from tkinter import ttk, filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import importlib.util
import sys, os


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.insert("end", str)
        self.widget.see("end")  # Auto-scroll to bottom

    def flush(self):
        pass  # Needed for compatibility


class ToolWindowPrototype(tk.Frame):
    def __init__(self, parent, show_screen_callback, tool_name, tool_category, tool_inputs, path_to_code):
        super().__init__(parent)
        self.show_screen_callback = show_screen_callback
        self.path_to_code = path_to_code
        self.is_code_running = False

        # Checking for a valid tool_category argument
        if tool_category in {"pre_docking", "post_docking", "misc"}:
            self.tool_category = tool_category
        else:
            raise ValueError("Invalid tool_category argument. Valid arguments are: pre_docking, post_docking, misc.")


        # Default window elements (e.g. page title, home button, additional labels)
        house_image = Image.open("./data/images/house_icon.png").resize((32, 34))
        self.house_img = ImageTk.PhotoImage(house_image)
        home_button = tk.Button(self, image=self.house_img, command=lambda: show_screen_callback("home"), borderwidth=4, relief="raised", highlightthickness=0)
        label_lab = ttk.Label(self, text="MOITESSIER LABORATORY\nMCGILL UNIVERSITY",
                              font=("Helvetica Black", 12, "bold"), justify="right")
        label_app_name = ttk.Label(self, text="PROGRAM", font=("Helvetica Black", 12, "bold"))
        label_tool_name = ttk.Label(self, text=tool_name, font=("Helvetica Black", 23, "bold"))


        # Frame for all contents
        content_frame = ttk.Frame(self)


        # Frame for tool inputs
        input_frame = ttk.LabelFrame(content_frame, text="INPUTS", padding=(20, 10))
        input_frame.columnconfigure(0, weight=1)  # left spacer
        input_frame.columnconfigure(1, weight=0)  # label
        input_frame.columnconfigure(2, weight=0)  # entry
        input_frame.columnconfigure(3, weight=1)  # right spacer

        scrollable_inputs = ctk.CTkScrollableFrame(input_frame, width=370, height=220, fg_color="transparent", corner_radius=0)
        scrollable_inputs.pack(fill="both", expand=True, padx=0, pady=0)

        # Parsing the tool_inputs.txt file for inputs
        input_specs = []
        with open(f"tools/{tool_category}/inputs/{tool_inputs}") as f:
            counter = 0
            for line in f:
                # Skip empty lines, header, or comment lines
                line = line.strip()
                if not line or line.startswith("argument_name") or line.startswith("#"):
                    continue
                counter += 1
                parts = line.strip().split("|||")
                parts += [""] * (6 - len(parts))
                arg_name, arg_type, desc, browse_file, browse_dir, default = parts
                input_specs.append((arg_name, arg_type, desc, browse_file == "True", browse_dir == "True", default))

        self.inputs = {}
        for row, (arg_name, arg_type, desc, browse_file, browse_dir, default) in enumerate(input_specs):
            label_text = arg_name
            label = ttk.Label(scrollable_inputs, text=label_text)
            entry = ttk.Entry(scrollable_inputs)
            if default:
                entry.insert(0, default)
            label.grid(row=row, column=1, sticky="e", padx=15, pady=5)
            entry.grid(row=row, column=2, sticky="we", ipadx=10, padx=15, pady=3 )
            # Store (in a dict) entry by arg_name for later access
            self.inputs[arg_name] = entry

            # Add the browse button if needed
            if browse_file or browse_dir:
                def make_browse_cmd(entry=entry, browse_file=browse_file, browse_dir=browse_dir):
                    def _browse():
                        if browse_file:
                            path = filedialog.askopenfilename()
                        elif browse_dir:
                            path = filedialog.askdirectory()
                        else:
                            path = ""
                        if path:
                            entry.delete(0, "end")
                            entry.insert(0, path)
                    return _browse
                browse_btn = ttk.Button(scrollable_inputs, text="Browse", command=make_browse_cmd())
                browse_btn.grid(row=row, column=3, sticky="w", padx=8)
            scrollable_inputs.rowconfigure(row, weight=1)


        # Frame for RUN button and progress bar
        code_frame = ttk.Frame(content_frame, padding=(20, 10))
        code_frame.columnconfigure(0, weight=8)
        code_frame.columnconfigure(1, weight=0)
        code_frame.rowconfigure(0, weight=1)  # Top spacer
        code_frame.rowconfigure(1, weight=0)  # Button
        code_frame.rowconfigure(2, weight=0)  # Progressbar + Percent label
        code_frame.rowconfigure(3, weight=1)  # Top spacer

        run_button = ttk.Button(code_frame, text="RUN", style="Accent.TButton", command=self.run)
        run_button.grid(row=1, column=0,columnspan=2, sticky="ew", ipadx=20, ipady=35, pady=(0, 10))

        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(code_frame, variable=self.progress_var, maximum=100, mode="determinate")
        self.progress_bar.grid(row=2, column=0, sticky="ew", pady=(15, 10))

        self.percent_lbl = ttk.Label(code_frame, text="0%")
        self.percent_lbl.grid(row=2, column=1, sticky="ew", padx=(20, 0))


        # Frame for shell output
        shell_frame = ctk.CTkFrame(content_frame, fg_color="transparent", corner_radius=0)
        shell_label = ctk.CTkLabel(
            shell_frame,
            text="TERMINAL OUTPUT",
            font=("Helvetica Black", 13, "bold"),
            text_color="#232629",  # or any color you want
            anchor="w"
        )
        shell_label.pack(anchor="w", padx=2)
        self.shell_textbox = ctk.CTkTextbox(
            shell_frame,
            height=180,
            font=("Consolas", 12),
            fg_color="#f9f9f9",
            text_color="#232629",
            wrap="word"
        )
        self.shell_textbox.pack(fill="both", expand=True, padx=0, pady=0)


        # Root frame layout
        home_button.place(relx=0.0, x=20, y=20, anchor="nw")
        label_app_name.place(relx=0.0, x=65, y=25, anchor="nw")
        label_lab.place(relx=1.0, x=-20, y=20, anchor="ne")
        label_tool_name.pack(pady=(120, 30))

        content_frame.pack(padx=0, pady=0, fill="both", expand=True)  # pack in the root frame
        # Set columns: [0] for input_frame, [1] for code_frame
        content_frame.grid_columnconfigure(0, minsize=400, weight=1)
        content_frame.grid_columnconfigure(1, minsize=350, weight=1)
        # Set rows: [0] for input/code, [1] for shell
        content_frame.grid_rowconfigure(0, minsize=300, weight=1)
        content_frame.grid_rowconfigure(1, minsize=180, weight=1) # weight=1 to grow vertically when the window is resized

        # Place frames in the content_frame
        input_frame.grid(row=0, column=0, padx=(45, 40), pady=(15, 30), sticky="nsew")
        input_frame.config(width=400, height=260)  # Adjust as needed
        input_frame.grid_propagate(False)  # Prevents auto-resizing
        code_frame.grid(row=0, column=1, padx=(40, 30), pady=(15, 30), sticky="nsew")
        shell_frame.grid(row=1, column=0, columnspan=2, padx=30, pady=(0, 30), sticky="ew")



    def _go_pressed(self, callback):
        # Closure to pass input values when GO is pressed
        def _wrapped():
            values = {name: ent.get() for name, ent in self.inputs.items()}
            if callback:
                callback(values, self)
        return _wrapped


    def run(self):
        """
        Command to run the code in the specified path_to_code.

        :return:
        """
        if self.is_code_running:
            if tk.messagebox.askyesno("Confirm", "Run again?"):
                self.is_code_running = False
                # Reset progress bar and label?

        if not self.is_code_running:
            path_to_code = self.path_to_code
            module_name = os.path.splitext(os.path.basename(path_to_code))[0]

            # ---- Redirecting stdout/stderr ----
            self.shell_textbox.delete("1.0", "end")  # Clear previous output
            sys.stdout = TextRedirector(self.shell_textbox, "stdout")
            sys.stderr = TextRedirector(self.shell_textbox, "stderr")
            # -----------------------------------
            try:
                spec = importlib.util.spec_from_file_location(module_name, path_to_code)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                # Check if the module has a main() function
                if hasattr(module, "main"):
                    input_values = {name: entry.get() for name, entry in self.inputs.items()}
                    module.main(**input_values)
                    self.is_code_running = True
                else:
                    print("No main() function found in the code file!")

            finally:
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__


    def update_progress(self, percent):
        # NEED TO UPDATE PROGRESS IN RUN?
        # To be called by the tool's backend function, e.g., inside tqdm loop
        self.progress_var.set(percent)
        self.percent_lbl.config(text=f"{int(percent)}%")
        self.update_idletasks()