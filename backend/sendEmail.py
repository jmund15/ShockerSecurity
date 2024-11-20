import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from SQLiteConnect import getAllEmails

def alertUsers(image_path):
    time = datetime.now().strftime("%I:%M %p")

    recipient_emails = getAllEmails() 
    for email in recipient_emails:
        #sendEmail(time, email)
        sendEmail(time, email, image_path)

def sendEmail(time, recipient_email, image_path = None):
    smtp_server = 'smtp.gmail.com' #sender email must be gmail (use smtp-mail.outlook.com if using outlook email)
    smtp_port = 587
    sender_email = 'shockerscrty.noreply@gmail.com'  # Replace with account email
    sender_password = 'ShockerSecurity3!'  # Replace with account password

    subject = "Detected Unidentified Person"
    body = f"An identified person was seen at {time}."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if image_path is not None:
        with open(image_path, 'rb') as fp:
            img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename='unaccepted_face.jpg')
        msg.attach(img)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

