import pandas as pd

class DatasetManager:
    _instance = None

    def __new__(cls, file_path: str = None):
        if cls._instance is None:
            cls._instance = super(DatasetManager, cls).__new__(cls)
            cls._instance._df = None
            cls._instance._file_path = file_path
        return cls._instance

    def load(self, file_path: str):
        if self._df is None or self._file_path != file_path:
            self._file_path = file_path
            self._df = pd.read_csv(file_path)
        return self._df

    def get_df(self):
        if self._df is None:
            raise ValueError("Dataset not loaded.")
        return self._df

def load_dataset(file_path):
    manager = DatasetManager()
    manager.load(file_path)
    return manager
