import streamlit as st
import asyncio
import json
import pandas as pd
from fastmcp import Client

st.set_page_config(page_title="Brand Comparison", layout="centered")

st.title("🏷️ Nike vs Puma Comparison")

# Button to trigger comparison
if st.button("Compare Brands"):

    async def run_comparison():
        async with Client("compareserver.py") as client:
            nike_raw = await client.call_tool("get_brand_data", {"brand_name": "nike"})
            puma_raw = await client.call_tool("get_brand_data", {"brand_name": "puma"})

            # Extract JSON string safely
            nike_json = nike_raw.content[0].text
            puma_json = puma_raw.content[0].text

            # Convert to Python list
            nike_data = json.loads(nike_json)
            puma_data = json.loads(puma_json)

            return nike_data, puma_data

    # Run async function
    nike_data, puma_data = asyncio.run(run_comparison())

    # Convert to DataFrame
    nike_df = pd.DataFrame(nike_data)
    puma_df = pd.DataFrame(puma_data)

    # Display tables
    st.subheader("📊 Nike Data")
    st.dataframe(nike_df, use_container_width=True)

    st.subheader("📊 Puma Data")
    st.dataframe(puma_df, use_container_width=True)

    # 🔧 Robust analysis function
    def analyze(data):
        prices = []
        ratings = []

        for item in data:
            # Handle price safely
            price = item.get("price")
            if price:
                try:
                    prices.append(float(price.replace("$", "")))
                except:
                    pass

            # Handle rating safely
            rating = item.get("rating")
            if rating is not None:
                try:
                    ratings.append(float(rating))
                except:
                    pass

        avg_price = sum(prices) / len(prices) if prices else 0
        avg_rating = sum(ratings) / len(ratings) if ratings else 0

        return avg_price, avg_rating

    nike_price, nike_rating = analyze(nike_data)
    puma_price, puma_rating = analyze(puma_data)

    # 📈 Comparison Section
    st.subheader("📈 Comparison Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Nike Avg Price", f"${nike_price:.2f}")
        st.metric("Nike Avg Rating", f"{nike_rating:.2f}")

    with col2:
        st.metric("Puma Avg Price", f"${puma_price:.2f}")
        st.metric("Puma Avg Rating", f"{puma_rating:.2f}")

    # 🏆 Final Verdict
    st.subheader("🏆 Final Verdict")

    if nike_rating > puma_rating and nike_price <= puma_price:
        st.success("Nike offers better value for money.")
    elif puma_rating > nike_rating and puma_price <= nike_price:
        st.success("Puma offers better value for money.")
    elif nike_rating > puma_rating:
        st.info("Nike has better ratings but is more expensive.")
    elif puma_rating > nike_rating:
        st.info("Puma has better ratings but is more expensive.")
    else:
        st.info("Both brands offer similar value. Choice depends on preference.")