import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests
import wikipedia
from weather import Weather
import win32com.client as wincl
import time
import sys
sys.path.append('..')
import keyboard
from time import ctime
from subprocess import Popen, PIPE
import subprocess



speak = wincl.Dispatch("SAPI.SpVoice")

def talkToMe(audio):
    "speaks audio passed as argument"
 
    print(audio)
    speak.Speak(audio)

    


def myCommand():
    talkToMe("ready")

    "listens for commands"
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ready...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        talkToMe('sorry , didnt catch that')
        command = myCommand();

    return command


def assistant(command):
    "if statements for executing commands"
   
    if 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            
        else:
            pass
    elif 'google' in command :                    
        reg_ex = re.search('google (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = "https://www.google.com.tr/search?q={}".format(domain)
            webbrowser.open(url)
        else:
            pass
    elif 'where is' in command :                    
        reg_ex = re.search('where is (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = "https://www.google.nl/maps/place/{0}".format(domain)
            webbrowser.open(url)
            
        else:
            pass
        
    elif "wikipedia"  in command:
        reg_ex = re.search('wikipedia (.+)', command)
        if reg_ex:
           regex = re.compile('[^a-zA-Z ,;.1234567890]')
           summary = str((wikipedia.summary(reg_ex.group(1), sentences=3).encode("utf-8")))
           output= regex.sub('', summary)
           talkToMe(output)
            
        else:
            pass
    elif "you know about"  in command:
        reg_ex = re.search('you know about (.+)', command)
        if reg_ex:
           regex = re.compile('[^a-zA-Z ,;.1234567890]')
           summary = str((wikipedia.summary(reg_ex.group(1), sentences=3).encode("utf-8")))
           output= regex.sub('', summary)
           talkToMe(output)
            
        else:
            pass        
        
    elif 'what\'s up' in command:
        talkToMe('Just doing my thing')
        
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            talkToMe(str(res.json()['joke'].encode("utf-8")))
        else:
            talkToMe('oops!I ran out of jokes')

    elif 'current weather in' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            weather = Weather()
            location = weather.lookup_by_location(city)
            condition = location.condition()
            talkToMe('The Current weather in %s is %s The tempeture is %.1f degree' % (city, condition.text(), (int(condition.temp())-32)/1.8))

    elif 'weather forecast in' in command:
        reg_ex = re.search('weather forecast in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            weather = Weather()
            location = weather.lookup_by_location(city)
            forecasts = location.forecast()
            for i in range(0,3):
                talkToMe('On %s will it %s. The maximum temperature will be %.1f degree.'
                         'The lowest temperature will be %.1f degrees.' % (forecasts[i].date(), forecasts[i].text(), (int(forecasts[i].high())-32)/1.8, (int(forecasts[i].low())-32)/1.8))



    #elif 'sarah' in command:
        #talkToMe("yes, mustafa?")
        
    elif 'do you love me' in command:
        talkToMe("yes, i love you mustafa <3")
      
        
    elif "run" in command:
        if "face detection" in command:
            process = Popen(['python', 'C:\python27\cascad.py'], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            print stdout
            
        elif "python" in command :
            os.startfile("C:\shortcuts\idle.lnk")
        elif "instagram" in command:
            os.startfile("C:\shortcuts\insta.lnk")

        elif 'prodis' in command:
            os.startfile("C:\shortcuts\pr.lnk")
        elif "arduino" in command :
            os.startfile("C:\shortcuts\crd.lnk")
        elif "cmd" in command :
            os.startfile("C:\shortcuts\cmd.lnk")
        else :
            talkToMe("file doesnt exist")
            

    elif 'exit' in command:
        exit()
        
    elif 'time' in command :
        talkToMe(ctime())
        pass
   
                   
    else:
        talkToMe('I don\'t know what you mean!')


talkToMe('I am ready for your command')

#loop to continue executing multiple commands

"""
Prints the scan code of all currently pressed keys.
Updates on every keyboard event.
"""

def Keyboard_record(e):
    line = ', '.join(str(code) for code in keyboard._pressed_events)
	# '\r' and end='' overwrites the previous line.
	# ' '*40 prints 40 spaces at the end to ensure the previous line is cleared.
    if line == "82":
        assistant(myCommand())
        talkToMe("done")
    else :
        return 1


    
keyboard.hook(Keyboard_record)
while 1:
    time.sleep(0.01)
