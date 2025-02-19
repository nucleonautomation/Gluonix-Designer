################################################################################################################################
#Menu
################################################################################################################################
import os
import inspect
import shutil
import time

class New:
    def __init__(self, Global, Project):
        try:
            self.Global = Global
            self.Project = Project
            self.Widget = []
            self.Error = False
            
            Fixture = self.Global['GUI'].Locate(60, 50, 25, 25)
            self.Frame = self.Global['Gluonix'].Frame(self.Global['GUI'])
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Background='white', Border_Size=1, Display=False)
            self.Frame.Create()
            self.Project.Widget.append(self.Frame)
            
                #Info Label
            Fixture = self.Frame.Locate(70, 6, 3, 8)
            self.Info_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Info_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Info_Label.Config(Foreground='black', Font_Size=9, Font_Weight='normal', Align='w', Border_Size=0)
            self.Info_Label.Config(Value="Enter the name and location for the new project")
            self.Info_Label.Create()
            
                #Name Label
            Fixture = self.Frame.Locate(10, 6, 3, 16)
            self.Name_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Name_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Name_Label.Config(Foreground='black', Value="Name:", Font_Size=9, Font_Weight='normal', Align='w', Border_Size=0)
            self.Name_Label.Create()
            
                #Name Entry
            Fixture = self.Frame.Locate(70, 6, 13, 16)
            self.Name_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Name_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Name_Entry.Config(Background='white', Foreground='black', Font_Size=10, Font_Weight='normal', Align='left', Border_Size=1)
            self.Name_Entry.Bind(On_Key_Release=lambda E: self.Update_Path())
            self.Name_Entry.Create()
            
                #Location Label
            Fixture = self.Frame.Locate(10, 6, 3, 24)
            self.Name_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Name_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Name_Label.Config(Foreground='black', Value="Location:", Font_Size=9, Font_Weight='normal', Align='w', Border_Size=0)
            self.Name_Label.Create()
            
                #Location Entry
            Fixture = self.Frame.Locate(70, 6, 13, 24)
            self.Location_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Location_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Location_Entry.Config(Background='white', Foreground='black', Font_Size=10, Font_Weight='normal', Align='left', Border_Size=1)
            self.Location_Entry.Bind(On_Key_Release=lambda E: self.Update_Path())
            self.Location_Entry.Create()
            
                #Location Browser
            Fixture = self.Frame.Locate(12, 6, 85, 24)
            self.Location_Browser = self.Global['Gluonix'].Label(self.Frame)
            self.Location_Browser.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Location_Browser.Config(Background='#e1e1e1', Foreground='black', Value='Browser...', Font_Size=9, Font_Weight='normal', Border_Size=1, Border_Color='#adadad')
            self.Location_Browser.Bind(On_Hover_In=lambda E: self.Location_Browser.Config(Border_Color='#0078d7', Background='#d5dcf0'))
            self.Location_Browser.Bind(On_Hover_Out=lambda E: self.Location_Browser.Config(Border_Color='#adadad', Background='#e1e1e1'))
            self.Location_Browser.Bind(On_Click=lambda E: self.Project_Folder())
            self.Location_Browser.Create()
            
                #Project Path Label
            Fixture = self.Frame.Locate(50, 4, 13, 34)
            self.Project_Path_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Project_Path_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Project_Path_Label.Config(Foreground='black', Font_Size=9, Font_Weight='normal', Align='w', Border_Size=0)
            self.Project_Path_Label.Config(Value="The project will be created in")
            self.Project_Path_Label.Create()
            self.Location_Browser.Create()
            
                #Project Path
            Fixture = self.Frame.Locate(70, 15, 13, 38.5)
            self.Project_Path = self.Global['Gluonix'].Label(self.Frame)
            self.Project_Path.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Project_Path.Config(Foreground='black', Font_Size=9, Font_Weight='normal', Align='nw', Border_Size=0)
            self.Project_Path.Create()
            
                #Ok Button
            Fixture = self.Frame.Locate(12, 6, 70, 88)
            self.Ok_Button = self.Global['Gluonix'].Label(self.Frame)
            self.Ok_Button.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Ok_Button.Config(Background='#e1e1e1', Foreground='black', Value='OK', Font_Size=9, Font_Weight='normal', Border_Size=1, Border_Color='#adadad')
            self.Ok_Button.Bind(On_Hover_In=lambda E: self.Ok_Button.Config(Border_Color='#0078d7', Background='#d5dcf0'))
            self.Ok_Button.Bind(On_Hover_Out=lambda E: self.Ok_Button.Config(Border_Color='#adadad', Background='#e1e1e1'))
            self.Ok_Button.Bind(On_Click=lambda E: self.Create())
            self.Ok_Button.Create()
            
                #Cancel Button
            Fixture = self.Frame.Locate(12, 6, 85, 88)
            self.Cancel_Button = self.Global['Gluonix'].Label(self.Frame)
            self.Cancel_Button.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Cancel_Button.Config(Background='#e1e1e1', Foreground='black', Value='Cancel', Font_Size=9, Font_Weight='normal', Border_Size=1, Border_Color='#adadad')
            self.Cancel_Button.Bind(On_Hover_In=lambda E: self.Cancel_Button.Config(Border_Color='#0078d7', Background='#d5dcf0'))
            self.Cancel_Button.Bind(On_Hover_Out=lambda E: self.Cancel_Button.Config(Border_Color='#adadad', Background='#e1e1e1'))
            self.Cancel_Button.Bind(On_Click=lambda E: self.Frame.Hide())
            self.Cancel_Button.Create()
                
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Reset(self):
        try:
            self.Name_Entry.Set("Project1")
            self.Location_Entry.Set(os.path.join(os.path.expanduser('~'), 'Documents'))
            self.Project_Path.Set(self.Location_Entry.Get()+"/"+self.Name_Entry.Get())
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        
    def Project_Folder(self):
        try:
            Folder_Path = self.Global['GUI'].Folder(Initial=self.Location_Entry.Get())
            if Folder_Path:
                self.Location_Entry.Set(Folder_Path)
                self.Update_Path()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        
            
    def Update_Path(self):
        try:
            Error = False
            if os.path.exists(self.Location_Entry.Get()):
                self.Location_Entry.Config(Border_Color='black')
            else:
                self.Location_Entry.Config(Border_Color='red')
                Error = True
            if self.Name_Entry.Get():
                self.Name_Entry.Config(Border_Color='black')
            else:
                self.Name_Entry.Config(Border_Color='red')
                Error = True
            if Error:
                self.Error = True
                self.Project_Path.Set('Project path does not exists!')
            else:
                self.Error = False
                self.Project_Path.Set(self.Location_Entry.Get()+"/"+self.Name_Entry.Get())
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        
    def Create(self):
        try:
            Project_Path = self.Location_Entry.Get()
            Project_Name = self.Name_Entry.Get()
            if not self.Error:
                if self.Global['Custom'].Is_Empty(Project_Path):
                    self.Global['Message'].Hide()
                    with open(f'{Project_Path}/{Project_Name}.ng', 'w') as File:
                        File.write(Project_Name)
                    os.makedirs(f'{Project_Path}/Data')
                    os.makedirs(f'{Project_Path}/Data/File')
                    Icon = self.Global['Custom'].MD5(Project_Name+str(time.time()))
                    shutil.copy(self.Global['Image']("Icon", "ico"), f'{Project_Path}/Data/File/{Icon}')
                    shutil.copy(self.Global['Data']('NGD.dll'), f'{Project_Path}/Data/NGD.dll')
                    TempDatabase = self.Global['Gluonix'].SQL(f'{Project_Path}/Data/NGD.dll')
                    TempDatabase.Post(f"UPDATE `Variable` SET `DATA`='{Project_Name}' WHERE `ID`='Name'")
                    TempDatabase.Post(f"UPDATE `Variable` SET `DATA`='{Project_Name}' WHERE `ID`='Title'")
                    TempDatabase.Post(f"UPDATE `Variable` SET `DATA`='{Icon}' WHERE `ID`='Icon'")
                    TempDatabase.Post(f"UPDATE `Display` SET `Title`='{Project_Name}' WHERE `ID`='Root'")
                    TempDatabase.Close()
                    self.Project.Home.Panel.Overview.Project_Path = Project_Path
                    self.Project.Home.Panel.Overview.Update()
                    self.Frame.Hide()
                else:
                    self.Global['Message'].Show('Error', 'Project Folder Is Not Empty')
            else:
                if not os.path.exists(Project_Path):
                    self.Global['Message'].Show('Error', 'Path Does Not Exist')
                if not Project_Name:
                    self.Global['Message'].Show('Error', 'Enter A Project Name')
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))