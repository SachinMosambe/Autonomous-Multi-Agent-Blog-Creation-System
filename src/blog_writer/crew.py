from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import yaml
import os

@CrewBase
class BlogWriter():
    """BlogWriter crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

@CrewBase
class BlogWriter():
    """BlogWriter crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        # Base path
        base_dir = os.path.dirname(__file__)
        agents_path = os.path.join(base_dir, 'config', 'agents.yaml')
        tasks_path = os.path.join(base_dir, 'config', 'tasks.yaml')

        # Load YAML files
        with open(agents_path, 'r') as f:
            self.agents = {k.lower(): v for k, v in yaml.safe_load(f).items()}

        with open(tasks_path, 'r') as f:
            self.tasks = {k.lower(): v for k, v in yaml.safe_load(f).items()}

    @agent
    def planner(self) -> Agent:
        return Agent(
            config=self.agents_config['Planner'],
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['Writer'],
            verbose=True
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['Editor'],
            verbose=True
        )

    @agent
    def reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['Reviewer'],
            verbose=True
        )

    @task
    def plan_task(self) -> Task:
        return Task(
            config=self.tasks_config['plan_task']
        )

    @task
    def write_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_task']
        )

    @task
    def edit_task(self) -> Task:
        return Task(
            config=self.tasks_config['edit_task'],
            output_file='report.md'
        )

    @task
    def review_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
