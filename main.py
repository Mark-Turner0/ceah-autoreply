from time import sleep
from imaplib import IMAP4_SSL
from smtplib import SMTP
from email import message_from_bytes
from getpass import getpass
from email.mime.text import MIMEText
from responder import *

def makePayload(message):
    message = message.decode().strip().split("<br>")[2:-1]
    if len(message) != 12:
        print("Parsing error")
        return False
    toSend = []
    for i in range(len(message)):
        toAppend = question(message[i],str(i+5))
        if toAppend == False:
            return False
        elif toAppend != "":
            toSend.append(toAppend)
    return "\n".join(toSend)

def reply(message, password):
    mail= SMTP("smtp.office365.com",587)
    mail.ehlo()
    mail.starttls()
    payload = "𝗧𝗵𝗮𝗻𝗸 𝘆𝗼𝘂 𝗳𝗼𝗿 𝘁𝗮𝗸𝗶𝗻𝗴 𝗽𝗮𝗿𝘁 𝗶𝗻 𝘁𝗵𝗲 𝗖𝘆𝗯𝗲𝗿 𝗘𝘀𝘀𝗲𝗻𝘁𝗶𝗮𝗹𝘀 𝗮𝘁 𝗛𝗼𝗺𝗲 𝗶𝗻𝗶𝘁𝗶𝗮𝗹 𝘀𝘂𝗿𝘃𝗲𝘆!! Below are your responses with some brief feedback:\n\n"
    payload += "Please take the time to read them, and I will contact you with a follow-up!\n\n"
    content = makePayload(message.get_payload(decode=True))
    if not content: return False
    payload += content
    sender= "mark.turner-7@postgrad.manchester.ac.uk"
    recipient = message["Reply-To"]
    mail.login("mark.turner-7@postgrad.manchester.ac.uk",password)
    print(payload)
    payload = MIMEText(payload, "plain", "utf-8")
    payload["To"] = recipient
    payload["From"] = sender
    payload["Subject"] = "Reponses to Survey Questions"
    mail.sendmail(sender,recipient, payload.as_string())
    mail.close()
    return True

def main():
    password = getpass("Enter password for mark.turner-7@postgrad.manchester.ac.uk:\t")
    while True:
        f = open("log.txt",'r')
        log = [line.strip() for line in f]
        f.close()
        mail = IMAP4_SSL('outlook.office365.com')
        try: 
            mail.login('mark.turner-7@postgrad.manchester.ac.uk', password)
        except:
            print("Password incorrect. Quiting...")
            break
        mail.list()
        mail.select("inbox")
        _, data = mail.search(None, "SUBJECT","NewresponseforCyberEssentialsatHomeSurvey\r\n")
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
            print("Response sent successfully!")
            f = open("log.txt",'a')
            f.write(response["Message-Id"]+"\n")
            f.close()
        else:
            print("Error sending email. Stopping program for security.")
            break
        sleep(10)
    del password

if __name__ == '__main__':
	main()
