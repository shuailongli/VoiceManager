from Online_Search import online_search
from Local_File import local_file
import time
import math
import os
from AudioProcess import speak

def audioexecute(mywords):
    if "Friday" in mywords:
        fwrite=open("temp/initializer.txt",'w')
        fwrite.write("T")
        fwrite.close()
        React=False
        Reacted=False
        return [React,Reacted]
            
    if "quit" in mywords or "exit" in mywords:
        reply="Ok, Bye"
        speak(reply)
        fwrite=open("temp/initializer.txt",'w')
        fwrite.write("NAN")
        fwrite.close()
        quit()
    
    if "thanks" in mywords or "thank" in mywords or "bye-bye" in mywords or "bye" in mywords:
        reply="Ok, Bye"
        speak(reply)
        #print('\a')
        React=False
        Reacted=False
        return [React,Reacted]
            
    bool1="wait" in mywords
    bool2="one" in mywords and "second" in mywords and (mywords.index("second")-mywords.index("one"))==1
    bool3="one" in mywords and "moment" in mywords and (mywords.index("moment")-mywords.index("one"))==1
    if  bool1 or bool2 or bool3:
        reply="Ok, take your time"
        speak(reply)
        #print('\a')
        time.sleep(5)
        React=True
        Reacted=True
        return [React,Reacted]
    
    KeyCommandList=[["go", "up"],["go", "down"],["scroll","up"],["scroll","down"]]
    KeyControllerList=["Key.page_up","Key.page_down","Key.up","Key.down"]
    for entry in KeyCommandList:
        if all(ele in mywords for ele in entry):
            command="python3 KeyboardControll.py "+KeyControllerList[KeyCommandList.index(entry)]
            os.system(command)
            React=True
            Reacted=True
            return [React,Reacted]

    if "time" in mywords:
        if time.localtime().tm_hour<12:
            reply="It's "+str(time.localtime().tm_hour)+" "+str(time.localtime().tm_min)+" am"
        else:
            reply="It's "+str(time.localtime().tm_hour-12)+" "+str(time.localtime().tm_min)+" pm"
            print(reply)
            speak(reply)
        React=True
        Reacted=True
        return [React,Reacted]
    
    if "date" in mywords:
        reply="It's "+time.strftime("%A, %B, ", time.localtime())+str(time.localtime().tm_mday)+" ,"+str(time.localtime().tm_year)
        print(reply)
        speak(reply)
        React=True
        Reacted=True
        return [React,Reacted]

    
    local_search=local_file()
    method1=local_search.action(mywords,False)
    method2=online_search(mywords,False)
    if method1>0 or method2>0:
        if method1>method2: local_search.action(mywords,True)
        else: online_search(mywords,True)
        Reacted=True
        React=True
        return [React,Reacted]
    
    if "Friday" in mywords:
        Reacted=True
        React=False
        return [React,Reacted]
    
    React=True
    Reacted=False
    return [React,Reacted]

