from app.tools.search_tool import search_tool
from app.tools.cv_tool import cv_tool
from app.tools.analysis_tool import analysis_tool


class JobAgent:

    def __init__(self):

        self.tools = {
            search_tool.name: search_tool,
            cv_tool.name: cv_tool,
            analysis_tool.name: analysis_tool,
        }

    def search_jobs(self, query, k=10):
        return self.tools["job_search"].execute(query, k)

    def match_cv(self, cv_text):
        return self.tools["cv_match"].execute(cv_text)

    def analyze(self, cv_text, skills, jobs):
        return self.tools["career_analysis"].execute(
            cv_text,
            skills,
            jobs
        )


job_agent = JobAgent()