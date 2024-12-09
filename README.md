# Scheduled Email Sending Application

This application allows users to automatically send emails at a specified date and time. Users can enter the content of the email and recipient information to schedule their emails for delivery at their desired time.

## Technologies Used

- **Streamlit**: A Python library for creating quick and interactive web applications.
- **Python**: The primary programming language for the application.
- **Gmail API**: Google’s API for sending emails via Gmail.

## Installation

### 1. Setting Up the Gmail API

1. Go to the **Google Cloud Console**: [Google Cloud Console].
2. Create a new project or select an existing one.
3. Navigate to "API & Services" and select the "Library" section.
4. Search for "Gmail API" and enable it.
5. Go to "API & Services" and select the "Credentials" section.
6. Click on the "Create Credentials" button and choose "OAuth client ID".
7. Fill in the "Application Name" and "OAuth consent screen" information.
8. Select "Desktop app" and click the "Create" button.
9. Download the generated `credentials.json` file and place it in the root directory of your application.

### 2. Installing Required Libraries

Before running the application, you need to install the required libraries. Run the following command in your terminal:

> pip install -r requirements.txt


### 3. Running the Application
To start the application, use the following command in your terminal:

> streamlit run app.py


## Relevant Links
[Gmail API](https://developers.google.com/gmail/api/guides?hl=tr)

[Streamlit](https://streamlit.io/)

## Contact Information
For any questions or feedback, feel free to contact me:

Email: [kptnhanife.2002@gmail.com](mailto:kptnhanife.2002@gmail.com )

Linkedin: [My Linkedin](https://www.linkedin.com/in/hanifekaptan-u1f90d/)
