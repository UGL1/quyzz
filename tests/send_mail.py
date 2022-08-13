import smtplib
from email.message import EmailMessage

smtp_hostname = "mail.mailo.com"
smtp_port = 587
smtp_login = "ugli@mailo.com"
smtp_password = "***"

sender = "ugli@mailo.com"
destination = "uglimusic@gmail.com"
title = "titre"
content = "contenu"


def send_text_mail(sender, destination, title, content):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = title
    msg['From'] = sender
    msg['To'] = destination
    s = smtplib.SMTP(host=smtp_hostname, port=smtp_port)  # 587 : out port no encryption
    s.login(user=smtp_login, password=smtp_password)
    s.send_message(msg)
    s.quit()


send_text_mail("ugli@mailo.com", "ugli@mailo.com", "test", "ceci est un test")

"""
IMAP4 configuration parameters
Account name:
Your full e-mail address
ugli@mailo.com
Password:
The password of your account
 
Mail server *:
mail.mailo.com
Recommended parameters:
SSL – port: 993
Other possible parameters:
No encryption – port: 143
 
SMTP outgoing mail server *:
mail.mailo.com
Authentication:
Required
Recommended parameters:
SSL – port: 465
Other possible parameters:
No encryption – port: 587
"""
