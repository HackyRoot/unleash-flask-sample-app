from flask import Flask, jsonify, render_template_string, render_template
from flask_unleash import Unleash
# from UnleashClient.api.features import get_feature_toggles

import pandas as pd

app = Flask(__name__)
app.config["UNLEASH_URL"] = "http://localhost:4242/api"  # Unleash server URL
app.config["UNLEASH_APP_NAME"] = "default" # Unleash project name 
app.config["UNLEASH_ENVIRONMENT"] = "development" # Environment of the project
app.config["UNLEASH_CUSTOM_HEADERS"] = {'Authorization': 'default:development.8e190b7b2cdd0d97abd758d92c28045f0200c35f1de6515ee7bf71c3'} # Unleash API Key

unleash = Unleash(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
@app.route('/menu/')
def get_menu():
    # Read data from the bookstore
    menu_content = pd.read_csv('menu.csv').to_dict('records')

    # if isReviewsEnabled toggle is enabled, show all fields, including ratings
    if unleash.client.is_enabled("isReviewsEnabled"):
        return render_template('menu.html', menu_data=menu_content)
        
    else:
        fields_to_include = ["id","dish_name","description","price","type","image"]
        menu_data = [{field: menu_item[field] for field in fields_to_include} for menu_item in menu_content]

        return render_template('menu.html', menu_data=menu_data)

if __name__ == '__main__':
    app.run(debug=True)    


    # {% comment %} <img class="square-image" src="{{ url_for('static', filename='dishes/'+dish.image) }}" alt="{{ dish.dish_name }}"> {% endcomment %}