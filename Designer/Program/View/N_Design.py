################################################################################################################################
#Design
################################################################################################################################
#Default Libraries
import inspect

#Program
from .Design.N_Stock import Stock
from .Design.N_Element import Element
from .Design.N_Configure import Configure

class Design:
    def __init__(self, Global, Main):
        try:
            self.Global = Global
            self.Main = Main
            self.Widget = []
            self.Database = False
            self.Project_Path = False
            self.Project_Data = False
            self.Display_ID = False
            self.Alignment = 'Pixel'
            
            #Frame
            Fixture = self.Main.Frame.Locate(100, 100, 0, 0)
            self.Frame = self.Global['Gluonix'].Frame(self.Main.Frame)
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Border_Size=0, Display=False)
            self.Frame.Config(Resize=False, Move=False)
            self.Frame.Create()
            self.Main.Widget.append(self.Frame)
            
            #Label
            Fixture = self.Frame.Locate(39, 10, 1, 0)
            self.Label = self.Global['Gluonix'].Label(self.Frame)
            self.Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Label.Config(Border_Size=0, Display=True)
            self.Label.Config(Foreground='black', Font_Size=16, Font_Weight='normal', Align='w')
            self.Label.Config(Resize=True, Move=True)
            self.Label.Create()
            
                #Close
            Fixture = self.Frame.Locate(12, 6, 86, 2)
            self.Close = self.Global['Gluonix'].Label(self.Frame)
            self.Close.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Close.Config(Background='#e1e1e1', Foreground='black', Value='Close', Font_Size=9, Font_Weight='normal', Border_Size=1, Border_Color='#adadad')
            self.Close.Bind(On_Hover_In=lambda E: self.Close.Config(Border_Color='#0078d7', Background='#d5dcf0'))
            self.Close.Bind(On_Hover_Out=lambda E: self.Close.Config(Border_Color='#adadad', Background='#e1e1e1'))
            self.Close.Bind(On_Click=lambda E: self.Close_Project())
            self.Close.Create()
            
            #Widget View
            self.Stock = Stock(self.Global, self)
            
            #Display View
            self.Element = Element(self.Global, self)
            
            #Configure View
            self.Configure = Configure(self.Global, self)
                    
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        
    def Update(self, Loading=True):
        try:
            if Loading:
                self.Global['Loading'].Show()
                self.Global['GUI'].After(500, lambda:self.Update(Loading=False))
            else:
                if self.Display_ID and self.Project_Data:
                    if self.Database:
                        self.Database.Close()
                    self.Database = self.Global['Gluonix'].SQL(f'{self.Project_Path}/Data/NGD.dll')
                    Display_Data_Temp = self.Database.Get(f"SELECT * FROM `Display` WHERE `ID`='{self.Display_ID}'", Keys=True)
                    self.Display_Data = Display_Data_Temp[0]
                    self.Label.Set(self.Display_Data['Title'])
                    self.Alignment = self.Display_Data['Alignment']
                    setattr(self, self.Display_ID, self.Global['Gluonix'].Popup(self.Global['GUI']))
                    Temp_Root = getattr(self, self.Display_ID)
                    Temp_Root.Config(Width=int(self.Display_Data['Width']), Height=int(self.Display_Data['Height']), Left=int(self.Display_Data['Left']), Top=int(self.Display_Data['Top']))
                    Temp_Root.Config(Title=self.Display_Data['Title'], Background=self.Display_Data['Background'], Icon=f"{self.Project_Path}/Data/File/{self.Project_Data['Icon']}", Resizable=bool(int(self.Display_Data['Resizable'])))
                    Temp_Root.Config(Persistent=True, Full_Screen=bool(int(self.Display_Data['Full_Screen'])), Minimize=True, Toolbar=bool(int(self.Display_Data['Toolbar'])), Alignment=self.Display_Data['Alignment'], Menu_Enable=bool(int(self.Display_Data['Menu'])))
                    Temp_Root.Create()
                    if bool(int(self.Display_Data['Menu'])):
                        Temp_Root.Add_Menu(Name='File')
                        Temp_Root.Add_Menu(Name='Help')
                    self.Element.Default(Parent=self.Display_ID)
                    self.Configure.Hide_All()
                    self.Frame.Show()
                    Temp_Root.Show()
                self.Global['Loading'].Hide()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Close_Project(self):
        try:
            Temp_Root = getattr(self, self.Display_ID)
            Temp_Root.Close()
            if self.Database:
                self.Database.Close()
            self.Database = False
            self.Frame.Hide()
            self.Main.Home.Frame.Show()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))