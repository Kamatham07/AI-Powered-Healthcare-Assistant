import streamlit as st
import nltk
from transformers import pipeline
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random
from datetime import datetime

# Download NLTK data (if not already downloaded)
nltk.download('punkt')
nltk.download('stopwords')

# Initialize the tokenizer and model
chatbot = pipeline("question-answering", model="deepset/bert-base-cased-squad2")

# Define a list of random doctors and hospitals
doctors = ["Dr. Aakash Mehta", "Dr. Bhavna Patel", "Dr. Chaitanya Rao", "Dr. Divya Sharma", "Dr. Esha Gupta", "Dr. Farhan Khan", "Dr. Gaurav Singh", "Dr. Harshita Jain", "Dr. Ishaan Verma", "Dr. Jyoti Desai", "Dr. Karan Malhotra", "Dr. Lavanya Reddy", "Dr. Manish Kumar", "Dr. Neha Agarwal", "Dr. Omkar Joshi", "Dr. Priya Nair", "Dr. Qasim Ali", "Dr. Ritu Kapoor", "Dr. Sandeep Roy", "Dr. Tanvi Mehta", "Dr. Uday Kulkarni", "Dr. Varun Sharma", "Dr. Waseem Ahmed", "Dr. Xena Fernandes", "Dr. Yashwant Singh", "Dr. Zoya Khan"]

hospitals = ["Apollo Hospitals", "Asian Institute of Medical Sciences", "Aster DM Healthcare", "Billroth Hospitals", "Care Hospitals", "Command Hospital", "Council of Christian Hospitals", "Devadoss Hospital", "Dr. Agarwal's Eye Hospital", "Dr. Mohan's Diabetes Specialities Centre", "Fortis Healthcare", "Global Hospitals Group", "Hinduja Healthcare Limited", "Kailash Group of Hospitals", "Krishna Institute of Medical Sciences", "L. V. Prasad Eye Institutes", "LifeSpring Hospitals", "Manipal Hospitals", "Max Healthcare", "Medica Hospitals", "Metro Group of Hospitals", "Narayana Health", "Paras Healthcare", "Regional Cancer Centre", "Sahyadri Hospital", "Shalby Hospital", "Sir Jamshetjee Jeejebhoy Group of Hospitals", "Sterling Hospitals", "Vasan Healthcare", "Wockhardt Hospitals", "Yatharth Hospitals"]


def healthcare_chatbot(context, user_input):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(user_input)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

    if "symptoms" in filtered_sentence:
        return "Please consult a doctor for accurate advice."
    elif "appointment" in filtered_sentence:
        st.session_state.state = "appointment"
        return "Would you like to schedule an appointment with the doctor?"
    elif "medication" in filtered_sentence:
        return "It's important to take prescribed medicines regularly. If you have any concerns, consult the doctor."
    else:
        response = chatbot(question=user_input, context=context)
        return response['answer']

def handle_follow_up(context, user_input):
    if st.session_state.state == "appointment":
        if user_input.lower() == "yes":
            st.session_state.state = "appointment_date"
            return "Please select a date and time for the appointment."
        else:
            st.session_state.state = "initial"
            return "Okay, let me know if you need any other assistance."
    elif st.session_state.state == "appointment_date":
        st.session_state.appointment_details["date"] = user_input
        st.session_state.state = "appointment_time"
        return "Please select a time for the appointment."
    elif st.session_state.state == "appointment_time":
        st.session_state.appointment_details["time"] = user_input
        st.session_state.state = "initial"
        # Generate random appointment details
        ref_number = f"REF-{random.randint(1000, 9999)}"
        doctor = random.choice(doctors)
        hospital = random.choice(hospitals)
        return (f"Appointment scheduled for {st.session_state.appointment_details['date']} at {st.session_state.appointment_details['time']}.\n"
                f"Reference Number: {ref_number}\n"
                f"Doctor: {doctor}\n"
                f"Hospital: {hospital}")
    else:
        return healthcare_chatbot(context, user_input)

def main():
    st.title("Healthcare Assistant Chatbot")
    context = st.text_area("Provide the context (e.g., medical article, patient history):")
    user_input = st.text_input("How can I assist you today?")
    if st.button("Submit"):
        if context and user_input:
            st.write("User: ", user_input)
            with st.spinner("Processing your query, please wait..."):
                response = handle_follow_up(context, user_input)
            st.write("Healthcare Assistant: ", response)
        else:
            st.write("Please enter a message to get a response.")

    # Calendar and time picker for scheduling appointments
    if st.session_state.state == "appointment_date":
        date = st.date_input("Select an appointment date")
        st.session_state.appointment_details["date"] = date.strftime('%Y-%m-%d')
        if st.button("Confirm Date"):
            st.session_state.state = "appointment_time"

    if st.session_state.state == "appointment_time":
        time = st.time_input("Select an appointment time")
        st.session_state.appointment_details["time"] = time.strftime('%H:%M')
        if st.button("Confirm Time"):
            st.session_state.state = "initial"
            # Generate random appointment details
            ref_number = f"REF-{random.randint(1000, 9999)}"
            doctor = random.choice(doctors)
            hospital = random.choice(hospitals)
            st.write(f"Appointment scheduled for {st.session_state.appointment_details['date']} at {st.session_state.appointment_details['time']}.\n"
                     f"Reference Number: {ref_number}\n"
                     f"Doctor: {doctor}\n"
                     f"Hospital: {hospital}")

# Initialize session state variables
if 'state' not in st.session_state:
    st.session_state.state = 'initial'
if 'appointment_details' not in st.session_state:
    st.session_state.appointment_details = {}

# Run the main function
if __name__ == "__main__":
    main()
