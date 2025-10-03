import pandas as pd

DEMOGRAPHICS_PATH = "app/data/zipcode_demographics.csv"

def get_demographic_data(zipcode: str):
    """
    Retrieve demographic data for a given zipcode.
    """
    demographics_df = pd.read_csv(DEMOGRAPHICS_PATH, dtype={"zipcode": str})
    data = demographics_df[demographics_df["zipcode"] == zipcode]
    if data.empty:
        return None
    return data.drop(columns=["zipcode"]).iloc[0].to_dict()