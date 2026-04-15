import streamlit as st
import asyncio
from fastmcp import Client

st.title("🌦️ Weather MCP App")

city = st.text_input("Enter city name")

async def get_weather(city):
    client = Client("http://localhost:8000/mcp")

    async with client:
        result = await client.call_tool(
            "get_weather",
            {"city": city}
        )
        return result.data   # 👈 important

if st.button("Get Weather"):
    if city:
        data = asyncio.run(get_weather(city))

        # Display nicely
        st.success(f"Weather in {data['city']}")
        st.write(f"🌡 Temperature: {data['temperature_C']} °C")
        st.write(f"💧 Humidity: {data['humidity']} %")
        st.write(f"☁ Condition: {data['weather']}")
    else:
        st.warning("Please enter a city name")