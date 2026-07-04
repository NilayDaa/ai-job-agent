from app.services.semantic_search import semantic_search


class SearchTool:

    name = "job_search"

    description = "Search for jobs using semantic search."

    def execute(self, query, k=10):
        return semantic_search.search(query, k)


search_tool = SearchTool()