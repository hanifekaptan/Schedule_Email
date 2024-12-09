from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email_validator import EmailNotValidError, validate_email
import datetime
import base64
import os
import pickle
import streamlit as st

def authenticate(SCOPES):
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)
    

def check_emails(emails : str):
    try:
        return all(validate_email(email.strip()) for email in emails.split(","))
    
    except EmailNotValidError:
        st.error("Please enter a valid email.")
        return False


def sender_info(sender : str):
    if check_emails(sender) == True:
        message["from"] = sender


def receiver_info(to : str):
    if check_emails(to) == True:
        message["to"] = to


def subject_info(subject : str):
    message["subject"] = subject


def body_sign_info(body : str, signature : str = ""):
    if signature != "":
        body += f"\n\n{signature}"
    message["body"] = body
    message.attach(MIMEText(body, "plain"))


def cc_info(cc : str = ""):
    if cc != "":
        if check_emails(cc) == True:
            message["cc"] = cc


def bcc_info(bcc : str = ""):
    if bcc != "":
        if check_emails(bcc) == True:
            message["bcc"] = bcc


def schedule_info(date : datetime.date, time : datetime.time):
    dt = datetime.datetime.combine(date, time)
    now = datetime.datetime.now()
    if dt < now:
        st.error("The date and time value cannot be a past value.")
    else:
        schedule = dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    message["X-GM-Schedule-Time"] = schedule


def attachment_info(files):
        for file in files:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.getvalue())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition",
                            f"attachment; filename = {file.name}")
            message.attach(part)


def prepare_message(sender, receiver, subject, body, signature, cc, bcc, date, time, files):
    try:
        sender_info(sender)
        receiver_info(receiver)
        subject_info(subject)
        body_sign_info(body, signature)
        cc_info(cc)
        bcc_info(bcc)
        schedule_info(date, time)
        attachment_info(files)
        encoded_msg = base64.urlsafe_b64encode(message.as_string().encode("utf-8")).decode("utf-8")
        raw = {"raw": encoded_msg}
        return raw
    
    except:
        st.error("Message preparation failed!")


def send(raw):
    try:
        service.users().messages().send(userId = "me", body = raw).execute()
    
    except:
        st.error("Message sending failed!")


def app():
    st.set_page_config(page_title="Schedule E-Mail", page_icon="✉️", layout="centered")
    st.title("SEND A MESSAGE TO THE FUTURE!")
    sender = st.text_input("Sender:", placeholder="sender@example.com")
    receiver = st.text_input("Receivers: ", placeholder="recipient1@example.com, recipient2@example.com")
    subject = st.text_input("Subject:", placeholder="Enter the subject of the message")
    body = st.text_area("Body:", placeholder="Enter the body of the message")
    cc = st.text_input("CC:", placeholder="cc1@example.com, cc2@example.com (optional)")
    bcc = st.text_input("BCC:", placeholder="bcc1@example.com, bcc2@example.com (optional)")
    signature = st.text_input("Signature:", placeholder="Enter your signature (optional)")
    date = st.date_input("Schedule Date:")
    time = st.time_input("Schedule Time:")
    files = st.file_uploader("Choose files (must be max 25 MB)", accept_multiple_files=True)
    if files:
        total_size = sum(file.size for file in files)
        if total_size > 25 * 1024 * 1024:
            st.error("Total file size exceeds 25 MB. Please upload smaller files.")
    send_button = st.button("Send Message")
    if send_button:
        raw = prepare_message(sender, receiver, subject, body, signature, cc, bcc, date, time, files)
        send(raw)



SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
service = authenticate(SCOPES)

message = MIMEMultipart()

app()
