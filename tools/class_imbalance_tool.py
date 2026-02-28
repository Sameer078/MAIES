from crewai.tools import BaseTool
from eda_multiagent.core.dataset_manager import load_dataset
import pandas as pd
from eda_multiagent.core.memory import Memory

class ClassImbalanceTool(BaseTool):
    name: str = "Class Imbalance Detection Tool"
    description: str = "Detects class imbalance for categorical target column."

    def _run(self, file_path: str, target_column: str) -> dict:
        manager = load_dataset(file_path)
        df = manager.get_df()

        if target_column not in df.columns:
            return {"error": "Target column not found."}

        if not pd.api.types.is_string_dtype(df[target_column]) and not pd.api.types.is_categorical_dtype(df[target_column]):
            return {"error": "Target is not categorical (string) type."}

        dist = df[target_column].value_counts(normalize=True)
        n_classes = len(dist)

        expected_share = 1 / n_classes

        threshold = expected_share * 0.5

        is_imbalanced = bool(dist.min() < threshold)
        result = {
            "distribution": dist.to_dict(),
            "num_classes": n_classes,
            "expected_share": round(expected_share, 4),
            "threshold": round(threshold, 4),
            "is_imbalanced": is_imbalanced
        }
        Memory.update("tools", {"class_imbalance": result})
        return result
