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


Cuisine = st.selectbox('Cuisine:', ['Undefined', 'American', 'European', 'Asian', 'African'])

Duration = st.selectbox('Duration:', ['30 minutes', '30 to 60 minutes', '60 to 120 minutes', '120 to 180 minutes',
                                      'over 180 minutes'])

Health_goal = st.selectbox('Health Goal:', ['Balanced', 'Muscle Gain', 'Losing Fat'])

Diet = st.selectbox('Diet:', ['Normal', 'Keto', 'Vegetarian'])

if st.button('Predict Recipe'):
    input_variables_list = [Cuisine, Duration, Health_goal, Diet]
    with open("test", "wb") as fp:  # Pickling
        pickle.dump(input_variables_list, fp)
    nav_page("Results")

if st.button('Go to main'):
    nav_page("Main_page")
