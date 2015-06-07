import smtplib
import socket
from email.MIMEText import MIMEText

def send_email(receiver, subject, body):
    HOST = "smtp.gmail.com"
    PORT = "587"
    socket.setdefaulttimeout(None)
    sender= "wheredabathroomatdoe@gmail.com"
    with open('emailpassword', 'r') as f:
        password = f.read().strip()
   
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    server = smtplib.SMTP()
    server.connect(HOST, PORT)
    server.starttls()
    server.login(sender,password)
    server.sendmail(sender,receiver, msg.as_string())
    server.close()

def send_confirmation_email(receiver, first_name, url_id):
    email_body_template = '''
    Dear %(name)s,
    Please click <a href="%(url)s target="_blank"">here</a> to confirm your email address.
    Alternatively, here is a direct link: %(url)s
    Thank you for registering for wheredabathroomatdoe?!
    '''
    email_body = email_body_template%{ 'name': first_name
                                     , 'url': "http://www.chesley.party:8000/confirm/email/%s"%url_id
                                     }
    send_email(receiver, "wheredabathroomatdoe Account Confirmation", email_body)

#send_email("erickolbusz@gmail.com","TEST1","hey its works bub")
#send_email("trunkatedpig@gmail.com","TEST2","hey its still works bub")
send_confirmation_email("erickolbusz@gmail.com","Eric","testurl")
