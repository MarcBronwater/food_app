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

st.title('Wat wordt de maaltijd voor vanavond?')

st.markdown(
    """
    Benieuwd naar een nieuw recept op basis van jou diëet en gezondheidsdoel?
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


if st.button('Voorspel recept'):
    nav_page("questionnaire")

st.header("Info")
st.markdown(
    """
    Info
    blablablabbla
    """
)

st.header("Disclaimer")
st.markdown(
    """
    Disclaimer
    blala
    """
)