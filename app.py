import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from eda_multiagent.crew import MultiAgentEDACrew
from eda_multiagent.core.memory import Memory
from eda_multiagent.utils.load import dataset_snapshot
from eda_multiagent.utils.tool_parser import extract_tool_results, extract_outer_json

st.set_page_config(page_title="Multi-Agent Intelligent EDA System", layout="wide")
st.title("📊 Multi-Agent Intelligent EDA System")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

user_goal = st.text_area(
    "Describe your goal or what you want to extract from the data",
    placeholder="E.g., What ML technique should I apply?"
)

def render_tool_data(data):
    if isinstance(data, dict):
        try:
            df = pd.DataFrame(data)
            # Heatmap if square matrix
            if df.shape[0] == df.shape[1] and df.shape[0] > 1:
                st.dataframe(df)
                fig, ax = plt.subplots()
                cax = ax.matshow(df)
                plt.xticks(range(len(df.columns)), df.columns, rotation=90)
                plt.yticks(range(len(df.columns)), df.columns)
                fig.colorbar(cax)
                st.pyplot(fig)
            else:
                st.dataframe(df)
        except:
            for key, value in data.items():
                st.markdown(f"**{key.replace('_',' ').title()}**")
                render_tool_data(value)
    elif isinstance(data, list):
        if all(isinstance(i, dict) for i in data):
            st.dataframe(pd.DataFrame(data))
        else:
            for item in data:
                st.markdown(f"- {item}")
    else:
        st.write(data)


if st.button("Run Analysis"):
    if uploaded_file is None:
        st.warning("Please upload a CSV file.")
        st.stop()

    st.info("Running multi-agent analysis...")

    file_path = f"./tmp/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    Memory.clear()
    snapshot = dataset_snapshot(file_path)
    # Memory.set("snapshot", snapshot)
    crew = MultiAgentEDACrew().crew()

    inputs = {
        "file_path": file_path,
        "dataset_info": snapshot,
        "user_goal": user_goal
    }

    crew.kickoff(inputs=inputs)
    st.success("Analysis Completed!")

    intent_mem = Memory.get("intent")
    eda_mem = Memory.get("eda")
    insight_mem = Memory.get("insight")
    ml_mem = Memory.get("ml_strategy")
    summary_mem = Memory.get("summary")
    
    intent = extract_outer_json(intent_mem['raw']) if intent_mem else None
    eda = extract_outer_json(eda_mem['raw']) if eda_mem else None
    insights = extract_outer_json(insight_mem['raw']) if insight_mem else None
    ml = extract_outer_json(ml_mem['raw']) if ml_mem else None
    summary = extract_outer_json(summary_mem['raw']) if summary_mem else None

    tools_result = extract_tool_results(eda_mem['messages']) if eda_mem else []

    if summary:
        if summary.get("summary_text"):
            st.markdown("## 🧾 Summary")
            st.info(summary["summary_text"])

        if summary.get("key_findings"):
            st.markdown("## 🔎 Key Findings")
            for finding in summary["key_findings"]:
                st.markdown(f"- {finding}")

    if snapshot:

        st.markdown("---")
        st.header("Dataset Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            if snapshot.get("shape"):
                st.metric("Rows", snapshot["shape"].get("rows"))
        with col2:
            if snapshot.get("shape"):
                st.metric("Columns", snapshot["shape"].get("columns"))
        with col3:
            if snapshot.get("id_like_columns") is not None:
                st.metric("ID-like Columns", len(snapshot["id_like_columns"]))

        col1, col2, col3 = st.columns(3)

        with col1:
            if snapshot.get("numeric_columns"):
                st.subheader("Numeric Columns")
                for col in snapshot["numeric_columns"]:
                    st.markdown(f"- {col}")

        with col2:
            if snapshot.get("categorical_columns"):
                st.subheader("Categorical Columns")
                for col in snapshot["categorical_columns"]:
                    st.markdown(f"- {col}")

        with col3:
            if snapshot.get("id_like_columns"):
                st.subheader("ID-like Columns")
                for col in snapshot["id_like_columns"]:
                    st.markdown(f"- {col}")

        if snapshot.get("dtypes"):
            st.subheader("Data Types")
            st.json(snapshot["dtypes"])

        if snapshot.get("sample"):
            st.subheader("Sample Data")
            st.dataframe(pd.DataFrame(snapshot["sample"]))


    if intent:
        st.markdown("---")
        st.header("🎯 Intent Analysis")

        col1, col2 = st.columns(2)

        with col1:
            if intent.get("dataset_summary"):
                st.subheader("Dataset Summary")
                st.write(intent["dataset_summary"])

            if intent.get("domain"):
                st.subheader("Domain")
                st.write(intent["domain"])

            if intent.get("priority_features"):
                st.subheader("Priority Features")
                for f in intent["priority_features"]:
                    st.markdown(f"- {f}")

        with col2:
            if intent.get("user_goal_interpreted"):
                st.subheader("Goal")
                st.write(intent["user_goal_interpreted"])

            if intent.get("problem_type"):
                st.subheader("Problem Type")
                st.write(intent["problem_type"])

            if intent.get("target_column"):
                st.subheader("Target Column")
                st.write(intent["target_column"])


    if eda:
        st.markdown("---")
        st.header("📊 Exploratory Data Analysis")

        if eda.get("missing_values"):
            st.subheader("Missing Values")
            st.json(eda["missing_values"])
        else:
            st.success("No missing values detected.")

        if eda.get("duplicates") is not None:
            st.metric("Duplicate Rows", eda["duplicates"])

        if eda.get("strong_correlations"):
            st.subheader("Strong Correlations")
            for corr in eda["strong_correlations"]:
                st.markdown(f"- {corr}")

        if eda.get("data_quality_warnings"):
            st.subheader("Data Quality Warnings")
            for warning in eda["data_quality_warnings"]:
                st.warning(warning)

        if tools_result:
            st.subheader("Tool Outputs")

            for tool in tools_result:
                st.markdown("---")
                st.subheader(tool["name"].replace("_", " ").title())
                render_tool_data(tool["content"])



    if insights:
        st.markdown("---")
        st.header("🔎 Insights")

        col1, col2 = st.columns(2)

        with col1:
            if insights.get("key_findings"):
                st.subheader("Key Findings")
                for finding in insights["key_findings"]:
                    st.info(f"- {finding}")

            if insights.get("feature_ideas"):
                st.subheader("💡 Feature Engineering Ideas")
                for idea in insights["feature_ideas"]:
                    st.warning(f"- {idea}")

        with col2:
            if insights.get("risk_flags"):
                st.subheader("⚠ Risk Flags")
                for risk in insights["risk_flags"]:
                    st.error(f"- {risk}")


    if ml:
        st.markdown("---")
        st.header("🤖 Machine Learning Strategy")

        col1, col2 = st.columns(2)

        with col1:
            if ml.get("final_problem_type"):
                st.subheader("🎯 Problem Type")
                st.write(ml["final_problem_type"])

            if ml.get("recommended_target"):
                st.subheader("Recommended Target")
                st.write(ml["recommended_target"])

            if ml.get("suggested_models"):
                st.subheader("Suggested Models")
                for model in ml["suggested_models"]:
                    st.success(f"- {model}")

        with col2:
            if ml.get("preprocessing_steps"):
                st.subheader("Preprocessing Steps")
                for step in ml["preprocessing_steps"]:
                    st.warning(f"- {step}")

            if ml.get("training_risks"):
                st.subheader("Training Risks")
                for risk in ml["training_risks"]:
                    st.error(f"- {risk}")