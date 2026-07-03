from app.services.semantic_search import semantic_search
from app.services.llm_service import llm


class JobAgent:

    def search_jobs(self, request: str):

        jobs = semantic_search.search(request, k=5)

        recommendations = []

        for rank, job in enumerate(jobs, start=1):

            recommendations.append({
                "rank": rank,
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "score": round(job["score"], 3),
                "reason": self.generate_reason(job, request),
                "link": job["link"]
            })

        return recommendations

    def generate_reason(self, job, request):

        prompt = f"""
    You are an AI career assistant.

    User request:
    {request}

    Job title:
    {job['title']}

    Company:
    {job['company']}

    Location:
    {job['location']}

    Explain in 2-3 sentences why this job could match the user's request.
    """

        response = llm.generate(prompt)

        if response:
            return response

        return (
            f"This job matches your request "
            f"'{request}' with similarity score "
            f"{job['score']:.3f}."
    )

job_agent = JobAgent()