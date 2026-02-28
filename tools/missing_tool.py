from crewai.tools import BaseTool
from eda_multiagent.core.dataset_manager import load_dataset
from eda_multiagent.core.memory import Memory

class MissingValueTool(BaseTool):
    name: str = "Missing Value Analysis Tool"
    description: str = "Returns missing counts and percentage per column."

    def _run(self, file_path: str) -> dict:
        manager = load_dataset(file_path)
        df = manager.get_df()
        missing_counts = df.isnull().sum()
        missing_percentage = (missing_counts / len(df)) * 100
        result = {"missing_counts": missing_counts.to_dict(),
                "missing_percentage": missing_percentage.to_dict()}
        Memory.update("tools", {"missing": result})
        return result
