from ..prototype_tool_window import ToolWindowPrototype

class FAKEPredictorWindow(ToolWindowPrototype):
    def __init__(self, parent, show_screen_callback):
        # You can specify tool name and number of inputs for this tool
        super().__init__(parent, show_screen_callback, tool_name="Fake PREDICTOR", num_inputs=5)
        # You can customize more here: set input names, add extra widgets, override RUN, etc.

    def RUN(self):
        # Here you write the code to actually run your tool
        print("Running Fake PREDICTOR!")
        # If you want, call super().RUN() for any shared behavior
