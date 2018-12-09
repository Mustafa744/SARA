import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests
import wikipedia
from weather import Weather
import pyttsx

speech = pyttsx.init()
voices = speech.getProperty('voices')
speech.setProperty('voice', voices[0].id)

def talkToMe(audio):
    "speaks audio passed as argument"

    print(audio)
    for line in audio.splitlines():
        speech.say(audio)
        speech.runAndWait()

def myCommand():
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
            print('Done!')
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
                talkToMe('On %s will it %s. The maximum temperture will be %.1f degree.'
                         'The lowest temperature will be %.1f degrees.' % (forecasts[i].date(), forecasts[i].text(), (int(forecasts[i].high())-32)/1.8, (int(forecasts[i].low())-32)/1.8))


    elif 'exit' in command:
        exit()
    elif 'sarah' in command:
        speech.say("hi mustafa")
        speech.runAndWait()
    elif 'do you love me' in command:
        speech.say("dou  you.  doo you")
        speech.runAndWait()

    elif 'prodis' in command:
            os.startfile("C:\pr.lnk")
            print('Done!')
    elif "wikipedia" in command:
        reg_ex = re.search('wikipedia (.+)', command)
        if reg_ex:
           regex = re.compile('[^a-z A-Z]')
           summary = str((wikipedia.summary(reg_ex.group(1), sentences=1).encode("utf-8")))
           output= regex.sub('', summary)
           talkToMe(output)
            
        else:
            pass
                
        
    else:
        talkToMe('I don\'t know what you mean!')


talkToMe('I am ready for your command')

#loop to continue executing multiple commands
while True:
    assistant(myCommand())
