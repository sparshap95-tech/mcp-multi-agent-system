import streamlit as st
import asyncio
from fastmcp import Client

st.title(" Wikipedia MCP Agent")

query = st.text_input("Enter topic:")

async def call_mcp(query):
    client = Client("http://localhost:8000/mcp")

    async with client:
        result = await client.call_tool(
            "search_wikipedia",
            {"query": query}
        )
        return result

if st.button("Search"):
    if query:
        try:
            result = asyncio.run(call_mcp(query))

            st.write("### 📄 Result:")

            # ✅ Extract clean output
            if result.content and len(result.content) > 0:
                output = result.content[0].text
            elif result.structured_content and "result" in result.structured_content:
                output = result.structured_content["result"]
            else:
                output = "No result found."

            # ✅ Display nicely
            st.success(output)

        except Exception as e:
            st.error(f"Error: {str(e)}")

    else:
        st.warning("Please enter a topic")