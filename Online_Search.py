import math
import speech_recognition as sr
from gtts import gTTS
import os
import clipboard


def listDifference(listA,listB):
    if len(listA)==len(listB):
        dist=(sum(listA)-sum(listB))/len(listA)
        norm=0
        for ii in range(len(listA)):
            norm=norm+abs(listA[ii]-dist-listB[ii])
    return norm

def online_search(mywords,exe):
    KeyWordPrim=["Google","search","YouTube"]
    KeyWordSec=["open","how","what's","what","show","find"]
    score=0
    for word in mywords:
        if word in KeyWordPrim:
            score+=1
        if word in KeyWordSec:
            score+=0.5

    def openGoogle(mywords):
        if "open" in mywords and "Google" in mywords:
            subscore=2 if (mywords.index("Google")-mywords.index("open"))==1 else 0
            command="open https://www.google.com"
        else:
            subscore=0
            command=" "
        return [subscore,command]

    def openYouTube(mywords):
        if "open" in mywords and "YouTube" in mywords:
            subscore=2 if mywords.index("YouTube")-mywords.index("open")==1 else 0
            command="open https://www.youtube.com"
        else:
            subscore=0
            command=" "
        return [subscore,command]
    
    def SearchClipboard(mywords):
        if "search" in mywords and "it" in mywords and mywords.index("it")-mywords.index("search")==1:
            subscore=3
            cliptext = clipboard.paste()
            clipwords=list(cliptext.split(" "))
            googleURL='+'.join(clipwords)
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]
    
    def search(mywords):
        if "search" in mywords:
            subscore=1 if (len(mywords)-1)>mywords.index("search") else 0
            googleURL='+'.join(mywords[(mywords.index("search")+1):])
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]

    def open(mywords):
        if "open" in mywords:
            subscore=1 if (len(mywords)-1)>mywords.index("open") else 0
            googleURL='+'.join(mywords[(mywords.index("open")+1):])
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]

    def search_InGoogle(mywords):
        if "search" in mywords and "in" in mywords and "Google" in mywords:
            model=[0,1]   #[distance between search and in>1, distance between in and Google]
            extract=[(mywords.index("in")-mywords.index("search"))<1,(mywords.index("Google")-mywords.index("in"))]
            subscore=3.*math.exp(-listDifference(model,extract))
            googleURL='+'.join(mywords[(mywords.index("search")+1):mywords.index("in")])
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]

    def google(mywords):
        if "Google" in mywords:
            subscore=1 if (len(mywords)-1)>mywords.index("Google") else 0
            googleURL='+'.join(mywords[(mywords.index("Google")+1):])
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]

    def open_InGoogle(mywords):
        if "open" in mywords and "in" in mywords and "Google" in mywords:
            model=[0,1]   #[distance between search and in>1, distance between in and Google]
            extract=[(mywords.index("in")-mywords.index("open"))<1,(mywords.index("Google")-mywords.index("in"))]
            subscore=3.*math.exp(-listDifference(model,extract))
            googleURL='+'.join(mywords[(mywords.index("open")+1):mywords.index("in")])
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]

    def how(mywords):
        if "how" in mywords:
            subscore=1 if (len(mywords)-1)>mywords.index("how") else 0
            googleURL='+'.join(mywords[mywords.index("how"):])
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]

    def howTo(mywords):
        if "how" in mywords and "to" in mywords:
            subscore=2 if (mywords.index("to")-mywords.index("how")==1) and (len(mywords)-2)>mywords.index("how") else 0
            googleURL='+'.join(mywords[mywords.index("how"):])
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]

    def what(mywords):
        if "what" in mywords:
            subscore=1 if (len(mywords)-1>mywords.index("what")) else 0
            googleURL='+'.join(mywords[mywords.index("what"):])
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]

    def whatIs(mywords):
        if "what's" in mywords:
            subscore=1 if (len(mywords)-1)>mywords.index("what's") else 0
            googleURL='+'.join(mywords[mywords.index("what's")+1:])
            googleURL="whats+"+googleURL
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]

    def show(mywords):
        if "show" in mywords:
            subscore=1 if (len(mywords)-1)>mywords.index("show") else 0
            googleURL='+'.join(mywords[(mywords.index("show")+1):])
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]

    def showMe(mywords):
        if "show" in mywords and "me" in mywords:
            subscore=2 if (mywords.index("me")-mywords.index("show")==1) and ((len(mywords)-2)>mywords.index("show")) else 0
            googleURL='+'.join(mywords[mywords.index("me")+1:])
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]

    def showMe_InGoogle(mywords):
        if "show" in mywords and "me" in mywords and "in" in mywords and "Google" in mywords:
            model=[1,0,1]   #[dist between show and me, distance between me and in>1, distance between in and Google]
            extract=[mywords.index("me")-mywords.index("show"),(mywords.index("in")-mywords.index("me"))<1,mywords.index("Google")-mywords.index("in")]
            subscore=4.*math.exp(-listDifference(model,extract))
            googleURL='+'.join(mywords[(mywords.index("me")+1):mywords.index("in")])
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]

    def find(mywords):
        if "find" in mywords:
            subscore=1 if (len(mywords)-1)>mywords.index("find") else 0
            googleURL='+'.join(mywords[(mywords.index("find")+1):])
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]

    def find_InGoogle(mywords):
        if "find" in mywords and "in" in mywords and "Google" in mywords:
            model=[0,1]   #[distance between search and in>1, distance between in and Google]
            extract=[(mywords.index("in")-mywords.index("find"))<1,(mywords.index("Google")-mywords.index("in"))]
            subscore=3.*math.exp(-listDifference(model,extract))
            googleURL='+'.join(mywords[(mywords.index("find")+1):mywords.index("in")])
            command="open http://www.google.com/search?q="+googleURL
        else:
            subscore=0
            command=" "
        return [subscore,command]

    listfunc=[openGoogle, openYouTube, search, open, search_InGoogle, google, open_InGoogle, how, howTo, what, whatIs, show, showMe, showMe_InGoogle, find, find_InGoogle,SearchClipboard]
    subscore=0
    optimized_func=listfunc[0]
    for func in listfunc:
        ind_score=func(mywords)[0]
        #if not exe: print(func.__name__, ind_score)
        if subscore<ind_score:
            subscore=ind_score
            optimized_func=func
    if exe:
        command=optimized_func(mywords)[1]
        os.system(command)
    return score+subscore


