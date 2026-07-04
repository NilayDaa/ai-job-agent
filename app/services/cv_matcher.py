from app.services.semantic_search import semantic_search


class CVMatcher:

    def match(self, cv_text: str):

        jobs = semantic_search.search(
            query=cv_text,
            k=10
        )

        return jobs


cv_matcher = CVMatcher()