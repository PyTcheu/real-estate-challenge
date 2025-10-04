import streamlit as st
import requests

st.set_page_config(page_title="🏠 Advanced Model Predict", page_icon="🏠")

st.title("🏠 Advanced Model — Price Prediction")
st.write("""
This page uses the **enhanced model** trained with **all available features**  
(e.g., property details, location coordinates, and surrounding home information) to estimate real estate prices.

This model improves upon the baseline by including **richer data** such as neighborhood features,  
allowing more accurate and reliable predictions.
""")

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    bedrooms = st.number_input("Bedrooms", min_value=0, step=1, value=3)
    bathrooms = st.number_input("Bathrooms", min_value=0.0, step=0.5, value=2.0)
    sqft_living = st.number_input("Living Area (sqft)", min_value=0, step=1, value=1800)
    sqft_lot = st.number_input("Lot Area (sqft)", min_value=0, step=1, value=5000)
    floors = st.number_input("Floors", min_value=0.0, step=0.5, value=2.0)
    waterfront = st.selectbox("Waterfront", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", index=0)
    lat = st.number_input("Latitude", value=47.5354, format="%.6f")
    long = st.number_input("Longitude", value=-122.273, format="%.6f")

with col2:
    view = st.number_input("View (0-4)", min_value=0, max_value=4, step=1, value=0)
    condition = st.number_input("Condition (1-5)", min_value=1, max_value=5, step=1, value=3)
    grade = st.number_input("Grade (1-13)", min_value=1, max_value=13, step=1, value=7)
    sqft_above = st.number_input("Above Ground Area (sqft)", min_value=0, step=1, value=1500)
    sqft_basement = st.number_input("Basement Area (sqft)", min_value=0, step=1, value=300)
    yr_built = st.number_input("Year Built", min_value=1800, max_value=2025, step=1, value=1990)
    yr_renovated = st.number_input("Year Renovated", min_value=0, max_value=2025, step=1, value=0)
    sqft_living15 = st.number_input("Average Living Area of 15 Neighbors (sqft)", min_value=0, step=1, value=1560)
    sqft_lot15 = st.number_input("Average Lot Area of 15 Neighbors (sqft)", min_value=0, step=1, value=5765)

zipcode = st.text_input("Zipcode", value="98118")

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
        "zipcode": zipcode,
        "lat": lat,
        "long": long,
        "sqft_living15": sqft_living15,
        "sqft_lot15": sqft_lot15
    }

    try:
        base_url = "http://127.0.0.1:8000/"
        url = f"{base_url}predictions/all_features/real_estate_model_all_features"

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
This advanced predictor:
- Uses **all relevant features**, including property details, coordinates, and neighborhood statistics.  
- Merges **demographic and location information** automatically before predicting.  
- Is powered by an **ensemble or complex model** that improves accuracy over the baseline KNN.  

👉 Use this page to compare predictions against the baseline,  
and observe how richer features lead to better estimates.
""")
