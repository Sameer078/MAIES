from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, task, crew
from typing import List
from dotenv import load_dotenv
import os
from eda_multiagent.schema.schemas import IntentOutput, EDAOutput, InsightOutput, MLStrategyOutput, SummaryOutput
from eda_multiagent.tools.missing_tool import MissingValueTool
from eda_multiagent.tools.outlier_tool import OutlierTool
from eda_multiagent.tools.correlation_tool import CorrelationTool
from eda_multiagent.tools.multicollinearity_tool import MulticollinearityTool
from eda_multiagent.tools.duplicate_tool import DuplicateTool
from eda_multiagent.tools.class_imbalance_tool import ClassImbalanceTool
from eda_multiagent.core.memory import Memory
import time

_ = load_dotenv()
MODEL_NAME = os.getenv("MODEL")

llm = LLM(
    model=MODEL_NAME,
    temperature=0.2,
    max_tokens=600
)

THROTTLE_SECONDS = 120

@CrewBase
class MultiAgentEDACrew:
    """Multi Agent EDA Crew"""

    agents: List[Agent]
    tasks: List[Task]

    # ========== AGENTS ==========
    @agent
    def intent_agent(self) -> Agent:
        return Agent(config=self.agents_config["intent_agent"], llm=llm)

    @agent
    def eda_agent(self) -> Agent:
        return Agent(config=self.agents_config["eda_agent"], llm=llm, max_iter=3, tools = [
                                                                                    # MasterProfileTool(),
                                                                                    MissingValueTool(),
                                                                                    OutlierTool(),
                                                                                    CorrelationTool(),
                                                                                    MulticollinearityTool(),
                                                                                    DuplicateTool(),
                                                                                    ClassImbalanceTool()
                                                                                ]
                    )

    @agent
    def insight_agent(self) -> Agent:
        return Agent(config=self.agents_config["insight_agent"], llm=llm)

    @agent
    def ml_strategy_agent(self) -> Agent:
        return Agent(config=self.agents_config["ml_strategy_agent"], llm=llm)
    
    @agent
    def summary_agent(self) -> Agent:
        return Agent(
        config=self.agents_config["summary_agent"],
        llm=llm
    )

    # ========== TASKS ==========
    @task
    def intent_task(self) -> Task:
        return Task(
            config=self.tasks_config["intent_task"],
            output_pydantic=IntentOutput,
            callback=lambda output: Memory.set("intent", output.dict())
        )

    @task
    def eda_task(self) -> Task:
        return Task(
            config=self.tasks_config["eda_task"],
            context=[self.intent_task()],
            output_pydantic=EDAOutput,
            callback=lambda output: Memory.set("eda", output.dict())
        )

    @task
    def insight_task(self) -> Task:
        return Task(
            config=self.tasks_config["insight_task"],
            context=[self.intent_task(), self.eda_task()],  
            output_pydantic=InsightOutput,
            callback=lambda output: Memory.set("insight", output.dict())
        )

    @task
    def ml_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config["ml_strategy_task"],
            context=[
                self.intent_task(),
                self.eda_task(),
                self.insight_task(),
            ],  
            output_pydantic=MLStrategyOutput,
            callback=lambda output: Memory.set("ml_strategy", output.dict())
        )

    @task
    def summary_task(self) -> Task:
        return Task(
            config=self.tasks_config["summary_task"],
            context=[
                self.insight_task(),
                self.ml_strategy_task()
            ],
            output_pydantic=SummaryOutput,  
            callback=lambda output: Memory.set("summary", output.dict())
        )

    # ========== CREW ==========
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            after_task=lambda _: time.sleep(THROTTLE_SECONDS)
        )
