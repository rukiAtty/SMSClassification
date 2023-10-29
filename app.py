import numpy as np
import pickle
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.preprocessing.sequence import pad_sequences
import string
import streamlit as st

model=pickle.load(open('./model1.pkl','rb'))
VOCAB_SIZE = 1000
PUNCTUATION = string.punctuation

def remove_punctuation(series):
    no_punctuation = "".join([word for word in series if word not in PUNCTUATION])
    return no_punctuation

def predict_category(text):
    text = remove_punctuation(text)
    text = text.lower()
    
    encoded_text = [one_hot(text, VOCAB_SIZE)]
    padded_text = pad_sequences(encoded_text, maxlen=513, padding='post')
    
    pred = (model.predict(padded_text) > 0.5).astype("int32")
    pred = pred.flatten()[0]
    
    return "SPAM" if pred == 1 else "NOT A SPAM"


def main():
    st.title("Classify your SMS")

    if 'input_sms' not in st.session_state:
        st.session_state.input_sms = ""

    input_sms = st.text_area("Enter the SMS", value=st.session_state.input_sms, key="text")
    result = ''

    if st.button('Predict'):
        result = predict_category(input_sms)
        if result == "SPAM":
            st.write(f"Prediction: {result}", unsafe_allow_html=True, background="red")
        else:
            st.write(f"Prediction: {result}", unsafe_allow_html=True, background="green")

    def clear_text():
        st.session_state["text"] = ""
        st.session_state.input_sms = ""

    st.button("Clear Text Input", on_click=clear_text)
    st.write(input_sms)


if __name__ == "__main__":
    main()