def getDocument(filename):
    try:
        f = open("replies/"+filename, 'r')
        strBuilder = ""
        for line in f:
            strBuilder += line
        f.close()
        return strBuilder
    except:
        print("Error opening file",filename)
        return False

def question(content, index):
    if index == "5" or index == "8" or index == "11": #Very familiar / Somewhat familiar / Unfamiliar question
        which = ["Very familiar","Somewhat familiar","Unfamiliar"]
        if content not in which:
            print("Error parsing question",index)
            return False
        return getDocument(index+"-"+str(which.index(content)+1)+".html")
    
    elif index == "6" or index == "9" or index == "12": #Yes / No / Not sure question
        which = ["Yes","No","Not sure"]
        if content not in which:
            if content == "[Not asked]":
                return ""
            print("Error parsing question",index)
            return False
        return getDocument(index+"-"+str(which.index(content)+1)+".html")

    elif index == "13" or index == "14": #Scale questions 1 - 5
        try:
            content = int(content)
            if content < 0 or content > 5:
                raise IndexError("Response "+content+" out of bounds.") 
        except:
            print("Error parsing question",index)
            return False 
        if content > 4: 
            return getDocument(index+"-1.html")
        elif content > 2:
            return getDocument(index+"-2.html")
        else:
            return getDocument(index+"-3.html")


    elif index == "7": #Antivirus... 
        which = ["identifies and removes viruses","pretends to be legitimate but is actually malicious code","protects your IP address","only scans files you download for viruses","not sure"]
        if content not in which:
            if content == "[Not asked]":
                return ""
            print("Error parsing question",index,content)
            return False
        return getDocument(index+"-"+str(which.index(content)+1)+".html")
    
    elif index == "10": #A firewall...
        which = ["blocks / allows connections","blocks / allows malware","protects your IP address","protects you from phishing emails","not sure"]
        if content not in which:
            if content == "[Not asked]":
                return ""
            print("Error parsing question",index)
            return False
        return getDocument(index+"-"+str(which.index(content)+1)+".html")

    elif index == "15":
        try:
            content = int(content)
            if content > 5:
                return getDocument(index+"-1.html")
            elif content > 3:
                return getDocument(index+"-2.html")
            else:
                return getDocument(index+"-3.html")
        except:
            print("Error parsing question",index)
            return False


    elif index == "16": #How many characters is your longest password?
        try:
            content = int(content)
            if content > 10:
                return getDocument(index+"-1.html")
            elif content > 7:
                return getDocument(index+"-2.html")
            else:
                return getDocument(index+"-3.html")
        except:
            print("Error parsing question",index)
            return False

    else:
        raise IndexError("Question "+index+" out of bounds.")
        return False
