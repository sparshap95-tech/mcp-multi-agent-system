import streamlit as st
import asyncio
from fastmcp import Client

st.title("🔍 Wikipedia MCP Agent")

query = st.text_input("Enter topic:")

# ✅ Async function
async def call_mcp_async(query):
    client = Client("http://localhost:8000/mcp")

    async with client:
        result = await client.call_tool(
            "search_wikipedia",
            {"query": query}
        )
        return result

# ✅ Sync wrapper (better for Streamlit)
def call_mcp(query):
    return asyncio.run(call_mcp_async(query))


# UI
if st.button("Search"):
    if query:
        with st.spinner("Fetching..."):
            result = call_mcp(query)

            # ✅ Clean output extraction
            if not result.is_error:
                try:
                    clean_output = result.structured_content["result"]
                except:
                    clean_output = result.data  # fallback

                st.markdown("### ✅ Result")
                st.write(clean_output)
            else:
                st.error("Error occurred")
    else:
        st.warning("Please enter a topic")