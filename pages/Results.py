import streamlit as st
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD, Adam, Adagrad, RMSprop
import tensorflow as tf
from tensorflow import keras
import numpy as np
from streamlit.components.v1 import html
import pickle
import joblib

df_recipes = pd.read_csv("updated_recipes.csv")

with open("test", "rb") as fp:   # Unpickling
    variables_list = pickle.load(fp)


Cuisine = variables_list[0]
Duration = variables_list[1]
Health_goal = variables_list[2]
Diet = variables_list[3]

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


Recipe = predict(Duration, Cuisine, Health_goal, Diet, Model)
st.success('The predicted recipe is ' + str(Recipe[1]))
# st.success(range(224))

for i in range(len(df_recipes)):
    if Recipe[1] == i:
        # st.success(len(df_recipes[df_recipes["Category"] == 0]))
        indices = np.where(df_recipes["Category"] == i)
        for j in indices:
            for k in j:
                st.success(df_recipes.loc[k, 'name'])


