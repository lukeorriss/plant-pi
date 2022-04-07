import smtplib
import ssl
from email.mime.text import MIMEText

# Initialise Email
smtp_server = "smtp.titan.email"
smtp_port = 465
sender = "noreply@lukeorriss.com"
password = "6#73K7HRfT&hDED!"
recipients = ['stuff@lukeorriss.com', 'lukeorriss@outlook.com']

def sendEmail(alert_type, subject, reason, temperature, humidity, moisture):
    context = ssl.create_default_context()
    s = smtplib.SMTP_SSL(smtp_server, smtp_port, context)
    s.set_debuglevel(0)
    s.ehlo()
    s.login(sender, password)

    if alert_type == "dead":
        body = getMessageDead(reason, temperature, humidity, moisture)
    else:
        body = getMessageAlive(temperature, humidity, moisture)

    msg = MIMEText(body)
    msg['From'] = "No Reply | Plant Update"
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    s.sendmail(sender, recipients, msg.as_string())
    s.close()