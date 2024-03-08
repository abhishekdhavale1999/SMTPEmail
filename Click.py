import streamlit as st
from email_sender import send_email
from click_tracker import track_click

def main():
    st.title('Email Click Tracking App')
    
    # Email Sending Section
    st.header('Send Email')
    sender_email = st.text_input('Sender Email')
    sender_password = st.text_input('Sender Password', type='password')
    recipient_email = st.text_input('Recipient Email')
    unique_link = st.text_input('Unique Link')
    if st.button('Send Email'):
        send_email(sender_email, sender_password, recipient_email, unique_link)
        st.success('Email sent successfully!')

    # Click Tracking Section
    st.header('Click Tracking')
    recipient_email = st.text_input('Recipient Email for Click Tracking')
    unique_link = st.text_input('Unique Link for Click Tracking')
    if st.button('Track Click'):
        track_click(recipient_email, unique_link)
        st.success('Click tracked successfully!')

if __name__ == "__main__":
    main()
