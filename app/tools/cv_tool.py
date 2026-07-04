from app.services.cv_matcher import cv_matcher


class CVTool:

    name = "cv_match"

    description = "Match a CV against available jobs."

    def execute(self, cv_text):
        return cv_matcher.match(cv_text)


cv_tool = CVTool()