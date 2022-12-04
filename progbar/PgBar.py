from tqdm import tqdm

class PgBar:
    
    def __init__(self, max_value) -> None:
        self.max_value = max_value
        self.p = self.pbar()

    def pbar(self) -> None:
        return tqdm(total=self.max_value)

    def update(self, update_value) -> int:
        self.p.update(update_value)
    
    def set_desc(self, set_desc) -> str:
        self.p.set_description(set_desc)
        
    def close(self):
        self.p.close()