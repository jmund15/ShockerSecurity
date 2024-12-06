import smtplib
import socket
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import threading

from SQLiteConnect import getAllEmails

def get_local_ip():
    try:
        # Create a socket and connect to an external host (e.g., Google's DNS server)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        # This does not actually connect, but gets the local IP address
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return f"Error fetching local IP address: {e}"

def alertUsers(image_path, name = 'Unidentified'):
    time = datetime.now().strftime("%I:%M %p")
    day = datetime.now().strftime("%m/%d/%Y")
    local_ip = get_local_ip()
    print('local ip: ', local_ip)
    
    recipient_emails = getAllEmails() 

    subject = "ShockerSecurity Alert: "
    if name != 'Unidentified':
        subject += "Detected Unauthorized Person!"
    else:
        subject += "Detected Unidentified Person!"

    body = f"""
<html>
    <body>
        <p>The unauthorized individual labeled "{name}" was seen at {time} on {day}. See the attached image for details.</p>
        <p>To make adjustments, login <a href="http://{local_ip}:3000">here</a>.</p>
    </body>
</html>
"""
    #http://192.168.155.54:3000

    # Example usage
    sendEmailInThread(
        recipient_emails=recipient_emails,
        subject=subject,
        body_html=body,
        image_path=image_path
    )
    #sendEmail(recipient_emails, subject, body, image_path)

def sendEmail(recipient_emails, subject, body_html, image_path=None):
    #print('sending email! \n\tsubject: ', subject, '\n\tbody: ', body_html, '\n\temails: ', recipient_emails, '\n\timage: ', image_path)
    
    smtp_server = 'smtp.gmail.com'  # SMTP server (use smtp-mail.outlook.com for Outlook)
    smtp_port = 465  # SSL port (use 587 for STARTTLS)
    sender_email = 'shockerscrty.noreply@gmail.com'  # Sender email
    sender_password = 'xnue bvwz mdrs nreo'  # Sender password (or app password if 2FA is enabled)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails)  # Join the list of emails into a single comma-separated string
    msg['Subject'] = subject

    # Attach the body text to the email
    msg.attach(MIMEText(body_html, 'html'))
    #print('attached body!')

    if image_path is not None:
        with open(image_path, 'rb') as fp:
            img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename='unaccepted_face.jpg')
        msg.attach(img)

    #print('attached image!')

    try:
        # Use SMTP_SSL to directly create an SSL connection
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            #print('opened server')
            server.login(sender_email, sender_password)  # Login to the server
            #print('logged in!')
            server.sendmail(sender_email, recipient_emails, msg.as_string())  # Send the email to multiple recipients
            print('email sent!')
    except Exception as e:
        print('Error:', e)

    # with smtplib.SMTP(smtp_server, smtp_port) as server:
    #     print('opened server')
    #     server.starttls()
    #     print('started tls!')
    #     server.login(sender_email, sender_password)
    #     print('logged in!')
    #     server.sendmail(sender_email, recipient_email, msg.as_string())

def sendEmailInThread(recipient_emails, subject, body_html, image_path=None):
    # This wrapper function will run sendEmail in a new thread
    email_thread = threading.Thread(target=sendEmail, args=(recipient_emails, subject, body_html, image_path))
    email_thread.start()  # Start the thread

