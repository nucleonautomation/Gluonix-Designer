################################################################################################################################
#Menu
################################################################################################################################
import inspect

#Program
from .N_Panel_Overview import Overview

class Panel:
    def __init__(self, Global, Home):
        try:
            self.Global = Global
            self.Home = Home
            self.Widget = []
            
            Fixture = self.Home.Frame.Locate(80, 100, 20, 0)
            self.Frame = self.Global['Gluonix'].Scroll(self.Home.Frame)
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Border_Size=0, Display=True)
            self.Frame.Config(Resize=True, Move=True)
            self.Frame.Create()
            
            #Overview
            self.Overview = Overview(self.Global, self)

        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))