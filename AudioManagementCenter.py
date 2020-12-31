from gtts import gTTS
import os
import speech_recognition as sr
import time
import math
from Online_Search import online_search
import Local_File
from AudioExecute import audioexecute
import AudioProcess
from multiprocessing import Process

global React #whether initilzed
global Reacted   #whether a event successfully handled

React=False
Reacted=False

def Initializer(label):
    
    mytext=AudioProcess.listen("                        Initializer")
    mywords=list(mytext.split(" "))
    if "Friday" in mywords:
        #print("                        initializer ",label," reacted")
        print("you said: ",mytext)
        fwrite=open("temp/initializer.txt",'w')
        fwrite.write("T")
        fwrite.close()
    elif "quit" in mywords or "exit" in mywords:
        print("Bye")
        fwrite=open("temp/initializer.txt",'w')
        fwrite.write("NAN")
        fwrite.close()
    else: 1



def event_loop():
    global React
    global Reacted
    global local_search
    #print("                        event loop is called")
    while React:
        #print("                        entered event loop")
        if Reacted==False:
            reply="Hi"
            print("-----------------------------------------")
            AudioProcess.speak(reply)
            #print('\a')
        else:
            reply="Ok"
            print("-----------------------------------------")
            AudioProcess.speak(reply)
            #print('\a')
            Reacted=False
        
        while ((not Reacted) and React):
            mysentence=AudioProcess.listen()
            mywords=list(mysentence.split(" "))
            [React,Reacted]=audioexecute(mywords)

            if (not Reacted) and React:
                reply="Sorry"
                print("-----------------------------------------")
                AudioProcess.speak(reply)
                #print('\a\a')

if __name__ == '__main__':
    EventLoop=Process(target=event_loop)
    while True:
        Initializer1=Process(target=Initializer,args=('1'))
        Initializer1.start()
        Initializer1.join(5)
        #print("--------------------------initialized")
        fread=open("temp/initializer.txt",'r')
        word=fread.read()
        #print(word,end="\r")
        is_init=True if word=="T" else False
        if word=="NAN": quit()
        fread.close()
        fwrite=open("temp/initializer.txt",'w')
        fwrite.write("F")
        fwrite.close()
        if is_init:
            React=True
            if EventLoop.is_alive():
                EventLoop.terminate()
                EventLoop=Process(target=event_loop)
                EventLoop.start()
                EventLoop.join(1)
            else:
                EventLoop=Process(target=event_loop)
                EventLoop.start()
                EventLoop.join(1)
        
        if Initializer1.is_alive(): Initializer1.terminate()





