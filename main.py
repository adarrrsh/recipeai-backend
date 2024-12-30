
import pandas as pd 

from flask import Flask,request,jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pd.read_csv("data.csv")
data["Cleaned-Ingredients"] = data["Cleaned-Ingredients"].str.split()

def calculate_score(user_ingredients, data_my):
    user_set = set(user_ingredients)  
    data_set = set(data_my)          
    return len(user_set.intersection(data_set))


@app.route("/predict",methods=["POST"])
def predict():
    user = request.get_json()
    user_ingridients = user.get("Ingridients")
    user_ingridients = user_ingridients.split(",")
    Foodtype = user.get("type")
    print(user_ingridients)
    data["Score"] = data["Cleaned-Ingredients"].apply(
        lambda x: calculate_score(user_ingridients, x)
    )
    top_recipes = data.sort_values(by="Score",ascending=False).head(5)
    # top_recipes = top_recipes.sort_values(type,ascending=False)
    return jsonify({"recipes":top_recipes["TranslatedRecipeName"].to_list()})



if __name__ == "__main__":
    app.run()