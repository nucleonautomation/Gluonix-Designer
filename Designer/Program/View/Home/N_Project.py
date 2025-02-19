################################################################################################################################
#Menu
################################################################################################################################
import os
import inspect
import requests
import _thread
import sqlite3

#Program
from .N_Project_New import New

class Project:
    def __init__(self, Global, Home):
        try:
            self.Global = Global
            self.Home = Home
            self.Widget = []
            
            Fixture = self.Home.Frame.Locate(20, 100, 0, 0)
            self.Frame = self.Global['Gluonix'].Scroll(self.Home.Frame)
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Background='white', Border_Size=0, Display=True) 
            self.Frame.Config(Resize=True, Move=True)
            self.Frame.Create()
            
            #Project View
                #Label
            Fixture = self.Frame.Locate(70, 4, 13, 2)
            self.Project_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Project_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Project_Label.Config(Foreground='gray', Value="Project", Font_Size=16, Font_Weight='normal', Align='w', Border_Size=0)
            self.Project_Label.Create()
            
                #New
                    #Image
            Fixture = self.Frame.Locate(15, 4, 10, 8)
            self.New_Image = self.Global['Gluonix'].Image(self.Frame)
            self.New_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.New_Image.Config(Path=self.Global['Image']('New'), Border_Size=0)
            self.New_Image.Bind(On_Click=lambda E: self.Create_Project(), Cursor_Hand=True)
            self.New_Image.Create()
                    #Label
            Fixture = self.Frame.Locate(70, 4, 25, 8)
            self.New_Label = self.Global['Gluonix'].Label(self.Frame)
            self.New_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.New_Label.Config(Foreground='black', Value="New project", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.New_Label.Bind(On_Click=lambda E: self.Create_Project(), Cursor_Hand=True)
            self.New_Label.Create()
            
                #Open
                    #Image
            Fixture = self.Frame.Locate(15, 4, 10, 12)
            self.Open_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Open_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Open_Image.Config(Path=self.Global['Image']('Open'), Border_Size=0)
            self.Open_Image.Bind(On_Click=lambda E: self.Open_Project(), Cursor_Hand=True)
            self.Open_Image.Create()
                    #Label
            Fixture = self.Frame.Locate(70, 4, 25, 12)
            self.Open_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Open_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Open_Label.Config(Foreground='black', Value="Open project", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Open_Label.Bind(On_Click=lambda E: self.Open_Project(), Cursor_Hand=True)
            self.Open_Label.Create()
            
                #Version
                    #Current
            Fixture = self.Frame.Locate(17, 4, 10, 90)
            self.Current_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Current_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Current_Label.Config(Foreground='black', Value=f"V {self.Global['Version']}.{self.Global['Revision']}", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Current_Label.Create()
            
            #Create New Project
            self.New = New(self.Global, self)
                   
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Create_Project(self):
        try:
            self.New.Reset()
            self.New.Frame.Show()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        
    def Open_Project(self):
        try:
            Project_File_Path = self.Global['GUI'].File(Initial=os.path.join(os.path.expanduser('~'), 'Documents'), Title='Select Project', Default='.ng', Type=[["Nucleon Gluonix (*.ng)", "*.ng"]])
            if Project_File_Path:
                Project_Path = os.path.dirname(Project_File_Path)
                self.Update_Database(f'{Project_Path}/Data/NGD.dll', self.Global['Data']('NGD.dll'))
                self.Home.Panel.Overview.Project_Path = Project_Path
                self.Home.Panel.Overview.Update()
                self.Global['Message'].Hide()
        except Exception as E:
            self.Global['Message'].Show('Error', 'Project Files Are Corrupted')
            self.Project_Path = False
            self.Project_Name = False
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Database(self, Old_Structure_Database, New_Structure_Database):
        Conn_Old = sqlite3.connect(Old_Structure_Database)
        Conn_New = sqlite3.connect(New_Structure_Database)
        Cursor_Old = Conn_Old.cursor()
        Cursor_New = Conn_New.cursor()
        Cursor_New.execute("SELECT name FROM sqlite_master WHERE type='table';")
        Tables = Cursor_New.fetchall()
        for (Table,) in Tables:
            Cursor_New.execute(f"PRAGMA table_info({Table});")
            Columns_New = Cursor_New.fetchall()
            Cursor_Old.execute(f"PRAGMA table_info({Table});")
            Columns_Old = Cursor_Old.fetchall()
            if Columns_Old:
                Existing_Columns = {col[1] for col in Columns_Old}
                New_Columns = {col[1]: col[4] for col in Columns_New}
                for Col in Columns_New:
                    Column_Name = Col[1]
                    Column_Type = Col[2]
                    Default_Value = Col[4]
                    if Column_Name not in Existing_Columns:
                        if Default_Value is None:
                            Alter_Statement = f"ALTER TABLE {Table} ADD COLUMN {Column_Name} {Column_Type};"
                        else:
                            Alter_Statement = f"ALTER TABLE {Table} ADD COLUMN {Column_Name} {Column_Type} DEFAULT {Default_Value};"
                        Cursor_Old.execute(Alter_Statement)
            else:
                Create_Statement = f"CREATE TABLE {Table} (" + ", ".join([f"{col[1]} {col[2]} DEFAULT {col[4]}" for col in Columns_New]) + ");"
                Cursor_Old.execute(Create_Statement)
        Conn_Old.commit()