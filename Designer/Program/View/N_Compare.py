################################################################################################################################
#Design
################################################################################################################################
#Default Libraries
import inspect
import os
import shutil
import random
import string
import time
import traceback

#Program
from .Compare.N_Element import Element

class Compare:
    def __init__(self, Global, Main):
        try:
            self.Global = Global
            self.Main = Main
            self.Widget = []
            self.Database_1 = False
            self.Database_2 = False
            self.Project_1 = False
            self.Project_2 = False
            self.Project_1_Path = False
            self.Project_2_Path = False
            self.From = False
            self.To = False
            
            #Frame
            Fixture = self.Main.Frame.Locate(100, 100, 0, 0)
            self.Frame = self.Global['Gluonix'].Frame(self.Main.Frame)
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Border_Size=0, Display=False)
            self.Frame.Config(Resize=True, Move=True)
            self.Frame.Create()
            self.Main.Widget.append(self.Frame)
            
            #Label 1
            Fixture = self.Frame.Locate(40, 10, 0, 0)
            self.Label_1 = self.Global['Gluonix'].Label(self.Frame)
            self.Label_1.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Label_1.Config(Border_Size=0, Display=True)
            self.Label_1.Config(Foreground='black', Font_Size=16, Font_Weight='bold', Align='center')
            self.Label_1.Config(Resize=True, Move=True)
            self.Label_1.Create()
            
            #Display 2 Select
            Fixture = self.Frame.Locate(8, 4, 16, 7)
            self.Display_1_Select = self.Global['Gluonix'].Select(self.Frame)
            self.Display_1_Select.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Display_1_Select.Config(Foreground='black', Font_Size=11, Font_Weight='normal', Align='center', Border_Size=1)
            self.Display_1_Select.Bind(On_Change=lambda E: self.Update(Partial=True))
            self.Display_1_Select.Create()
            
            #Label 2
            Fixture = self.Frame.Locate(40, 10, 60, 0)
            self.Label_2 = self.Global['Gluonix'].Label(self.Frame)
            self.Label_2.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Label_2.Config(Border_Size=0, Display=True)
            self.Label_2.Config(Foreground='black', Font_Size=16, Font_Weight='bold', Align='center')
            self.Label_2.Config(Resize=True, Move=True)
            self.Label_2.Create()
            
            #Display 2 Select
            Fixture = self.Frame.Locate(8, 4, 76, 7)
            self.Display_2_Select = self.Global['Gluonix'].Select(self.Frame)
            self.Display_2_Select.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Display_2_Select.Config(Foreground='black', Font_Size=11, Font_Weight='normal', Align='center', Border_Size=1)
            self.Display_2_Select.Bind(On_Change=lambda E: self.Update(Partial=True))
            self.Display_2_Select.Create()
            
            #Copy 1->2
            Fixture = self.Frame.Locate(12, 6, 44, 30)
            self.Copy12 = self.Global['Gluonix'].Compound(self.Frame)
            self.Copy12.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Copy12.Config(Background='#e1e1e1', Foreground='black', Value='COPY       ', Font_Size=10, Font_Weight='bold', Border_Size=1, Border_Color='#adadad')
            self.Copy12.Config(Compound='right', Path=self.Global['Image']('Arrow_Right'))
            self.Copy12.Bind(On_Hover_In=lambda E: self.Copy12.Config(Border_Color='#0078d7', Background='#d5dcf0'))
            self.Copy12.Bind(On_Hover_Out=lambda E: self.Copy12.Config(Border_Color='#adadad', Background='#e1e1e1'))
            self.Copy12.Bind(On_Click=lambda E: self.Copy_From_1_To_2())
            self.Copy12.Create()
            
            #Copy 1->2
            Fixture = self.Frame.Locate(12, 6, 44, 45)
            self.Copy21 = self.Global['Gluonix'].Compound(self.Frame)
            self.Copy21.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Copy21.Config(Background='#e1e1e1', Foreground='black', Value='       COPY', Font_Size=10, Font_Weight='bold', Border_Size=1, Border_Color='#adadad')
            self.Copy21.Config(Compound='left', Path=self.Global['Image']('Arrow_Left'))
            self.Copy21.Bind(On_Hover_In=lambda E: self.Copy21.Config(Border_Color='#0078d7', Background='#d5dcf0'))
            self.Copy21.Bind(On_Hover_Out=lambda E: self.Copy21.Config(Border_Color='#adadad', Background='#e1e1e1'))
            self.Copy21.Bind(On_Click=lambda E: self.Copy_From_2_To_1())
            self.Copy21.Create()
            
                #Close
            Fixture = self.Frame.Locate(12, 6, 44, 2)
            self.Close = self.Global['Gluonix'].Label(self.Frame)
            self.Close.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Close.Config(Background='#e1e1e1', Foreground='black', Value='Close', Font_Size=9, Font_Weight='normal', Border_Size=1, Border_Color='#adadad')
            self.Close.Bind(On_Hover_In=lambda E: self.Close.Config(Border_Color='#0078d7', Background='#d5dcf0'))
            self.Close.Bind(On_Hover_Out=lambda E: self.Close.Config(Border_Color='#adadad', Background='#e1e1e1'))
            self.Close.Bind(On_Click=lambda E: self.Close_Compare())
            self.Close.Create()
            
            #Display View
            self.Element_1 = Element(self.Global, self)
            self.Element_2 = Element(self.Global, self)
            Fixture = self.Frame.Locate(0, 0, 60, 0)
            self.Element_2.Frame.Config(Left=Fixture[2])
                    
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
    
    def Copy_From_1_To_2(self):
        try:
            self.Global['Message'].Hide()
            From = self.Element_1.Tree.Current()
            if From:
                Element_ID = self.Element_1.Tree.Get(From)
                if Element_ID[0]!=self.Element_1.Parent:
                    self.From = [Element_ID, 1, From]
                    To = self.Element_2.Tree.Current()
                    if To:
                        Element_ID = self.Element_2.Tree.Get(To)
                        if Element_ID[0]!=self.Element_2.Parent:
                            self.To = [Element_ID, 2, To]
                            self.Copy()
                            return
                    self.Global['Message'].Show('Error', f'Location Not Selected In {self.Project_2}')
                    return
            self.Global['Message'].Show('Error', f'Item Not Selected In {self.Project_1}')
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
    
    def Copy_From_2_To_1(self):
        try:
            self.Global['Message'].Hide()
            From = self.Element_2.Tree.Current()
            if From:
                Element_ID = self.Element_2.Tree.Get(From)
                if Element_ID[0]!=self.Element_2.Parent:
                    self.From = [Element_ID, 2, From]
                    To = self.Element_1.Tree.Current()
                    if To:
                        Element_ID = self.Element_1.Tree.Get(To)
                        if Element_ID[0]!=self.Element_1.Parent:
                            self.To = [Element_ID, 1, To]
                            self.Copy()
                            return
                    self.Global['Message'].Show('Error', f'Location Not Selected In {self.Project_1}')
                    return
            self.Global['Message'].Show('Error', f'Item Not Selected In {self.Project_2}')
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        
    def Copy(self):
        try:
            Paste_Type = self.To[0][1]
            if Paste_Type=='Frame' or Paste_Type=='Canvas' or Paste_Type=='Scroll':
                self.Paste(self.From[2], self.To[2])
            else:
                self.Global['Message'].Show('Error', 'Copy To Selected Widget Not Posiible')
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Paste(self, ID=False, Root=False):
        try:
            if ID and Root:
                From = getattr(self, f"Element_{self.From[1]}")
                To = getattr(self, f"Element_{self.To[1]}")
                Root_ID = To.Tree.Get(Root)[0]
                Element_ID = From.Tree.Get(ID)[0]
                if len(From.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Element_ID}'", Keys=True))>0:
                    Type = 'Frame'
                elif len(From.Database.Get(f"SELECT * FROM `Item` WHERE `ID`='{Element_ID}'", Keys=True))>0:
                    Type = 'Item'
                else:
                    Type = 'Widget'
                From.Database.Post(f"DELETE FROM `{Type}_Copy`")
                From.Database.Post(f"INSERT INTO `{Type}_Copy` SELECT * FROM `{Type}` WHERE `ID`='{Element_ID}'")
                Frame_Data = From.Database.Get(f"SELECT * FROM `{Type}_Copy` WHERE `ID`='{Element_ID}'", Keys=True)[0]
                Number = 0
                Exist = From.Database.Get(f"SELECT * FROM `{Type}` WHERE (`Name`='{Frame_Data['Name']}' AND `Root`='{Root_ID}')")
                while len(Exist)>0:
                    Number += 1
                    Exist = From.Database.Get(f"SELECT * FROM `{Type}` WHERE (`Name`='{Frame_Data['Name']}{Number}' AND `Root`='{Root_ID}')")
                if Number>0:
                    Name = f"{Frame_Data['Name']}{Number}"
                else:
                    Name = Frame_Data['Name']
                Random_Letter = ''.join(random.choices(string.ascii_letters, k=10))
                New_ID = Random_Letter+self.Global['Custom'].MD5(Root_ID+Name+str(time.time()*1000000))
                From.Database.Post(f"UPDATE `{Type}_Copy` SET `ID`='{New_ID}',`Name`='{Name}',`Root`='{Root_ID}' WHERE `ID`='{Element_ID}'")
                Data = From.Database.Get(f"SELECT * FROM `{Type}_Copy` WHERE `ID`='{New_ID}'", Keys=True)[0]
                Columns = ','.join(f'`{K}`' for K in Data.keys())
                Values = ','.join(self.Format(V) for V in Data.values())
                To.Database.Post(f"INSERT INTO `{Type}` ({Columns}) VALUES ({Values})")
                From.Database.Post(f"DELETE FROM `{Type}_Copy` WHERE `ID`='{New_ID}'")
                if os.path.exists(f"{From.Project_Path}/Data/File/{Element_ID}"):
                    shutil.copy(f"{From.Project_Path}/Data/File/{Element_ID}", f"{To.Project_Path}/Data/File/{New_ID}")
                if Type=='Frame':
                    Root_Level = To.Tree.Get(Root)[2]
                    To.Database.Post(f"UPDATE `{Type}` SET `Level`='{Root_Level+1}' WHERE `ID`='{New_ID}'")
                Widget = To.Database.Get(f"SELECT * FROM `{Type}` WHERE `ID`='{New_ID}'", Keys=True)[0]
                Level = 0
                if Type=='Frame':
                    Level = Widget['Level']
                Image = self.Global['Image'](Widget['Type'])
                Temp_ID = To.Tree.Add(Name=Widget['Name'], Parent=Root, Value=[Widget['ID'], Widget['Type'], Level], Path=Image)
                for Each in From.Tree.Child(ID):
                    self.Paste(Each, Temp_ID)
        except Exception as E:
            traceback.print_exc()
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        
    def Update(self, Loading=True, Partial=False):
        try:
            if Loading:
                self.Global['Loading'].Show()
                self.Global['GUI'].After(500, lambda:self.Update(Loading=False, Partial=Partial))
            else:
                if not Partial:
                    if self.Database_1:
                        self.Database_1.Close()
                    if self.Database_2:
                        self.Database_2.Close()
                    self.Database_1 = self.Global['Gluonix'].SQL(f'{self.Project_1_Path}/Data/NGD.dll')
                    self.Element_1.Database = self.Database_1
                    self.Element_1.Project_Path = self.Project_1_Path
                    Display_Data = self.Database_1.Get(f"SELECT * FROM `Display`", Keys=True)
                    self.Display_1_Select.Clear()
                    for Display in Display_Data:
                        self.Display_1_Select.Add(Display['ID'])
                        if Display['ID']=='Root':
                            self.Label_1.Set(Display['Title'])
                            self.Project_1 = Display['Title']
                            self.Display_1_Select.Set(Display['ID'])
                    self.Database_2 = self.Global['Gluonix'].SQL(f'{self.Project_2_Path}/Data/NGD.dll')
                    self.Element_2.Database = self.Database_2
                    self.Element_2.Project_Path = self.Project_2_Path
                    Display_Data = self.Database_2.Get(f"SELECT * FROM `Display`", Keys=True)
                    self.Display_2_Select.Clear()
                    for Display in Display_Data:
                        self.Display_2_Select.Add(Display['ID'])
                        if Display['ID']=='Root':
                            self.Label_2.Set(Display['Title'])
                            self.Project_2 = Display['Title']
                            self.Display_2_Select.Set(Display['ID'])
                self.Element_1.Default(self.Display_1_Select.Get())
                self.Element_2.Default(self.Display_2_Select.Get())
                self.Frame.Show()
                self.Global['Loading'].Hide()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Close_Compare(self):
        try:
            if self.Database_1:
                self.Database_1.Close()
            self.Database_1 = False
            if self.Database_2:
                self.Database_2.Close()
            self.Database_2 = False
            self.Element_2.Database = False
            self.Project_1_Path = False
            self.Project_2_Path = False
            self.Element_1.Project_Path = False
            self.Element_2.Project_Path = False
            self.Frame.Hide()
            self.Main.Home.Frame.Show()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Format(self, Value):
        try:
            if isinstance(Value, str):
                return "'" + Value.replace("'", "''") + "'"
            elif Value is None:
                return 'NULL'
            else:
                return str(Value)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))