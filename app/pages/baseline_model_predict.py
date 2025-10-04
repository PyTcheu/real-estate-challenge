import streamlit as st
import requests

st.set_page_config(page_title="🏠 Baseline Model Predict", page_icon="🏠")

st.title("🏠 Baseline Model — Price Prediction")
st.write("""
This page uses the **baseline model** trained only with **property features**  
(e.g., bedrooms, bathrooms, area, and condition) to estimate real estate prices.

This simpler model — **K-Nearest Neighbors (KNR)** using only Sales features —  
was our **starting point** before introducing demographic and location data in later models.
""")

col1, col2 = st.columns(2)

with col1:
    bedrooms = st.number_input("Bedrooms", min_value=0, step=1, value=3)
    bathrooms = st.number_input("Bathrooms", min_value=0.0, step=0.5, value=2.0)
    sqft_living = st.number_input("Living Area (sqft)", min_value=0, step=1, value=1800)
    sqft_lot = st.number_input("Lot Area (sqft)", min_value=0, step=1, value=5000)
    floors = st.number_input("Floors", min_value=0.0, step=0.5, value=2.0)
    waterfront = st.selectbox("Waterfront", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", index=0)

with col2:
    view = st.number_input("View (0-4)", min_value=0, max_value=4, step=1, value=0)
    condition = st.number_input("Condition (1-5)", min_value=1, max_value=5, step=1, value=3)
    grade = st.number_input("Grade (1-13)", min_value=1, max_value=13, step=1, value=7)
    sqft_above = st.number_input("Above Ground Area (sqft)", min_value=0, step=1, value=1500)
    sqft_basement = st.number_input("Basement Area (sqft)", min_value=0, step=1, value=300)
    yr_built = st.number_input("Year Built", min_value=1800, max_value=2025, step=1, value=1990)
    yr_renovated = st.number_input("Year Renovated", min_value=0, max_value=2025, step=1, value=0)

zipcode = st.text_input("Zipcode", value="98052")

if st.button("🚀 Predict"):
    input_data = {
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "sqft_living": sqft_living,
        "sqft_lot": sqft_lot,
        "floors": floors,
        "waterfront": waterfront,
        "view": view,
        "condition": condition,
        "grade": grade,
        "sqft_above": sqft_above,
        "sqft_basement": sqft_basement,
        "yr_built": yr_built,
        "yr_renovated": yr_renovated,
        "zipcode": zipcode
    }

    try:
        base_url = "http://127.0.0.1:8000/"
        url = f"{base_url}predictions/real_estate_model"

        response = requests.post(url, json=input_data)

        if response.status_code == 200:
            prediction = response.json().get("prediction", ["No prediction available"])[0]
            st.success(f"💰 **Predicted Price:** ${prediction:,.2f}")
        else:
            error_message = response.json().get("detail", "Unknown error occurred.")
            st.error(f"❌ API Error: {error_message}")

    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Could not connect to the prediction service:\n\n{e}")

st.markdown("""
---
### 🧠 Model Notes
This baseline predictor:
- Uses **only property-related features** (no demographic or location data).  
- Is powered by a **K-Nearest Neighbors** model trained as part of the initial benchmark.  
- Demonstrates how predictions behave **before** introducing richer features in later models.

👉 In the next pages, you’ll compare how performance improves  
as we include **demographic, location, and engineered variables**.
""")
