from crewai.tools import BaseTool
from eda_multiagent.core.dataset_manager import load_dataset
from eda_multiagent.core.memory import Memory

class CorrelationTool(BaseTool):
    name: str = "Correlation Tool"
    description: str = "Calculates correlation matrix for numeric columns."

    def _run(self, file_path: str) -> dict:
        manager = load_dataset(file_path)
        df = manager.get_df()
        numeric_df = df.select_dtypes(include="number")
        if numeric_df.shape[1] < 2:
            result =  {"warning": "Not enough numeric columns."}
        result = {"correlation_matrix": numeric_df.corr().to_dict()}
        Memory.update("tools", result)
        return result
