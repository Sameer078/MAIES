from crewai.tools import BaseTool
from eda_multiagent.core.dataset_manager import load_dataset
from statsmodels.stats.outliers_influence import variance_inflation_factor
from eda_multiagent.core.memory import Memory

class MulticollinearityTool(BaseTool):
    name: str = "Multicollinearity Tool"
    description: str = "Calculates VIF scores for numeric columns."

    def _run(self, file_path: str) -> dict:
        manager = load_dataset(file_path)
        df = manager.get_df()
        numeric_df = df.select_dtypes(include="number").dropna()
        if numeric_df.shape[1] < 2:
            return {"warning": "Not enough numeric columns."}
        X = numeric_df.values
        vif_scores = {numeric_df.columns[i]: float(variance_inflation_factor(X, i)) for i in range(numeric_df.shape[1])}
        Memory.update("tools", {"multicollinearity": vif_scores})

        return {"vif_scores": vif_scores}
