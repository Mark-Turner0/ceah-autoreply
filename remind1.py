from getpass import getpass
import sys
import json
from smtplib import SMTP, SMTPAuthenticationError
from email.mime.text import MIMEText


def getHTML(recipient):
    f = open("remind1.html")
    html = f.read()
    f = open("style.css")
    style = f.read()
    html = "<style>" + style + "</style>" + html
    f = open("license.html")
    license = f.read()
    f = open("codes.json")
    codes = json.load(f)
    f.close()
    try:
        return html.replace("1234567890", codes[recipient]).replace("[LICENSE]", license)
    except Exception:
        print("No unique code found for", recipient)
        return False


def reply(recipient, password):
    mail = SMTP("smtp.office365.com", 587)
    mail.ehlo()
    mail.starttls()
    payload = getHTML(recipient)
    if not payload:
        return False
    sender = "mark.turner-7@postgrad.manchester.ac.uk"
    mail.login(sender, password)
    print(payload)
    payload = MIMEText(payload, "html")
    payload["To"] = recipient
    payload["From"] = sender
    payload["Subject"] = "Reminder - The Cyber Essentials at Home tool is ready!"
    mail.sendmail(sender, recipient, payload.as_string())
    mail.close()
    print(payload)
    print("Email sent!")
    return True


if __name__ == "__main__":
    password = getpass("Password for mark.turner-7@postgrad.manchester.ac.uk:\t")
    f = open("remind.json")
    reminding = json.load(f)
    f.close()
    for i in reminding.keys():
        try:
            if not reply(i, password):
                sys.exit(1)
        except IndexError:
            print("Command-line argumemnt must include recipient's email address")
            sys.exit(1)
        except SMTPAuthenticationError:
            print("Password incorrect!")
            sys.exit(1)
