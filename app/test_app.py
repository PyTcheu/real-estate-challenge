# Load data from a file
import requests
import pandas as pd

data_unseen = pd.read_csv("app/data/future_unseen_examples.csv")

# Make predictions and print results and API status codes
url = "http://127.0.0.1:5000/predictions/real_estate_model"

sample = data_unseen.head()
for i, row in sample.iterrows():
    input_data = row.to_dict()

    # Ensure zipcode is a string
    input_data["zipcode"] = str(int(input_data["zipcode"]))

    print("Input Data:", input_data)  # Debugging print

    # Send the dictionary directly to the `json` parameter
    response = requests.post(url, json=input_data)
    print("Response:", response)
    print("Response Content:", response.text)  # Print the error message from the server