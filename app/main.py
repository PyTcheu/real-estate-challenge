import streamlit as st

st.set_page_config(
    page_title="Sound Realty AI",
    page_icon="🏠",
    layout="centered"
)

# --- Header ---
st.title("🏠 Sound Realty: Smarter Home Pricing with AI")
st.markdown("---")

# --- Non-technical Overview ---
st.header("🏠 The Challenge")
st.markdown("""
Selling a home in Seattle can be tricky. Real estate agents at **Sound Realty** spend a lot of time estimating how much a property is worth.  
It’s a process that involves comparing hundreds of homes, prices, and neighborhood details — and it can easily take hours for every new listing.
""")

st.header("💡 The Idea")
st.markdown("""
One of Sound Realty’s team members experimented with **machine learning**, a type of artificial intelligence that learns patterns from data.  
They built a **simple model** that can automatically predict home prices using information such as the number of bedrooms, square footage, and location.

Even though the model is basic, it proved that **AI can help make property valuation faster and more consistent**.  
Now, Sound Realty wants to make this tool accessible to their whole team — without requiring anyone to understand the technical side.
""")

st.header("🚀 Our Mission")
st.markdown("""
We’re helping Sound Realty turn this idea into a **working online service**.

We’ll deploy the model as an **API (Application Programming Interface)** — a digital bridge that lets other applications send home details and receive instant price predictions.

In plain terms, this means:
- Agents can upload or send home data and get immediate price estimates.
- The service handles background tasks automatically — merging demographic data and running the model.
- As Sound Realty improves the model, it can be updated **without interrupting the service**.
""")

st.header("🔍 What’s Next")
st.markdown("""
Once live, this system will:
- Save agents valuable time
- Reduce guesswork in pricing
- Provide a foundation for more advanced AI models in the future

Ultimately, our goal is to help Sound Realty **use data and AI to make home selling smarter, faster, and easier**.
""")

st.markdown("---")

# --- Technical Section ---
st.header("🧠 Technical Architecture (For Developers)")
st.markdown("""
The deployed solution uses a **FastAPI backend** running under **Guvicorn**, containerized with **Docker** for portability and scalability.
Below is an outline of the main system design and features:
""")

st.subheader("🧩 API Endpoints")
st.markdown("""
- `POST /predictions/{model_id}` → Make predictions with the latest version of a given model using the **simple numeric features**.  
- `POST /predictions/all_features/{model_id}` → Make predictions using the **ALL_FEATURES model**, which includes extended attributes.  
- `POST /models/` → Create a new model or update an existing one; the system automatically increments the version and updates the model registry.  
- `GET /models/latest/{model_id}` → Retrieve the latest version and metadata for a specific model.

**Key points about the implementation:** 
- The service always uses the **latest version** of the model for inference.
- Different endpoints are available for the **simple** and **complex (all features)** models, each with its own validation schema.  
- A **CSV-based model registry** tracks versions, features, authors, and artifact paths for all models.  
- Models are loaded from local paths or could be retrieved from **S3** for horizontal scaling, ensuring consistency across multiple instances.  
- This setup allows new models to be deployed **without downtime**, supports **containerized deployment**, and can scale efficiently with Uvicorn workers.
""")

st.subheader("✅ Input Validation with Pydantic")
st.markdown("""
- Rejects malformed or incomplete inputs  
- Prevents unnecessary computation and system load  
- Ensures requests match the model’s expected features
""")

st.subheader("🗂️ Model Registry & Version Control")
st.markdown("""
- Model versions, features, and artifact paths are stored in a **CSV registry**  
- Predictions always use the **latest model version**  
- Allows publishing new models **without downtime**
""")

st.subheader("🔄 Continuous Deployment & Scalability")
st.markdown("""
- Containerized architecture with Docker  
- Uvicorn workers configured for concurrency and efficiency  
- Model artifacts stored in **S3**, ensuring consistency across multiple instances  
- Supports **horizontal scaling** without replication issues  

**AWS Deployment Considerations:**
- Deploy the service on **Amazon EKS (Elastic Kubernetes Service)** for managed Kubernetes.  
- Use a **Load Balancer** (ALB/NLB) to distribute incoming API requests across multiple pods.  
- Optionally, place an **API Gateway** in front to manage authentication, rate limiting, and monitoring.  
- Kubernetes can automatically **scale pods horizontally** based on CPU, memory, or request load (HPA).  

**Horizontal vs Vertical Scaling:**
- **Horizontal scaling (adding more pods/instances)** is preferable for this API because:
  - Each prediction request is stateless and independent.  
  - Avoids overloading a single instance.  
  - Works seamlessly with S3-stored model artifacts, preventing replication issues.  
- **Vertical scaling (adding more CPU/memory to a single instance)** is less flexible and limited by machine capacity.
""")

st.subheader("🧪 Testing the API")
st.markdown("""
The `app/test_app.py` script is a **simple test client** that demonstrates the behavior of our deployed prediction service.  

##### Requirements:
   - Requires that both the model pickle files and feature JSON files are already in place.
   - You can generate them just by running the conda environment and executing `create_new_model.py` and `create_model.py`.

What it does:

1. **Creates new model entries via the API**:  
   - Sends POST requests to `/models/` to register models with their feature sets and artifacts.

2. **Loads unseen example data** from `data/future_unseen_examples.csv`.

3. **Submits prediction requests**:  
   - For both the **simple numeric features model** and the **all-features model**.  
   - Prints the predicted home prices along with API status codes.

In short, this script validates that:
- The API endpoints are functional.
- Models can be registered and updated.
- Predictions can be made for new, unseen data.
""")