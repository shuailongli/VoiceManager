import os
import fnmatch
from datetime import datetime
from pathlib import Path

def listDifference(listA,listB):
    if len(listA)==len(listB):
        dist=(sum(listA)-sum(listB))/len(listA)
        norm=0
        for ii in range(len(listA)):
            norm=norm+abs(listA[ii]-dist-listB[ii])
    return norm


def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime('%d %b %Y')
    return formated_date

def get_files(file_dir):
    dir_entries = os.scandir(file_dir)
    for entry in dir_entries:
        if not (entry.name.startswith('.') or entry.name.startswith('~')):
            info = entry.stat()
            size=os.path.getsize(entry)
            str_size=str(size)+"B" if size<1024 else str(int(size/1024))+"K" if size<2014*1024 else str(int(size/(1024*1024)))+"M"
            type="-f" if entry.is_file() else "-d"
            print(f'{type}\t {str_size} \t {convert_date(info.st_mtime)}\t {entry.name}')

class local_file:
    desktop="/Users/shuailongli/Desktop"
    document="/Users/shuailongli/Documents"
    Dropbox="/Users/shuailongli/Dropbox"
    research="/Users/shuailongli/Dropbox/Desktop/ExoticHiggsDecay/ChargedExoticDecay/MyAnalysis"
    KeyWordPrim=["file","open","remove","delete","move","rename","go"]
    KeyWordPrim.append(["path","list","desktop","dropbox","directory"])
    KeyWordSec=["research","back","current","set"]
    file_format=["txt","html","cpp","sh","mp3","pdf","png","h","py"]
    file_order=["first","second","third","fourth","last"]
    file_order_num=["1st","2nd","3rd","4th","last"]
    execute=False
    
    def __init__(self):
        self.previous_dir=self.desktop
        self.working_dir=self.desktop
        self.path=self.desktop
        fread=open("temp/file_info.txt",'r')
        readlines=fread.read().split('\n')
        for line in readlines:
            words=list(line.split(" "))
            if words[0]=="previous_dir":
                self.previous_dir=words[1]
            if words[0]=="working_dir":
                self.working_dir=words[1]
            if words[0]=="path":
                self.path=words[1]
        fread.close()
        self.execute=False
        self.listfunc=[self.GoTo,self.Open,self.GoOut,self.GoBack,self.SetPath,self.DisplayPath]
        self.optimized_func=self.listfunc[0]
        
    def action(self,mywords,exe):
        self.score=0
        self.mywords=[word.lower() for word in mywords]  #convert to lower case
        #print(self.mywords)
        self.execute=exe
        for word in mywords:
            if word in self.KeyWordPrim: self.score+=1
            if word in self.KeyWordSec: self.score+=0.5
        if not self.execute:
            subscore=0
            for func in self.listfunc:
                ind_score=func(mywords)
                #print(func.__name__,"\t",ind_score)
                if subscore<ind_score:
                    subscore=ind_score
                    self.optimized_func=func
            self.score+=subscore
        else:
            self.optimized_func(self.mywords)
            fwrite=open("temp/file_info.txt",'w')
            fwrite.write("previous_dir "+self.previous_dir+"\n")
            fwrite.write("working_dir "+self.working_dir+"\n")
            fwrite.write("path "+self.path+"\n")
            fwrite.close()
        return self.score
        
    def GoTo(self,mywords):
        subscore=0
        subsubscore=0
        if all(word in mywords for word in ["go", "to"]) or "enter" in mywords:
            if ("to" in mywords and (len(mywords)-1)>mywords.index("to")) or ("enter" in mywords and (len(mywords)-1)>mywords.index("enter")):
                subscore=2
                if "directory" in mywords: mywords=mywords[:mywords.index("directory")]
                if all(word in mywords for word in ["go", "to"]):
                    subsubscore,filename=self.match_file(mywords[mywords.index("to")+1:])
                else: subsubscore,filename=self.match_file(mywords[mywords.index("enter")+1:])
                filename=[file for file in filename if os.path.isdir(file)]
                if self.execute:
                    if subsubscore==0 or len(filename)==0: print("cannot find the direcotry")
                    elif len(filename)==1:
                        get_files(filename[0])
                        self.previous_dir=self.working_dir
                        self.working_dir=filename[0]
                    else:
                        print("These directoris match your requirement: ")
                        for dir_entry in filename: print(dir_entry)
        return subscore+subsubscore

    def SetPath(self,mywords):
        subscore=0
        subsubscore=0
        filename=[]
        if all(word in mywords for word in ["set", "path"]):
            subscore+=2
            if "to" in mywords and mywords.index("to")==(mywords.index("path")+1):
                mywords=mywords[mywords.index("to")+1:]
                subscore+=0.5
                if "directory" in mywords: mywords=mywords[:mywords.index("directory")]
                subsubscore,filename=self.match_file(mywords)
                filename=[file for file in filename if os.path.isdir(file)]
            if self.execute:
                if subsubscore==0 or len(filename)==0: self.path=self.working_dir
                elif len(filename)==1:
                    self.path=filename[0]
                else:
                    print("These directoris match your requirement: ")
                    for dir_entry in filename: print(dir_entry)
                print("path= ",self.path)
        return subscore+subsubscore

    def DisplayPath(self,mywords):
        subscore=0
        subsubscore=0
        filename=" "
        if all(word in mywords for word in ["display", "path"]) and mywords.index("path")>mywords.index("display"):
            subscore+=2
            filename="path= "+self.path
            if "working" in mywords:
                filename="working directory= "+self.working_dir
                subsubscore=0.5
            if "previous" in mywords:
                filename="previous directory= "+self.previous_dir
                subsubscore=0.5
            if self.execute: print(filename)
        return subscore+subsubscore

    def Open(self,mywords):
        subscore=0
        subsubscore=0
        if "open" in mywords:
            subscore=2
            sub_mywords=mywords[mywords.index("open")+1:]
            if "directory" in sub_mywords:
                subsubscore,filename=self.match_file(sub_mywords[:sub_mywords.index("directory")])
                filename=[file for file in filename if os.path.isdir(file)]
                if self.execute:
                    if subsubscore==0 or len(filename)==0: print("cannot find the direcotry")
                    elif len(filename)==1:
                        command="open "+filename[0]
                        os.system(command)
                        self.previous_dir=self.working_dir
                        self.working_dir=filename[0]
                    else:
                        print("These directoris match your requirement: ")
                        for dir_entry in filename: print(dir_entry)
                return subscore+subsubscore
            if "file" in sub_mywords:
                subsubscore,filename=self.match_file(sub_mywords[:sub_mywords.index("file")])
                filename=[file for file in filename if os.path.isfile(file)]
                if self.execute:
                    if subsubscore==0 or len(filename)==0: print("cannot find the file")
                    elif len(filename)==1:
                        if "with" in sub_mywords:
                            if sub_mywords[sub_mywords.index("with")+1:] =="vim": command="vim "+filename[0]
                            else: command="open -a \""+sub_mywords[sub_mywords.index("with")+1:][0]+"\" "+filename[0]
                        else: command="open "+filename[0]
                        os.system(command)
                    else:
                        print("These files match your requirement: ")
                        for dir_entry in filename: print(dir_entry)
                return subscore+subsubscore
            else:
                if "with" in sub_mywords:
                    subsubscore,filename=self.match_file(sub_mywords[:sub_mywords.index("with")])
                    filename=[file for file in filename if os.path.isfile(file)]
                    if self.execute:
                        if subsubscore==0 or len(filename)==0: print("cannot find the file")
                        elif len(filename)==1:
                            if sub_mywords[sub_mywords.index("with")+1:] =="vim": command="vim "+filename[0]
                            else: command="open -a \""+sub_mywords[sub_mywords.index("with")+1:][0]+"\" "+filename[0]
                            os.system(command)
                        else:
                            print("These files match your requirement: ")
                            for dir_entry in filename: print(dir_entry)
                    return subscore+subsubscore
                else:
                    subsubscore,filename=self.match_file(sub_mywords)
                    if self.execute:
                        if subsubscore==0 or len(filename)==0: print("cannot find the file")
                        elif len(filename)==1:
                            command="open "+filename[0]
                            os.system(command)
                            if os.path.isdir(filename[0]):
                                self.previous_dir=self.working_dir
                                self.working_dir=filename[0]
                        else:
                            print("These files match your requirement: ")
                            for dir_entry in filename: print(dir_entry)
                    return subscore+subsubscore
        else: return subscore+subsubscore

    def GoOut(self,mywords):
        subscore=0
        if "go" in mywords and "out" in mywords and mywords.index("out")==(mywords.index("go")+1):
            subscore+=3
            if self.execute:
                self.previous_dir=self.working_dir
                self.working_dir=str(Path(self.working_dir).parent)
                get_files(self.working_dir)
        return subscore

    def GoBack(self,mywords):
        subscore=0
        if "go" in mywords and "back" in mywords and mywords.index("back")==(mywords.index("go")+1):
            subscore+=3
            if self.execute:
                tem_filename=self.previous_dir
                self.previous_dir=self.working_dir
                self.working_dir=tem_filename
                get_files(self.working_dir)
        return subscore




    def match_file(self,mywords):
        subscore=0
        filename=[]
        if "desktop" in mywords:
            subscore=2
            filename.append(self.desktop)
            return [subscore,filename]
        if "path" in mywords:
            subscore=2
            filename.append(self.path)
            return [subscore,filename]
        if "research" in mywords:
            subscore=2
            filename.append(self.research)
            return [subscore,filename]
        if "document" in mywords:
            subscore=2
            filename.append(self.document)
            return [subscore,filename]
        if "dropbox" in mywords:
            subscore=2
            filename.append(self.Dropbox)
            return [subscore,filename]
        if all(word in mywords for word in ["previous"]):
            subscore=2
            filename.append(self.previous_dir)
            return [subscore,filename]
        if all(word in mywords for word in ["working"]):
            subscore=2
            filename.append(self.working_dir)
            return [subscore,filename]

        sub_mywords=[word.lower() for word in mywords]  #convert to small leters
        dir_entries=[entry for entry in os.listdir(self.working_dir) if not (entry.startswith('.') or entry.startswith('~'))]
        if "file" in mywords:
            subscore+=1
            sub_mywords=mywords[:mywords.index("file")]
        if "all" in sub_mywords: sub_mywords.remove("all")
        if "the" in sub_mywords: sub_mywords.remove("the")
        for word in self.file_order:
            if word in sub_mywords:
                subscore+=0.5
                if self.file_order.index(word) != (len(self.file_order)-1):
                    filename.append(self.working_dir+"/"+dir_entries[self.file_order.index(word)])
                else:
                    filename.append(self.working_dir+"/"+dir_entries[len(dir_entries)-1])
                return [subscore,filename]
        for word in self.file_order_num:
            if word in sub_mywords:
                subscore+=0.5
                if self.file_order_num.index(word) != (len(self.file_order_num)-1):
                    filename.append(self.working_dir+"/"+dir_entries[self.file_order_num.index(word)])
                else:
                    filename.append(self.working_dir+"/"+dir_entries[len(dir_entries)-1])
                return [subscore,filename]
        for word in sub_mywords:
            if word in self.file_format:
                subscore+=1
                sub_mywords.remove(word)
                dir_entries=[entry for entry in dir_entries if fnmatch.fnmatch(entry.lower(),"*"+word+"*")]
            dir_entries=[entry for entry in dir_entries if fnmatch.fnmatch(entry.lower(),"*"+word+"*")]
        filename=[self.working_dir+"/"+entry for entry in dir_entries]
        subscore+=0.5*len(dir_entries)
        return [subscore,filename]



#########################################
