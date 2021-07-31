from time import sleep
from imaplib import IMAP4_SSL
from smtplib import SMTP
from email import message_from_bytes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from socket import gaierror
from responder import question
import sys


def makePayload(message):
    message = message.decode().strip().split("<br>")[2:-1]
    if len(message) != 14:
        print("Parsing error")
        return False
    toSend = []
    toSendHTML = []
    count = 1
    for i in range(len(message)):
        toAppend = question(message[i], str(i + 5))
        if toAppend is False:
            return False
        elif toAppend != "":
            toSend.append("______________________________\n\n𝑄𝑢𝑒𝑠𝑡𝑖𝑜𝑛 " + str(count) + ": " + toAppend)
            toSendHTML.append("<hr><br><i>Question " + str(count) + "</i>: " + toAppend.replace('\n', "<br>"))
            count += 1
    return "\n".join(toSend), "<br>".join(toSendHTML)


def reply(message, password):
    mail = SMTP("smtp.office365.com", 587)
    mail.ehlo()
    mail.starttls()

    f = open("style.css")
    style = f.read()
    f.close()
    payloadHTML = "<style>" + style + "</style>"
    payloadHTML += '<body><h1 style="font-size:40px;font-weight:700;">Cyber Essentials at Home </h1><hr>'
    payload = "𝗧𝗛𝗔𝗡𝗞 𝗬𝗢𝗨 𝗙𝗢𝗥 𝗧𝗔𝗞𝗜𝗡𝗚 𝗣𝗔𝗥𝗧 𝗜𝗡 𝗧𝗛𝗘 𝗖𝗬𝗕𝗘𝗥 𝗘𝗦𝗦𝗘𝗡𝗧𝗜𝗔𝗟𝗦 𝗔𝗧 𝗛𝗢𝗠𝗘 𝗜𝗡𝗜𝗧𝗜𝗔𝗟 𝗦𝗨𝗥𝗩𝗘𝗬!\n\n"
    payloadHTML += "<p><b style='font-size:20px;'>THANK YOU FOR TAKING PART IN THE CYBER ESSENTIALS AT HOME SURVEY!</b><br><br>"
    payload += "Below are your responses with some brief feedback just for you:\n\n"
    payloadHTML += "Below are your responses with some brief feedback just for you:<br>"
    payload += "P͟l͟e͟a͟s͟e͟ ͟t͟a͟k͟e͟ ͟t͟h͟e͟ ͟t͟i͟m͟e͟ ͟t͟o͟ ͟r͟e͟a͟d͟ ͟t͟h͟e͟m͟, and I will contact you with a follow-up!\n\n"
    payloadHTML += "<u>Please take the time to read them,</u> and I will contact you with a follow-up!</p>"
    content, contentHTML = makePayload(message.get_payload(decode=True))
    if not content:
        return False
    payload += content
    payloadHTML += contentHTML

    sender = "mark.turner-7@postgrad.manchester.ac.uk"
    recipient = message["Reply-To"]
    mail.login("mark.turner-7@postgrad.manchester.ac.uk", password)
    final = MIMEMultipart("alternative")
    payload = MIMEText(payload, "plain", "utf-8")
    print(payloadHTML)
    payloadHTML = MIMEText(payloadHTML, "html")
    final.attach(payload)
    final.attach(payloadHTML)
    final["To"] = recipient
    final["From"] = sender
    final["Subject"] = "Reponses to Survey Questions"
    mail.sendmail(sender, recipient, final.as_string())
    mail.close()
    return True


def main():
    try:
        password = sys.argv[1]
    except IndexError:
        print("Command-line argument must contain password")
        sys.exit(1)
    while True:
        try:
            f = open("log.txt", 'r')
            log = [line.strip() for line in f]
            f.close()
        except FileNotFoundError:
            print("Existing log file not found, creating one...")
            f = open("log.txt", 'x')
            log = []
            f.close()
        try:
            mail = IMAP4_SSL('outlook.office365.com')
        except gaierror:
            continue
        try:
            mail.login('mark.turner-7@postgrad.manchester.ac.uk', password)
        except Exception:
            print("Password incorrect. Quiting...")
            sys.exit(1)
        mail.list()
        mail.select("inbox")
        _, data = mail.search(None, "SUBJECT", "NewresponseforCyberEssentialsatHomeSurvey\r\n")
        try:
            latest = data[0].split()[-1]
        except IndexError:
            print("No mail found.")
            sleep(10)
            continue
        _, data = mail.fetch(latest, "(RFC822)")
        response = message_from_bytes(data[0][1])
        if response["Message-Id"] in log:
            print("Latest mail already replied to.")
            sleep(10)
            continue
        if reply(response, password):
            print("\nResponse sent successfully!")
            f = open("log.txt", 'a')
            f.write(response["Message-Id"] + "\n")
            f.close()
        else:
            print("Error sending email. Stopping program for security.")
            sys.exit(1)
        sleep(10)
    del password


if __name__ == '__main__':
    main()
