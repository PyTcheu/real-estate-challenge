import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Model metrics", page_icon="🔧", layout="wide")
st.title("🔧 Model Training Results")

BASE_DIR = Path(__file__).parent.parent  # go up one level to `app/`
metrics_path = BASE_DIR / "new_model" / "training_metrics.csv"

if not metrics_path.exists():
    st.warning("⚠️ No training results found. Run `create_new_model.py` first to generate metrics.")
else:
    metrics_df = pd.read_csv(metrics_path)


    st.subheader("📊 Model Comparison")
    st.write("Below you can see how each model performed when trained with different types of information:")

    st.markdown("""
    - **Sales_Subset:** Uses only property details (bedrooms, bathrooms, area, etc.)  
    - **All_Features:** Includes both property and neighborhood details (income, population, location, etc.)
    """)

    # Pivot the table
    pivot = metrics_df.pivot(index="Model", columns="Feature_Set", values=["MAE", "MSE", "R2"])
    st.dataframe(pivot.style.format("{:,.2f}"), use_container_width=True)

    st.markdown("""
    ---
    ### 💡 Understanding the Results

    Each model tries to predict **house prices** based on the available data.  
    We tested four different approaches:
    **Gradient Boosting**, **K-Nearest Neighbors (KNR)**, **Random Forest**, and **XGBoost**.

    #### 🏠 What We Found
    - The **Random Forest (All_Features)** model gave the **most accurate predictions**, explaining about **88% of price variations (R² = 0.8797)**.  
    - **XGBoost** followed closely behind, showing similar consistency.  
    - When using only the **Sales_Subset**, performance dropped across all models — showing that **location and demographic data play an important role** in explaining price variation.  
    - Simpler methods like **KNN** struggled to adapt to the complexity of the dataset.

    #### 📌 Quick Comparison with Baseline Model")

    - **Previous Baseline (KNR with Sales_Subset only)**  
    - MAE ≈ 102k
    - R² ≈ 0.728  

    - **New Best Model (RandomForest with All_Features)**  
    - MAE ≈ 70k
    - R² ≈ 0.88  

    ✅ This shows that including **location, demographic, and neighborhood features** improves accuracy significantly:  
    - **MAE** dropped by ~32%  
    - **R²** increased from 0.73 to 0.88  

    This means the new model is not only more precise but also better at generalizing to unseen data.
    In other words, the new model can provide **more reliable price estimates** for a wider range of properties.

    #### 🏆 Best Model
    The **Random Forest using All_Features** is the **best fit overall** —  
    it balances accuracy and robustness, achieving **R² ≈ 0.88** with low error rates.  
    This indicates a good generalization to new data without overfitting.

    #### ⚙️ About This Test
    These models were trained with:
    - **Default settings** (no hyperparameter tuning)  
    - **No advanced feature engineering or EDA**

    This setup serves as a **baseline**, already achieving strong accuracy with minimal tuning —  
    proving that including demographic and location features greatly enhances performance.

    🚀 **Next Steps**
    Future improvements could include:
    - Hyperparameter tuning (e.g., GridSearchCV or Optuna)  
    - Adding engineered features (like price per sqft, age of property, etc.)  
    - Testing ensemble methods or stacked models to push R² even higher.
    """)
