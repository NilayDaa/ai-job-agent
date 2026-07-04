import json
import re

from app.services.llm_service import llm


class CareerAnalyzer:

    def analyze(self, cv_text, skills, jobs):

        prompt = f"""
You are an expert AI career coach.

Candidate Skills:
{skills}

CV:
{cv_text[:3000]}

Top Matching Jobs:
{json.dumps(jobs, indent=2)}

Return ONLY valid JSON in this format:

{{
  "overall_match": 0-100,
  "strengths": [],
  "missing_skills": [],
  "recommendation": "",
  "learning_path": []
}}
"""

        response = llm.generate(prompt)

        if response:
            try:
                cleaned = response.strip()

                # Remove Markdown code fences
                cleaned = re.sub(r"^```json\s*", "", cleaned)
                cleaned = re.sub(r"^```\s*", "", cleaned)
                cleaned = re.sub(r"\s*```$", "", cleaned)

                return json.loads(cleaned)
            except:
                return {
                    "error": "Could not parse AI response.",
                    "raw_response": response
                }

        return {
            "error": "Gemini unavailable."
        }


career_analyzer = CareerAnalyzer()