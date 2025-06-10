################################################################################################################################
#Home
################################################################################################################################
#Default Libraries
import inspect

#Program
from .Home.N_Project import Project
from .Home.N_Panel import Panel

class Home:
    def __init__(self, Global, Main):
        try:
            self.Global = Global
            self.Main = Main
            self.Widget = []
            
            #Frame
            Fixture = self.Main.Frame.Locate(100, 100, 0, 0)
            self.Frame = self.Global['Gluonix'].Frame(self.Main.Frame)
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Border_Size=0, Display=True) 
            self.Frame.Config(Resize=True, Move=True)
            self.Frame.Create()
            self.Main.Widget.append(self.Frame)
            
            #Project View
            self.Project = Project(self.Global, self)
            
            #Panel View
            self.Panel = Panel(self.Global, self)
                    
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))