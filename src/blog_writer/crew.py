from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.tools import SerperDevTool, TavilySearchTool, SearchTool
from typing import List
import yaml
import os

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
            self.agents_config = {k.lower(): v for k, v in yaml.safe_load(f).items()}

        with open(tasks_path, 'r') as f:
            self.tasks_config = {k.lower(): v for k, v in yaml.safe_load(f).items()}

        # Set up search tools
        self.search_tools = self.setup_search_tools()

    def setup_search_tools(self):
        """Set up search tools for the agents."""
        tools = []
        
        # Try to initialize Tavily search if API key is available
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if tavily_api_key:
            tools.append(TavilySearchTool())
        
        # Try to initialize SerperDev search if API key is available
        serper_api_key = os.getenv("SERPER_API_KEY")
        if serper_api_key:
            tools.append(SerperDevTool())
        
        # Add the built-in search tool as a fallback
        tools.append(SearchTool())
        
        return tools

    @agent
    def planner(self) -> Agent:
        return Agent(
            config=self.agents_config['planner'],
            tools=self.search_tools,
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
            verbose=True
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'],
            verbose=True
        )

    @agent
    def reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['reviewer'],
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
            agents=[self.planner(), self.writer(), self.editor(), self.reviewer()],
            tasks=[self.plan_task(), self.write_task(), self.edit_task(), self.review_task()],
            process=Process.sequential,
            verbose=True,
        )
