################################################################################################################################
#Message
################################################################################################################################
import time
import inspect

class Message:
    def __init__(self, Global):
        try:
            self.Global = Global
            self.List = []
            #Frame 
            Fixture = self.Global['GUI'].Locate(25, 15, 73.5, 82.5)
            self.Frame = self.Global['Gluonix'].Frame(self.Global['GUI'])
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Border_Size=1, Display=False)
            self.Frame.Create()
            self.Global['Widget'].append(self.Frame)
                #Top Bar
            Fixture = self.Frame.Locate(100, 20, 0, 0)
            self.Top_Bar = self.Global['Gluonix'].Label(self.Frame)
            self.Top_Bar.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Top_Bar.Config(Background='#5a1b1b', Border_Size=0)
            self.Top_Bar.Create()
                #Close Image
            Fixture = self.Frame.Locate(5, 10, 94, 4)
            self.Close = self.Global['Gluonix'].Image(self.Frame)
            self.Close.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Close.Config(Background='#5a1b1b', Path=self.Global['Image']('Cross_White'), Border_Size=0)
            self.Close.Config(Foreground='#FFFFFF', Hover_Foreground='#F36D6D', Use_Foreground=True)
            self.Close.Bind(On_Click=lambda E: self.Hide())
            self.Close.Create()
                #Status Image
            Fixture = self.Frame.Locate(20, 77, 4, 21)
            self.Image = self.Global['Gluonix'].Image(self.Frame)
            self.Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Image.Config(Path=self.Global['Image']('Success'), Border_Size=0)
            self.Image.Create()
                #Message Label
            Fixture = self.Frame.Locate(73, 77, 25, 21)
            self.Label = self.Global['Gluonix'].Label(self.Frame)
            self.Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Label.Config(Foreground='black', Value="Message", Font_Size=9, Font_Weight='normal', Align='center', Border_Size=0)
            self.Label.Create()
            
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))

    def Show(self, Type='Success', Text=''):
        try:
            self.Label.Config(Value=Text)
            self.Image.Config(Path=self.Global['Image'](Type.capitalize()))
            self.Frame.Show()
            if Type.lower()=='warning' or Type.lower()=='error':
                Time = int(time.time())
                self.List.append([Type, Text, Time])
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        
    def Hide(self, Delay=False):
        try:
            if Delay:
                self.Global['GUI'].After(Delay*1000, lambda: self.Hide(Delay=False))
            else:
                self.Frame.Hide()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Clear(self):
        try:
            self.List = []
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))