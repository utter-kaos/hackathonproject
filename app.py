from flask import Flask, request, jsonify, send_file
import pandas as pd

app = Flask(__name__)

# Loading CSV's 
df = pd.read_csv("facilities.csv")
df.fillna("Unavailable", inplace=True)
pantry_df = pd.read_csv("cleanedpantrys.csv")
pantry_df.fillna("Unavailable", inplace=True)
# serving html files (flask btw)
@app.route("/")
def index():

    return send_file("index.html")

@app.route("/food")
def food():
    return send_file("food.html")
@app.route("/resume")
def resume():
    return send_file("resume.html")
@app.route("/health")
def health():
    return send_file("health.html")
#this is the data set handling that actually kinda matters 
@app.route("/search", methods=["GET"])
def search_facilities():
    # Get query parameter like CLOTHING=true, FOOD_GROCERIES=true
    filters = request.args.to_dict()
    filtered_df = df.copy()

    # For each category that's marked "true", filter out rows where the value is "Unavailable", I tghi
    for category, value in filters.items():
        if value.lower() == "true":
            filtered_df = filtered_df[filtered_df[category] != "Unavailable"]

    # Return the filtered data as JSON
    return jsonify(filtered_df.to_dict(orient="records"))

@app.route("/food/search", methods=["GET"])
def search_food_pantries():
    # Get query parameters for food pantries
    filters = request.args.to_dict()
    filtered_df = pantry_df.copy()

    # Filter based on the selected categories
    if "SHOPPING" in filters:
        filtered_df = filtered_df[filtered_df["PROGRAM"] == "Shopping"]
    if "DIRECT_DISTRIBUTION" in filters:
        filtered_df = filtered_df[filtered_df["PROGRAM"] == "Direct Distributions"]
    if "BOTH" in filters:
        filtered_df = filtered_df[filtered_df["PROGRAM"] == "Shopping & Direct Distribution"]

    # Return the filtered data as JSON
    return jsonify(filtered_df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)