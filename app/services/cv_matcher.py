from app.services.semantic_search import semantic_search


class CVMatcher:

    def match(self, cv_text: str):

        jobs = semantic_search.search(
            query=cv_text,
            k=5
        )

        recommendations = []

        for rank, job in enumerate(jobs, start=1):

            score = round(job["score"], 3)

            if score >= 0.70:
                match = "Excellent Match"

            elif score >= 0.55:
                match = "Good Match"

            elif score >= 0.40:
                match = "Possible Match"

            else:
                match = "Low Match"

            recommendations.append({
                "rank": rank,
                "match": match,
                "score": score,
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "link": job["link"]
            })

        return recommendations


cv_matcher = CVMatcher()