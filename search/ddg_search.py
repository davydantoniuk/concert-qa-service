from duckduckgo_search import DDGS

def perform_search(query: str, max_results: int = 3) -> str:
    """
    Uses DuckDuckGo Search to find relevant web information when RAG system fails.
    """
    snippets = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            snippets.append(f"- {r['title']}: {r['body']}")

    return "\n".join(snippets) if snippets else None