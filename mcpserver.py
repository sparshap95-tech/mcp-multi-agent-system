from fastmcp import FastMCP
import wikipedia

mcp = FastMCP("wikipedia-mcp")

@mcp.tool()
def search_wikipedia(query: str) -> str:
    """
    Search Wikipedia and return a short summary.
    """
    summary = wikipedia.summary(query, sentences=1)
    if not summary:
        return "No summary found."
    return summary
    

# if __name__ == "__main__":
#     mcp.run(transport="http", port=8000)
if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")