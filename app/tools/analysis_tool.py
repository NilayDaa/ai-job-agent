from app.services.career_analyzer import career_analyzer


class AnalysisTool:

    name = "career_analysis"

    description = "Analyze a CV and matched jobs."

    def execute(self, cv_text, skills, jobs):
        return career_analyzer.analyze(
            cv_text,
            skills,
            jobs
        )


analysis_tool = AnalysisTool()