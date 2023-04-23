from tqdm import tqdm

class ProgressBar:
    
    def __init__(self, max_value) -> None:
        self.max_value = max_value
        self.p = self.pbar()

    # Creates the progress bar
    def pbar(self) -> None:
        return tqdm(total=self.max_value)

    # Updates the progress bar
    def update(self, update_value) -> int:
        self.p.update(update_value)
    
    # Sets the description of the progress bar
    def set_desc(self, set_desc) -> str:
        self.p.set_description(set_desc)
        
    # Closes the progress bar
    def close(self):
        self.p.close()