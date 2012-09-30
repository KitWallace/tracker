from persistant import *

class Control(Persistant) :
    def __init__(self,name,initial=0,step=1,min=0, max=100000) :
      self.name = name
      self.initial = initial
      self.step = step
      self.min = min
      self.max = max
      self.on = True
      self.val = self.initial
      self.put()

    def toggle(self) :
      self.on = not self.on
      self.put()
      return self

    def increment(self,m=0) :
      if m==0 :
         m = self.step
      self.val= min((self.max,self.val + m))
      self.put()
      return self

    def decrement(self,m=0) :
      if m==0 :
         m = self.step
      self.val = max((self.min, self.val - m))
      self.put()
      return self
   
    @property
    def value(self) :
      return self.val

    @property
    def status(self) :
        if self.on :
            return "on"
        else : 
            return "off"
        

