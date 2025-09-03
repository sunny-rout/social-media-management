import os
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperDevTool
)
from social_media_management_automation.tools.social_media_publisher import SocialMediaPublisherTool
from crewai_tools import CrewaiEnterpriseTools


@CrewBase
class SocialMediaManagementAutomationCrew:
    """SocialMediaManagementAutomation crew"""

    
    @agent
    def social_media_content_manager(self) -> Agent:
        enterprise_actions_tool = CrewaiEnterpriseTools(
            actions_list=[
                
                "google_sheets_create_row",
                
                "google_sheets_update_row",
                
            ],
        )
        
        return Agent(
            config=self.agents_config["social_media_content_manager"],
            tools=[
				SocialMediaPublisherTool(),
				*enterprise_actions_tool
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    
    @agent
    def trend_research_analyst(self) -> Agent:
        
        return Agent(
            config=self.agents_config["trend_research_analyst"],
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    
    @agent
    def social_media_analytics_specialist(self) -> Agent:
        enterprise_actions_tool = CrewaiEnterpriseTools(
            actions_list=[
                
                "google_sheets_get_row",
                
            ],
        )
        
        return Agent(
            config=self.agents_config["social_media_analytics_specialist"],
            tools=[
				*enterprise_actions_tool
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    

    
    @task
    def research_industry_trends(self) -> Task:
        return Task(
            config=self.tasks_config["research_industry_trends"],
            markdown=False,
        )
    
    @task
    def analyze_performance_metrics(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_performance_metrics"],
            markdown=False,
        )
    
    @task
    def create_content_calendar(self) -> Task:
        return Task(
            config=self.tasks_config["create_content_calendar"],
            markdown=False,
        )
    
    @task
    def schedule_and_publish_content(self) -> Task:
        return Task(
            config=self.tasks_config["schedule_and_publish_content"],
            markdown=False,
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the SocialMediaManagementAutomation crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
