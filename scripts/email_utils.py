import smtplib
from email.message import EmailMessage
import re
from openai import OpenAI

with open('system_prompt.txt', 'r') as file:
    system_prompt = file.read().strip()

def generate_email_content(last_response):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
    user_prompt = last_response

    completion = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
    )
    response = completion.choices[0].message.content

    pattern = r"(From:|To:|Subject:|Body:)(.*?)(?=(?:\nFrom:|\nTo:|\nSubject:|\nBody:|$))"
    matches = re.finditer(pattern, response, re.DOTALL)
    parts = {match.group(1).strip(':'): match.group(2).strip() for match in matches}
    return parts

def send_phishing_email(subject, body):
    smtp_server = ''
    smtp_port = 587
    smtp_username = ''
    smtp_password = ''
    msg = EmailMessage()
    msg['From'] = ""
    msg['To'] = ""
    msg['Subject'] = subject
    msg.set_content(body)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

    print("Email sent successfully!")