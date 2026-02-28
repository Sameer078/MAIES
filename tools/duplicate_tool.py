from crewai.tools import BaseTool
from eda_multiagent.core.dataset_manager import load_dataset
from eda_multiagent.core.memory import Memory

class DuplicateTool(BaseTool):
    name: str = "Duplicate Detection Tool"
    description: str = "Counts duplicate rows in dataset."

    def _run(self, file_path: str) -> dict:
        manager = load_dataset(file_path)
        df = manager.get_df()
        result = {"duplicate_rows": int(df.duplicated().sum())}
        Memory.update("tools", result)
        return result
