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
import base64


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


add_bg_from_local('pictures/main_page_background.jpg')

st.title('What are you going to cook tonight?')

st.markdown(
    """
    Curious what recipe you want to cook tonight?
    Most people get into a cycle where they cook the same dish almost every week because that's what they know and 
    are comfortable with.
    If you want to try something new, this app predicts a selection of recipes you could like based on your choice of
     cuisine, time to cook, health goal and diet.
    It does this via an Artificial Intelligence.
    """
)


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


if st.button('Choose preferences'):
    nav_page("questionnaire")

st.header("Info")
st.markdown(
    """
    This app predicts which recipes you would like based on your choice of cuisine, time to cook, health goal and diet.
    The AI has learned which recipes are best suited based on the available choices. Health goals and the keto diet are 
    determined by macro nutrition values. These nutritional values are chosen based on multiple articles which contain 
    results from scientific studies. 
    """
)
st.markdown(
    """
    The dataset used to train the AI is somewhat limited. So there will not be a specific measurement for the 
    ingredients listed.
    """
)
