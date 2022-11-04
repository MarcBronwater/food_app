import streamlit as st
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD, Adam, Adagrad, RMSprop
import numpy as np
from streamlit.components.v1 import html
import pickle
from ast import literal_eval
import base64

df_recipes = pd.read_csv("updated_recipes.csv", converters={"steps": literal_eval, "ingredients": literal_eval})

with open("test", "rb") as fp:  # Unpickling
    variables_list = pickle.load(fp)

Cuisine = variables_list[0]
Duration = variables_list[1]
Health_goal = variables_list[2]
Diet = variables_list[3]


# create navigation
def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)


if st.button('Go to main'):
    nav_page("Main_page")

if st.button('Change preferences'):
    nav_page("questionnaire")

Model = tf.keras.models.load_model("model.h5")


def predict(duration, cuisine, health_goal, diet, model):
    if duration == "30 minutes":
        duration = 0  # "30 minutes"
    elif duration == "30 to 60 minutes":
        duration = 0.25  # "30 to 60 minutes"
    elif duration == "60 to 120 minutes":
        duration = 0.5  # "60 to 120 minutes"
    elif duration == "120 to 180 minutes":
        duration = 0.75  # "120 to 180 minutes"
    elif duration == "over 180 minutes":
        duration = 1.0  # "over 180 minutes"

    if cuisine == "Undefined":
        cuisine = 0  # "undefined"
    elif cuisine == "American":
        cuisine = 0.25  # "american"
    elif cuisine == "European":
        cuisine = 0.5  # "european"
    elif cuisine == "Asian":
        cuisine = 0.75  # "asian"
    elif cuisine == "African":
        cuisine = 1.0  # "african"

    if health_goal == "Balanced":
        health_goal = 0  # "Balanced"
    elif health_goal == "Muscle Gain":
        health_goal = 0.5  # "Muscle Gain"
    elif health_goal == "Losing Fat":
        health_goal = 1.0  # "Losing Fat"

    if diet == "Normal":
        diet = 0  # "Normal"
    elif diet == "Keto":
        diet = 0.5  # "Keto"
    elif diet == "Vegetarian":
        diet = 1.0  # "Vegetarian"

    model_array = model.predict(pd.DataFrame([[duration, cuisine, health_goal, diet]], columns=['Duration', 'Cuisine',
                                                                                                'Health Goal', 'Diet']))
    prediction = np.where(model_array == np.amax(model_array))
    return prediction


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """, unsafe_allow_html=True
    )


if Cuisine == "Undefined":
    add_bg_from_local('pictures/undefined_recipe_background.jpg')

if Cuisine == "American":
    add_bg_from_local('pictures/american_recipe_background.jpg')

if Cuisine == "European":
    add_bg_from_local('pictures/european_recipe_background.jpg')

if Cuisine == "Asian":
    add_bg_from_local('pictures/asian_recipe_background.jpg')

if Cuisine == "African":
    add_bg_from_local('pictures/african_recipe_background.jpg')

Recipe = predict(Duration, Cuisine, Health_goal, Diet, Model)
st.success('The predicted recipes are: ')
# st.success(range(224))

for i in range(len(df_recipes)):
    if Recipe[1] == i:
        # st.success(len(df_recipes[df_recipes["Category"] == 0]))
        indices = np.where(df_recipes["Category"] == i)
        for j in indices:
            for k in j:
                with st.expander(df_recipes.loc[k, 'name']):
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric(label="Calories (#)", value=df_recipes.loc[k, 'Calories (#)'])
                    col2.metric(label="Total Fat (PDV)", value=df_recipes.loc[k, 'Total Fat (PDV)'])
                    col3.metric(label="Carbohydrates (PDV)", value=df_recipes.loc[k, 'Carbohydrates (PDV)'])
                    col4.metric(label="Protein (PDV)", value=df_recipes.loc[k, 'Protein (PDV)'])

                    df_ingredients = pd.DataFrame(df_recipes.loc[k, 'ingredients'])
                    df_ingredients.columns = ["Ingredients"]
                    df_steps = pd.DataFrame(df_recipes.loc[k, 'steps'])
                    df_steps.columns = ["Steps"]
                    st.write("Ingredients: ", df_ingredients)
                    st.write('Steps: ', df_steps)



