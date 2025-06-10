################################################################################################################################
#Menu
################################################################################################################################
import os
import inspect
import shutil
import time

class Compare:
    def __init__(self, Global, Project):
        try:
            self.Global = Global
            self.Project = Project
            self.Widget = []
            self.Error_1 = False
            self.Error_2 = False
            
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
            self.Info_Label.Config(Value="Select two Gluonix projects to compare")
            self.Info_Label.Create()
            
                #Project 1 Label
            Fixture = self.Frame.Locate(10, 6, 3, 24)
            self.Project_1_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Project_1_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Project_1_Label.Config(Foreground='black', Value="Project 01:", Font_Size=9, Font_Weight='normal', Align='w', Border_Size=0)
            self.Project_1_Label.Create()
            
                #Project 1 Entry
            Fixture = self.Frame.Locate(70, 6, 13, 24)
            self.Project_1_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Project_1_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Project_1_Entry.Config(Background='white', Foreground='black', Font_Size=10, Font_Weight='normal', Align='left', Border_Size=1)
            self.Project_1_Entry.Bind(On_Key_Release=lambda E: self.Project_1_Update_Path())
            self.Project_1_Entry.Create()
            
                #Project 1 Browser
            Fixture = self.Frame.Locate(12, 6, 85, 24)
            self.Project_1_Browser = self.Global['Gluonix'].Label(self.Frame)
            self.Project_1_Browser.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Project_1_Browser.Config(Background='#e1e1e1', Foreground='black', Value='Browser...', Font_Size=9, Font_Weight='normal', Border_Size=1, Border_Color='#adadad')
            self.Project_1_Browser.Bind(On_Hover_In=lambda E: self.Project_1_Browser.Config(Border_Color='#0078d7', Background='#d5dcf0'))
            self.Project_1_Browser.Bind(On_Hover_Out=lambda E: self.Project_1_Browser.Config(Border_Color='#adadad', Background='#e1e1e1'))
            self.Project_1_Browser.Bind(On_Click=lambda E: self.Project_1_File_Select())
            self.Project_1_Browser.Create()
            
                #Project 2 Label
            Fixture = self.Frame.Locate(10, 6, 3, 40)
            self.Project_2_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Project_2_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Project_2_Label.Config(Foreground='black', Value="Project 02:", Font_Size=9, Font_Weight='normal', Align='w', Border_Size=0)
            self.Project_2_Label.Create()
            
                #Project 2 Entry
            Fixture = self.Frame.Locate(70, 6, 13, 40)
            self.Project_2_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Project_2_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Project_2_Entry.Config(Background='white', Foreground='black', Font_Size=10, Font_Weight='normal', Align='left', Border_Size=1)
            self.Project_2_Entry.Bind(On_Key_Release=lambda E: self.Project_2_Update_Path())
            self.Project_2_Entry.Create()
            
                #Project 2 Browser
            Fixture = self.Frame.Locate(12, 6, 85, 40)
            self.Project_2_Browser = self.Global['Gluonix'].Label(self.Frame)
            self.Project_2_Browser.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Project_2_Browser.Config(Background='#e1e1e1', Foreground='black', Value='Browser...', Font_Size=9, Font_Weight='normal', Border_Size=1, Border_Color='#adadad')
            self.Project_2_Browser.Bind(On_Hover_In=lambda E: self.Project_2_Browser.Config(Border_Color='#0078d7', Background='#d5dcf0'))
            self.Project_2_Browser.Bind(On_Hover_Out=lambda E: self.Project_2_Browser.Config(Border_Color='#adadad', Background='#e1e1e1'))
            self.Project_2_Browser.Bind(On_Click=lambda E: self.Project_2_File_Select())
            self.Project_2_Browser.Create()
            
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
            self.Project_1_Entry.Set('')
            self.Project_2_Entry.Set('')
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        
    def Project_1_File_Select(self):
        try:
            Project_File_Path = self.Global['GUI'].File(Initial=os.path.join(os.path.expanduser('~'), 'Documents'), Title='Select Project', Default='.ng', Type=[["Nucleon Gluonix (*.ng)", "*.ng"]])
            if Project_File_Path:
                self.Project_1_Entry.Set(Project_File_Path)
                self.Project_1_Update_Path()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        
            
    def Project_1_Update_Path(self):
        try:
            if os.path.exists(self.Project_1_Entry.Get()):
                self.Project_1_Entry.Config(Border_Color='black')
                self.Error_1 = False
            else:
                self.Project_1_Entry.Config(Border_Color='red')
                self.Error_1 = True
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        
    def Project_2_File_Select(self):
        try:
            Project_File_Path = self.Global['GUI'].File(Initial=os.path.join(os.path.expanduser('~'), 'Documents'), Title='Select Project', Default='.ng', Type=[["Nucleon Gluonix (*.ng)", "*.ng"]])
            if Project_File_Path:
                self.Project_2_Entry.Set(Project_File_Path)
                self.Project_2_Update_Path()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        
            
    def Project_2_Update_Path(self):
        try:
            if os.path.exists(self.Project_2_Entry.Get()):
                self.Project_2_Entry.Config(Border_Color='black')
                self.Error_2 = False
            else:
                self.Project_2_Entry.Config(Border_Color='red')
                self.Error_2 = True
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        
    def Create(self):
        try:
            Project_1_Path = self.Project_1_Entry.Get()
            Project_2_Path = self.Project_2_Entry.Get()
            if not self.Error_1 and not self.Error_2:
                self.Global['Message'].Hide()
                Project_1_Path = os.path.dirname(Project_1_Path)
                Project_2_Path = os.path.dirname(Project_2_Path)
                self.Project.Update_Database(f'{Project_1_Path}/Data/NGD.dll', self.Global['Data']('NGD.dll'))
                self.Project.Update_Database(f'{Project_2_Path}/Data/NGD.dll', self.Global['Data']('NGD.dll'))
                self.Project.Home.Main.Compare.Project_1_Path = Project_1_Path
                self.Project.Home.Main.Compare.Project_2_Path = Project_2_Path
                self.Project.Home.Main.Compare.Update()
                self.Global['Message'].Hide()
                self.Frame.Hide()
            else:
                if self.Error_1:
                    self.Global['Message'].Show('Error', 'Project 01 Does Not Exist')
                if self.Error_2:
                    self.Global['Message'].Show('Error', 'Project 02 Does Not Exist')
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))