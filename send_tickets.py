import smtplib, ssl, csv

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import time
import json

users = json.loads(open("data/users.json").read())
failed = []
count = 1

with open(f"data/schedule.png", "rb") as f:
    schedule = MIMEApplication(f.read(), _subtype="png")
schedule.add_header("Content-Disposition", "attachment", filename=str("schedule.png"))

# START: create message
def get_message(name, seatNo, filename):
    try:
        multi_message = MIMEMultipart()
        multi_message["From"] = "TEDxCUSAT 2022 <tedxcusat2021@gmail.com>"
        multi_message["Subject"] = "Booking Confirmed!"

        body = f"""Dear {name},

Thank you for booking seat no: {seatNo} for TEDxCUSAT 2022, Transcendence: Beyond all Bounds. The official event is held at the CUSAT seminar complex at 9am on April 2nd. 

Please observe the following details:
- This event requires you to have this ticket available when reaching the venue.
- Please arrive on time, at 9am sharp.
- Food and drinks will be provided to you at scheduled times. 
- At the end of the event, please ensure you receive a goodie bag from the exit gate.

We hope you enjoy the event!

Regards,
Suryanarayanan R
9446114249
"""
        # Add body to email

        with open(f"tickets/{filename}.png", "rb") as f:
            ticket = MIMEApplication(f.read(), _subtype="png")
        ticket.add_header(
            "Content-Disposition", "attachment", filename=str("ticket.png")
        )

        multi_message.attach(MIMEText(body, "plain"))
        multi_message.attach(ticket)
        multi_message.attach(schedule)
        message = multi_message.as_string()
        return message
    except:
        print(f"Ticket not found for {name}")


# END: create message

sender_email = "tedxcusat2021@gmail.com"
password = "tedxtedx"

context = ssl.create_default_context()
server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
server.login(sender_email, password)
# END: server login

for user in users:
    try:
        message = get_message(
            user["name"].upper(),
            user["seatNo"],
            f"{user['email'].split('@')[0]}",
        )
        server.sendmail(sender_email, user["email"], message)
        print(f"{count}: Success: {user['email']} - Ticket sending")
    except:
        print(f"{count}: Failure: {user['email']} - Ticket sending")
        failed.append(user["email"])
        time.sleep(5)
    count += 1
