from app.services.semantic_search import semantic_search


class JobAgent:
    """
    AI Job Agent (Version 1)

    Responsibilities:
    - Understand user requests
    - Search for jobs
    - Rank recommendations
    """

    def search_jobs(self, user_request: str):
        jobs = semantic_search.search(user_request, k=5)

        recommendations = []

        for i, job in enumerate(jobs, start=1):
            recommendations.append({
                "rank": i,
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "link": job["link"],
                "score": round(job["score"], 3),
                "reason": self.explain(job, user_request)
            })

        return recommendations

    def explain(self, job, request):
        """
        Version 1:
        Rule-based explanation.
        Later this will be replaced with an LLM.
        """

        return (
            f"This job is semantically similar to your request "
            f"'{request}' and received a similarity score of "
            f"{job['score']:.3f}."
        )


job_agent = JobAgent()