from getpass import getpass
import sys
import json
from smtplib import SMTP, SMTPAuthenticationError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def getImprovements(email):
    f = open("improv.json")
    improv = json.load(f)
    f.close()
    try:
        array = improv[email]
    except KeyError:
        return "Nothing!"
    toAppend = "<ol type='1'>"
    for i in array:
        toAppend += "<li>" + i + "</li><br>"
    return toAppend + "</ol>"


def getHTML():
    f = open("video1.html")
    html = f.read()
    f = open("style.css")
    style = f.read()
    html = "<style>" + style + "</style>" + html
    html = html.replace("[X]", sys.argv[2])
    html = html.replace("[Y]", getImprovements(sys.argv[1]))
    return html


def reply(recipient, password):
    mail = SMTP("smtp.office365.com", 587)
    mail.ehlo()
    mail.starttls()
    payload = getHTML()
    if not payload:
        return False
    sender = "mark.turner-7@postgrad.manchester.ac.uk"
    mail.login(sender, password)
    print(payload)
    msg = MIMEMultipart("related")
    payload = MIMEText(payload, "html")
    msg.attach(payload)
    msg["To"] = recipient
    msg["From"] = sender
    msg["Subject"] = "Video to watch for my Dissertation - Cyber Essentials at Home"
    mail.sendmail(sender, recipient, msg.as_string())
    mail.close()
    print(payload)
    print("Email sent!")
    return True


if __name__ == "__main__":
    try:
        if not reply(sys.argv[1], getpass("Password for mark.turner-7@postgrad.manchester.ac.uk:\t")):
            sys.exit(1)
    except IndexError:
        print("Command-line argumemnt must include recipient's email address and name")
        sys.exit(1)
    except SMTPAuthenticationError:
        print("Password incorrect!")
        sys.exit(1)
