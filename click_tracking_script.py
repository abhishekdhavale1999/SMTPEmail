# click_tracking_script.py

import streamlit as st

def track_click(recipient_email, unique_link):
    with open('clicks.log', 'a+') as logfile:
        existing_data = logfile.readlines()
        exists = any(f"{recipient_email},{unique_link}" in line for line in existing_data)
        if not exists:
            logfile.write(f"{recipient_email},{unique_link}\n")

def main():
    st.title('Click Tracking')

    recipient_email = st.text_input('Recipient Email')
    unique_link = st.text_input('Unique Link')

    if st.button('Track Click'):
        track_click(recipient_email, unique_link)
        st.success('Click tracked successfully!')

if __name__ == "__main__":
    main()
