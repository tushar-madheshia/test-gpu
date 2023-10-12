import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import json

st.set_page_config(page_title="Refract",layout="wide", page_icon="")
st.header("TV Linear Ads")
st.write("To find the optimum cost, event and time slot to maximize reach")
output1 = ""
check_prediction  = 0

with st.sidebar:
    from PIL import Image
    image = Image.open('refract.png')

    st.image(image)
    st.sidebar.header("Adjust your inputs")

    brand_name = st.text_input("Enter Brand Name ","Good night")
    channel_name = st.selectbox("Choose Channel",("Channel 1","Channel 2"))
    day_name = st.selectbox("Select Week",("Week1","Week2","Week3","Week4"))
    spot_time = st.selectbox("Select Spot Time",("2.00 pm","8.30 pm","6.30 pm","10.00 pm"))
    frequency = st.slider('Select Frequency', 1, 3, 2)
    grp = st.slider('Select GRP', 20, 500, 50)
    cost = st.slider("Choose Cost",100,10000,200)
    impression = st.slider("Select Required Impression",100,5000,600)


    if st.button('Predict'):
        check_prediction = 1

        payload = {'Brand': brand_name,
            'Channel': channel_name,
            'Day': day_name,
            'Spot time': spot_time,
            'Frequency': frequency,
            'GRPs': grp,
            'Cost': cost,
            'Impressions': impression
            }
        
    else :
        st.write('Please submit once you are ready!')

tab1, tab2, tab3 = st.tabs(["Prediction","Data Profile", "Insights"])

with tab2:
    HtmlFile = open("data_profile.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 600, scrolling=True)

with tab3:
  
#     image2 = Image.open('confusion_matrix_xgboost.png')
#     image3 = Image.open('xgb_ROC_AUC.png')

    
#     st.image(image2)
#     st.write("#")
#     st.image(image3)
#     st.write("#")
    

with tab1:
    if check_prediction > 0:
        #st.text_input("Raw Input", payload)
        headers={"Content-type":"application/json"}
        url = 'http://svc-fb76d6f3-7b26-44f3-a0c5-174c513cff9f:5001/lineartvadsmodel/1ad98815-f1f2-4105-8411-cbfe84cb8601/score'
        score_input = {"payload" : payload}
        st.text_input("Model Payload", score_input)
        response_json = requests.post(url, json=score_input, headers=headers)
        #st.text_input("API Response: ",response_json.content)
        response = response_json.json()
        try:
           st.text_input ('Prediction Output: ',response['data'])
        except ValueError: 
            st.text_input ('Oops we got an error: ',response_json.status_code)
        st.write("#")
    else:
        st.write("Submit to check the model prediction")
