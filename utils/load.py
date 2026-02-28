from eda_multiagent.core.dataset_manager import load_dataset

def dataset_snapshot(path: str):
    manager = load_dataset(path)
    df = manager.get_df()
    numeric_cols = list(df.select_dtypes(include="number").columns)
    categorical_cols = list(df.select_dtypes(include=["object", "category"]).columns)
    id_like = [c for c in df.columns if df[c].nunique() / len(df) > 0.95]
    return {
        "shape": {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
        },
        "columns": list(map(str, df.columns)),
        "dtypes": {str(k): str(v) for k, v in df.dtypes.items()},
        "sample": df.head(5).astype(str).to_dict(orient="list"),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "id_like_columns": id_like
    }