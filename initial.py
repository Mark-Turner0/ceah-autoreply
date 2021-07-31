from getpass import getpass
import sys
from smtplib import SMTP, SMTPAuthenticationError
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def getHTML():
    f = open("index.html")
    html = f.read()
    f = open("style.css")
    style = f.read()
    html = "<style>" + style + "</style>" + html
    f = open("me.jpg", 'rb')
    img = MIMEImage(f.read())
    f.close()
    html = html.replace("[X]", sys.argv[2])
    return html, img


def reply(recipient, password):
    mail = SMTP("smtp.office365.com", 587)
    mail.ehlo()
    mail.starttls()
    payload, img = getHTML()
    if not payload:
        return False
    sender = "mark.turner-7@postgrad.manchester.ac.uk"
    mail.login(sender, password)
    print(payload)
    msg = MIMEMultipart("related")
    payload = MIMEText(payload, "html")
    msg.attach(payload)
    img.add_header("Content-ID", "<me>")
    msg["To"] = recipient
    msg["From"] = sender
    msg["Subject"] = "Survey for my Dissertation - Cyber Essentials at Home"
    msg.attach(img)
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
