import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from backend.SQLiteConnect import getAllEmails

def sendEmail(time, recipient_email):
    smtp_server = 'smtp.gmail.com' #sender email must be gmail (use smtp-mail.outlook.com if using outlook email)
    smtp_port = 587
    sender_email = ''  # Replace with account email
    sender_password = ''  # Replace with account password

    subject = "Detected Unidentified Person"
    body = f"An identified person was seen at {time}."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # with open(image_path, 'rb') as fp:
    #     img = MIMEImage(fp.read())
    # img.add_header('Content-Disposition', 'attachment', filename='image.jpg')
    # msg.attach(img)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

if __name__ == "__main__":
    time = datetime.now().strftime("%I:%M %p")
    #image_path = ''

    recipient_emails = getAllEmails() 
    for email in recipient_emails:
        sendEmail(time, email)
        #sendEmail(time, image_path, email)
