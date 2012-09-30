import pickle
import time

def get(name) :   
      tries = 2
      while tries > 0 :
        try :
           file = open("obj/"+name+".pkl","rb")
           return pickle.load(file)
        except EOFError :
           time.sleep(0.02)
           tries-= 1

class Persistant(object) :
   
    def __init__(self,name) :
        self.set(name)
    
    def set(self,name) :
        self.name = name
        self.ts = time.time()
    
    def put(self) :
        file = open("obj/"+self.name+".pkl","wb")
        self.ts = time.time()
        pickle.dump(self,file)
        return self

