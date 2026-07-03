from app.services.semantic_search import semantic_search


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

        return (
            f"This job matches your search "
            f"'{request}' with a similarity score "
            f"of {job['score']:.3f}."
        )


job_agent = JobAgent()