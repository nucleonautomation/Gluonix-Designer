################################################################################################################################
#Main
################################################################################################################################
import inspect

#Program
from .N_Home import Home
from .N_Design import Design
from .N_Compare import Compare

class Main:
    def __init__(self, Global):
        try:
            self.Global = Global
            self.Widget = []
            #Frame
            Fixture = self.Global['GUI'].Locate(100, 100, 0, 0)
            self.Frame = self.Global['Gluonix'].Scroll(self.Global['GUI'])
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Border_Size=0, Scrollbar=20)
            self.Frame.Config(Resize=True, Move=True)
            self.Frame.Create()
            self.Frame.Hide()
            
            #Home Page
            self.Home = Home(self.Global, self)
            
            #Design Page
            self.Design = Design(self.Global, self)
            
            #Compare Page
            self.Compare = Compare(self.Global, self)
            
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))