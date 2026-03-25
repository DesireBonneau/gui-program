# progress_patch.py
from tqdm import tqdm as _tqdm

# Global variable, will be set once in main.py
GLOBAL_PROGRESSBAR = None

class TqdmTk(_tqdm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if GLOBAL_PROGRESSBAR is not None and self.total:
            GLOBAL_PROGRESSBAR["maximum"] = self.total
            GLOBAL_PROGRESSBAR["value"] = 0
            self.progressbar = GLOBAL_PROGRESSBAR
        else:
            self.progressbar = None

    def update(self, n=1):
        super().update(n)
        if self.progressbar is not None:
            self.progressbar["value"] = self.n
            self.progressbar.update_idletasks()

def apply_patch(progressbar):
    global GLOBAL_PROGRESSBAR
    GLOBAL_PROGRESSBAR = progressbar
    import tqdm
    tqdm.tqdm = TqdmTk
