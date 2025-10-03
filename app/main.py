import streamlit as st
import requests

st.title("🏠 Real Estate Price Prediction")
st.write("Fill in the property details below and click **Predict** to estimate the price.")

# TO-DO: Use streamlit interface as a case presentation before diving into the application
# Page 1: Intro and context, problem statement, and business understanding
# Page 2: Application for prediction only
# Page 3: Deploying new model version without downtime
# Page 4: Bonus: Test function to model evaluations

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

# Zipcode input spans the full width
zipcode = st.text_input("Zipcode", value="98052")

# Predict button
if st.button("Predict"):

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

    # Send POST request to Flask API
    try:
        base_url = f"http://127.0.0.1:5000/"
        url = f"{base_url}predictions/real_estate_model"

        response = requests.post(url, json=input_data)
        if response.status_code == 200:
            prediction = response.json().get("prediction", ["No prediction available"])[0]
            st.success(f"💰 Predicted Price: ${prediction:,.2f}")
        else:
            error_message = response.json().get("detail", "Unknown error occurred")
            st.error(f"❌ Error: {error_message}")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Failed to connect to the prediction service: {e}")