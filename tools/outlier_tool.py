from crewai.tools import BaseTool
from eda_multiagent.core.dataset_manager import load_dataset
from eda_multiagent.core.memory import Memory

class OutlierTool(BaseTool):
    name: str = "Outlier Detection Tool"
    description: str = "Detects outliers using IQR method for numeric columns."

    def _run(self, file_path: str) -> dict:
        manager = load_dataset(file_path)
        df = manager.get_df()
        numeric_df = df.select_dtypes(include="number")
        outlier_counts = {}
        for col in numeric_df.columns:
            Q1 = numeric_df[col].quantile(0.25)
            Q3 = numeric_df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outliers = numeric_df[(numeric_df[col] < lower) | (numeric_df[col] > upper)]
            outlier_counts[col] = len(outliers)
        result = {"outlier_counts": outlier_counts}
        Memory.update("tools", result)
        return result