import streamlit as st
import pandas as pd
import numpy as np
import sklearn
import pickle

# Page  Information
st.set_page_config(page_title="Can Suyolcu", page_icon=":bank:", layout="wide")

st.markdown("<h1 style='text-align: center; font-size: 40px;'>Welcome to Loaner!</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-size: 20px;'>You can assess your Customer's eligibility for a loan by filling out the form below:</h1>", unsafe_allow_html=True)
st.markdown("---")

# Loading the trained model
pickle_in = open('classifier.pkl', 'rb') 
model = pickle.load(pickle_in)

# User Input
Gender_input = st.selectbox(label = 'Gender of the applicant', options = ("Male", "Female"))
Married_input = st.selectbox(label = 'Marital Status', options = ("Married", "Single"))
Dependents_input = st.selectbox(label = 'Number of dependants', options = ("0"," 1", "2", "3+"))
Education_input = st.selectbox(label = 'Education Level', options = ("Graduate", "Not Graduate"))
Self_Employed_input = st.selectbox(label = 'Does the applicant own a business?', options = ("Yes", "No"))
ApplicantIncome_input = st.slider(label = 'Monthly income of the applicant', min_value = 0, max_value = 100000)
CoapplicantIncome_input = st.slider(label = 'Monthly income of the cosigner', min_value = 0, max_value = 100000)
LoanAmount_input = st.slider(label = 'The amount of desired loan (in thousands)', min_value = 0, max_value = 1000)
Loan_Amount_Term_input = st.slider(label = 'Desired maturity (in months)', min_value = 0, max_value = 480, step=1)
Credit_History_input = st.selectbox(label = 'Does the applicant have a loan history?', options = ("Yes", "No"))
Property_Area_input = st.selectbox(label = 'Location of the property for which the loan is requested', options = ("Semiurban", "Urban", "Rural"))

st.markdown("<h1 style='text-align: center; font-size: 40px;'>Summary of the information about the applicant:</h1>", unsafe_allow_html=True)
summary_dictionary = {'Gender': Gender_input,  'Marital Status': Married_input, 'Dependants': Dependents_input, 'Education': Education_input,  'Self Employed': Self_Employed_input,
'Income': ApplicantIncome_input, 'Cosigner Income': CoapplicantIncome_input, 'Credit Amount': LoanAmount_input*1000, 'Credit Maturity': Loan_Amount_Term_input,
'Credit History': Credit_History_input, 'Property Area': Property_Area_input}

summary_df  = pd.DataFrame([summary_dictionary])
st.table(summary_df)

# Defining the prediction model

def predict_(model, Gender_input, Married_input, Dependents_input, Education_input, Self_Employed_input, ApplicantIncome_input, CoapplicantIncome_input, LoanAmount_input,
 Loan_Amount_Term_input, Credit_History_input, Property_Area_input):
    
    # Preprocessing
    
    
    if Married_input == "Married":
        Married_var = "Yes"
    else:
        Married_var = "No"

    if Credit_History_input == "Yes":
        Credit_History_var= 1.0
    else:
        Credit_History_var= 0.0


    features = {'Gender': Gender_input ,  'Married': Married_var, 'Dependents': Dependents_input, 'Education': Education_input,  'Self_Employed': Self_Employed_input, 
    'ApplicantIncome': ApplicantIncome_input, 'CoapplicantIncome': CoapplicantIncome_input, 'LoanAmount': LoanAmount_input, 'Loan_Amount_Term': Loan_Amount_Term_input,
    'Credit_History': Credit_History_var, 'Property_Area':Property_Area_input}

    features_df  = pd.DataFrame([features])
    
    prediction_ = model.predict(features_df)

    if prediction_ == 0:
        pred = 'denied.'
    else:
        pred = 'approved.'
    
    return pred


# When the prediction but is clicked, write model predictions.
st.markdown("---")

st.markdown("<h1 style='text-align: left; font-size: 20px;'>Click the button below to see the results of loan application:</h1>", unsafe_allow_html=True)

if st.button('Should the loan be given?'):
    
    result_ = predict_(model, Gender_input, Married_input, Dependents_input, Education_input, Self_Employed_input, ApplicantIncome_input, CoapplicantIncome_input, LoanAmount_input, Loan_Amount_Term_input, Credit_History_input, Property_Area_input)

    if result_ == 'denied.':
        st.error(f'No, loan application of {LoanAmount_input * 1000} Dollars has been denied.')
    else:
        st.success(f'Yes, loan application of {LoanAmount_input * 1000} Dollars has been accepted.')
       

# ---- KEEP THE STRIMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)