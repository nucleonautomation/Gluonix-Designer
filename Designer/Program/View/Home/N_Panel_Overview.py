################################################################################################################################
#Menu
################################################################################################################################
import os
import math
import shutil
import inspect
from tkinter import colorchooser

class Overview:
    def __init__(self, Global, Panel):
        try:
            self.Global = Global
            self.Panel = Panel
            self.Widget = []
            self.Project_Path = False
            self.Runtime_Path = False
            self.TempDatabase = False
            self.Launch = False
            self.Direct = False
            self.Resize = False
            
            Fixture = self.Panel.Frame.Locate(100, 100, 0, 0)
            self.Frame = self.Global['Gluonix'].Frame(self.Panel.Frame)
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Border_Size=0, Display=False)
            self.Frame.Create()
            self.Panel.Widget.append(self.Frame)
            
                #Info Label
            Fixture = self.Frame.Locate(35, 8, 3, 5)
            self.Info_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Info_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Info_Label.Config(Foreground='black', Value="Project Configuration:", Font_Size=14, Font_Weight='bold', Align='w', Border_Size=0)
            self.Info_Label.Create()
            
                #Display Label
            Fixture = self.Frame.Locate(8, 4, 63, 7)
            self.Display_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Display_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Display_Label.Config(Foreground='black', Value="Display:", Font_Size=14, Font_Weight='bold', Align='w', Border_Size=0)
            self.Display_Label.Create()
            
                #Display Select
            Fixture = self.Frame.Locate(15, 4, 72, 7)
            self.Display_Select = self.Global['Gluonix'].Select(self.Frame)
            self.Display_Select.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Display_Select.Config(Foreground='black', Font_Size=11, Font_Weight='normal', Align='center', Border_Size=1)
            self.Display_Select.Bind(On_Change=lambda E: self.Update(Partial=True))
            self.Display_Select.Create()
            
                #Add Image
            Fixture = self.Frame.Locate(3, 4, 88, 7)
            self.Add_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Add_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Add_Image.Config(Background=False, Border_Size=0, Hand_Cursor=True)
            self.Add_Image.Config(Path=self.Global['Image']('Add'))
            self.Add_Image.Bind(On_Click=lambda E: self.Add())
            self.Add_Image.Create()
            
                #Delete Image
            Fixture = self.Frame.Locate(3.5, 5, 91.5, 6.5)
            self.Delete_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Delete_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Delete_Image.Config(Background=False, Border_Size=0, Hand_Cursor=True)
            self.Delete_Image.Config(Path=self.Global['Image']('Delete'))
            self.Delete_Image.Bind(On_Click=lambda E: self.Delete_Show())
            self.Delete_Image.Create()
            
                #Delete Confirm Image
            Fixture = self.Frame.Locate(3, 4, 88, 7)
            self.Delete_Confirm_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Delete_Confirm_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Delete_Confirm_Image.Config(Background=False, Border_Size=0, Hand_Cursor=True)
            self.Delete_Confirm_Image.Config(Path=self.Global['Image']('Success'))
            self.Delete_Confirm_Image.Bind(On_Click=lambda E: self.Delete())
            self.Delete_Confirm_Image.Create()
            
                #Delete Cancel Image
            Fixture = self.Frame.Locate(3, 4, 91.5, 7)
            self.Delete_Cancel_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Delete_Cancel_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Delete_Cancel_Image.Config(Background=False, Border_Size=0, Hand_Cursor=True)
            self.Delete_Cancel_Image.Config(Path=self.Global['Image']('Close'))
            self.Delete_Cancel_Image.Bind(On_Click=lambda E: self.Delete_Hide())
            self.Delete_Cancel_Image.Create()
            
                #Title Label
            Fixture = self.Frame.Locate(7, 5, 3, 16)
            self.Title_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Title_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Title_Label.Config(Foreground='black', Value="Title:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Title_Label.Create()
            
                #Title Entry
            Fixture = self.Frame.Locate(30, 5, 12, 16)
            self.Title_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Title_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Title_Entry.Config(Background='white', Foreground='black', Font_Size=10, Font_Weight='normal', Align='left', Border_Size=1)
            self.Title_Entry.Create()
            
                #Background Label
            Fixture = self.Frame.Locate(15, 5, 47, 16)
            self.Background_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Background_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Background_Label.Config(Foreground='black', Value="Background:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Background_Label.Create()
            
                #Background Color
            Fixture = self.Frame.Locate(4, 5, 61, 16)
            self.Background_Color = self.Global['Gluonix'].Label(self.Frame)
            self.Background_Color.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Background_Color.Config(Background='white', Foreground='black', Font_Size=10, Font_Weight='normal', Align='w', Border_Size=1)
            self.Background_Color.Bind(On_Click=lambda E: self.Select_Color())
            self.Background_Color.Create()
            
                #Alignment Label
            Fixture = self.Frame.Locate(12, 5, 70, 16)
            self.Alignment_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Alignment_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Alignment_Label.Config(Foreground='black', Value="Alignment:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Alignment_Label.Create()
            
                #Alignment Select
            Fixture = self.Frame.Locate(12, 5, 82, 16)
            self.Alignment_Select = self.Global['Gluonix'].Select(self.Frame)
            self.Alignment_Select.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Alignment_Select.Config(Background='white', Foreground='black', Font_Size=11, Font_Weight='normal', Align='center', Border_Size=1)
            self.Alignment_Select.Create()
            self.Alignment_Select.Add('Percentage')
            self.Alignment_Select.Add('Pixel')
            
                #Width Label
            Fixture = self.Frame.Locate(7, 5, 3, 25)
            self.Width_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Width_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Width_Label.Config(Foreground='black', Value="Width:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Width_Label.Create()

                #Width Entry
            Fixture = self.Frame.Locate(7, 5, 12, 25)
            self.Width_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Width_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Width_Entry.Config(Background='white', Foreground='black', Font_Size=10, Font_Weight='normal', Align='center', Border_Size=1)
            self.Width_Entry.Create()
            
                #Height Label
            Fixture = self.Frame.Locate(7, 5, 22, 25)
            self.Height_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Height_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Height_Label.Config(Foreground='black', Value="Height:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Height_Label.Create()

                #Width Entry
            Fixture = self.Frame.Locate(7, 5, 31, 25)
            self.Height_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Height_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Height_Entry.Config(Background='white', Foreground='black', Font_Size=10, Font_Weight='normal', Align='center', Border_Size=1)
            self.Height_Entry.Create()
            
                #Left Label
            Fixture = self.Frame.Locate(7, 5, 41, 25)
            self.Left_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Left_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Left_Label.Config(Foreground='black', Value="Left:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Left_Label.Create()

                #Left Entry
            Fixture = self.Frame.Locate(7, 5, 49, 25)
            self.Left_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Left_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Left_Entry.Config(Background='white', Foreground='black', Font_Size=10, Font_Weight='normal', Align='center', Border_Size=1)
            self.Left_Entry.Create()
            
                #Top Label
            Fixture = self.Frame.Locate(7, 5, 59, 25)
            self.Top_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Top_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Top_Label.Config(Foreground='black', Value="Top:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Top_Label.Create()

                #Top Entry
            Fixture = self.Frame.Locate(7, 5, 67, 25)
            self.Top_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Top_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Top_Entry.Config(Background='white', Foreground='black', Font_Size=10, Font_Weight='normal', Align='center', Border_Size=1)
            self.Top_Entry.Create()
            
                #Full Screen Label
            Fixture = self.Frame.Locate(12, 5, 3, 34)
            self.Full_Screen_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Full_Screen_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Full_Screen_Label.Config(Foreground='black', Value="Full Screen:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Full_Screen_Label.Create()
            
                #Full Screen Check
            Fixture = self.Frame.Locate(4, 5, 15, 34)
            self.Full_Screen_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Full_Screen_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Full_Screen_Check.Config(Border_Size=0)
            self.Full_Screen_Check.Create()
            
                #Resizable Label
            Fixture = self.Frame.Locate(12, 5, 26, 34)
            self.Resizable_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Resizable_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Resizable_Label.Config(Foreground='black', Value="Resizable:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Resizable_Label.Create()
            
                #Resizable Check
            Fixture = self.Frame.Locate(4, 5, 38, 34)
            self.Resizable_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Resizable_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Resizable_Check.Config(Border_Size=0)
            self.Resizable_Check.Create()
            
                #Persistent Label
            Fixture = self.Frame.Locate(12, 5, 49, 34)
            self.Persistent_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Persistent_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Persistent_Label.Config(Foreground='black', Value="Persistent:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Persistent_Label.Create()
            
                #Persistent Check
            Fixture = self.Frame.Locate(4, 5, 61, 34)
            self.Persistent_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Persistent_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Persistent_Check.Config(Border_Size=0)
            self.Persistent_Check.Create()
            
                #Menu Label
            Fixture = self.Frame.Locate(12, 5, 72, 34)
            self.Menu_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Menu_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Menu_Label.Config(Foreground='black', Value="Menu:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Menu_Label.Create()
            
                #Menu Check
            Fixture = self.Frame.Locate(4, 5, 84, 34)
            self.Menu_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Menu_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Menu_Check.Config(Border_Size=0)
            self.Menu_Check.Create()
            
                #Toolbar Label
            Fixture = self.Frame.Locate(12, 5, 3, 43)
            self.Toolbar_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Toolbar_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Toolbar_Label.Config(Foreground='black', Value="Toolbar:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Toolbar_Label.Create()
            
                #Toolbar Check
            Fixture = self.Frame.Locate(4, 5, 15, 43)
            self.Toolbar_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Toolbar_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Toolbar_Check.Config(Border_Size=0)
            self.Toolbar_Check.Create()
            
                #Error Log Label
            Fixture = self.Frame.Locate(12, 5, 26, 43)
            self.Error_Log_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Error_Log_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Error_Log_Label.Config(Foreground='black', Value="Error Log:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Error_Log_Label.Create()
            
                #Error Log Check
            Fixture = self.Frame.Locate(4, 5, 38, 43)
            self.Error_Log_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Error_Log_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Error_Log_Check.Config(Border_Size=0)
            self.Error_Log_Check.Create()
            
                #Topmost Label
            Fixture = self.Frame.Locate(12, 5, 26, 43)
            self.Topmost_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Topmost_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Topmost_Label.Config(Foreground='black', Value="Topmost:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Topmost_Label.Create()
            self.Topmost_Label.Hide()
            
                #Topmost Check
            Fixture = self.Frame.Locate(4, 5, 38, 43)
            self.Topmost_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Topmost_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Topmost_Check.Config(Border_Size=0)
            self.Topmost_Check.Create()
            self.Topmost_Check.Hide()
            
                #Version Label
            Fixture = self.Frame.Locate(12, 5, 49, 43)
            self.Version_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Version_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Version_Label.Config(Foreground='black', Value="Version:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Version_Label.Create()
            
                #Version Entry
            Fixture = self.Frame.Locate(6, 5, 61, 43)
            self.Version_Entry = self.Global['Gluonix'].Spinner(self.Frame)
            self.Version_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Version_Entry.Config(Background='white', Foreground='black', Font_Size=10, Font_Weight='normal', Align='center', Border_Size=1)
            self.Version_Entry.Create()
            
                #Revision Label
            Fixture = self.Frame.Locate(12, 5, 72, 43)
            self.Revision_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Revision_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Revision_Label.Config(Foreground='black', Value="Revision:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Revision_Label.Create()
            
                #Revision Entry
            Fixture = self.Frame.Locate(6, 5, 84, 43)
            self.Revision_Entry = self.Global['Gluonix'].Spinner(self.Frame)
            self.Revision_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Revision_Entry.Config(Background='white', Foreground='black', Font_Size=10, Font_Weight='normal', Align='center', Border_Size=1)
            self.Revision_Entry.Create()
            
                #Icon Label
            Fixture = self.Frame.Locate(7, 5, 3, 52)
            self.Icon_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Icon_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Icon_Label.Config(Foreground='black', Value="Icon:", Font_Size=12, Font_Weight='normal', Align='w', Border_Size=0)
            self.Icon_Label.Create()
            
                #Icon Image
            Fixture = self.Frame.Locate(15, 15, 12, 52)
            self.Icon_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Icon_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Icon_Image.Config(Background='white', Border_Size=1, Hand_Cursor=True)
            self.Icon_Image.Create()
            
                #Icon Browser
            Fixture = self.Frame.Locate(12, 6, 30, 52)
            self.Icon_Browser = self.Global['Gluonix'].Label(self.Frame)
            self.Icon_Browser.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Icon_Browser.Config(Background='#e1e1e1', Foreground='black', Value='Browser...', Font_Size=9, Font_Weight='normal', Border_Size=1, Border_Color='#adadad')
            self.Icon_Browser.Bind(On_Hover_In=lambda E: self.Icon_Browser.Config(Border_Color='#0078d7', Background='#d5dcf0'))
            self.Icon_Browser.Bind(On_Hover_Out=lambda E: self.Icon_Browser.Config(Border_Color='#adadad', Background='#e1e1e1'))
            self.Icon_Browser.Bind(On_Click=lambda E: self.Select_Icon())
            self.Icon_Browser.Create()
            
                #Deploy Button
            Fixture = self.Frame.Locate(8, 6, 66, 88)
            self.Deploy_Button = self.Global['Gluonix'].Label(self.Frame)
            self.Deploy_Button.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Deploy_Button.Config(Background='#D2B4DE', Foreground='black', Value='Deploy', Font_Size=9, Font_Weight='normal', Border_Size=1, Border_Color='#5B2C6F')
            self.Deploy_Button.Bind(On_Hover_In=lambda E: self.Deploy_Button.Config(Background='#8E44AD'))
            self.Deploy_Button.Bind(On_Hover_Out=lambda E: self.Deploy_Button.Config(Background='#D2B4DE'))
            self.Deploy_Button.Bind(On_Click=lambda E: self.Deploy())
            self.Deploy_Button.Create()
            
                #Design Button
            Fixture = self.Frame.Locate(8, 6, 76, 88)
            self.Design_Button = self.Global['Gluonix'].Label(self.Frame)
            self.Design_Button.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Design_Button.Config(Background='#FAD7A0', Foreground='black', Value='Design', Font_Size=9, Font_Weight='normal', Border_Size=1, Border_Color='#935116')
            self.Design_Button.Bind(On_Hover_In=lambda E: self.Design_Button.Config(Background='#F39C12'))
            self.Design_Button.Bind(On_Hover_Out=lambda E: self.Design_Button.Config(Background='#FAD7A0'))
            self.Design_Button.Bind(On_Click=lambda E: self.Save_Check(Launch=True, Direct=True))
            self.Design_Button.Create()
            
                #Save Button
            Fixture = self.Frame.Locate(8, 6, 86, 88)
            self.Save_Button = self.Global['Gluonix'].Label(self.Frame)
            self.Save_Button.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Save_Button.Config(Background='#ABEBC6', Foreground='black', Value='Save', Font_Size=9, Font_Weight='normal', Border_Size=1, Border_Color='#1D8348')
            self.Save_Button.Bind(On_Hover_In=lambda E: self.Save_Button.Config(Background='#2ECC71'))
            self.Save_Button.Bind(On_Hover_Out=lambda E: self.Save_Button.Config(Background='#ABEBC6'))
            self.Save_Button.Bind(On_Click=lambda E: self.Save_Check())
            self.Save_Button.Create()
            
                #Resize Frame
            Fixture = self.Frame.Locate(28, 20, 66, 66)
            self.Resize_Frame = self.Global['Gluonix'].Frame(self.Frame)
            self.Resize_Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Resize_Frame.Config(Border_Size=3, Display=False, Background='#FFFFFF')
            self.Resize_Frame.Create()
            
                    #Resize Label
            Fixture = self.Resize_Frame.Locate(90, 50, 5, 10)
            self.Resize_Label = self.Global['Gluonix'].Label(self.Resize_Frame)
            self.Resize_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Resize_Label.Config(Foreground='black', Value="", Font_Size=12, Font_Weight='normal', Align='center', Border_Size=0)
            self.Resize_Label.Create()
            self.Resize_Label.Set("Resize all widgets to adjust for new screen size?")
            
                    #Resize Reject Button
            Fixture = self.Resize_Frame.Locate(35, 25, 55, 65)
            self.Resize_Reject_Button = self.Global['Gluonix'].Label(self.Resize_Frame)
            self.Resize_Reject_Button.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Resize_Reject_Button.Config(Background='#F5B7B1', Foreground='black', Value='Reject', Font_Size=9, Font_Weight='normal', Border_Size=1, Border_Color='#1D8348')
            self.Resize_Reject_Button.Bind(On_Hover_In=lambda E: self.Resize_Reject_Button.Config(Background='#E74C3C'))
            self.Resize_Reject_Button.Bind(On_Hover_Out=lambda E: self.Resize_Reject_Button.Config(Background='#F5B7B1'))
            self.Resize_Reject_Button.Bind(On_Click=lambda E: self.Resize_Reject())
            self.Resize_Reject_Button.Create()
            
                    #Resize Accept Button
            Fixture = self.Resize_Frame.Locate(35, 25, 10, 65)
            self.Resize_Accept_Button = self.Global['Gluonix'].Label(self.Resize_Frame)
            self.Resize_Accept_Button.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Resize_Accept_Button.Config(Background='#ABEBC6', Foreground='black', Value='Accept', Font_Size=9, Font_Weight='normal', Border_Size=1, Border_Color='#1D8348')
            self.Resize_Accept_Button.Bind(On_Hover_In=lambda E: self.Resize_Accept_Button.Config(Background='#2ECC71'))
            self.Resize_Accept_Button.Bind(On_Hover_Out=lambda E: self.Resize_Accept_Button.Config(Background='#ABEBC6'))
            self.Resize_Accept_Button.Bind(On_Click=lambda E: self.Resize_Accept())
            self.Resize_Accept_Button.Create()
            
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Save(self, Loading=True):
        try:
            if Loading:
                self.Global['Loading'].Show()
                self.Global['GUI'].After(500, lambda:self.Save(Loading=False))
            else:
                Error = False
                if not Error and self.Title_Entry.Get()=='':
                    Error = True
                    self.Global['Message'].Show('Error', 'Enter Project Title')
                if not Error and not self.Width_Entry.Get().isdigit():
                    Error = True
                    self.Global['Message'].Show('Error', 'Incorrect Width Value')
                if not Error and not self.Height_Entry.Get().isdigit():
                    Error = True
                    self.Global['Message'].Show('Error', 'Incorrect Height Value')
                if not Error and not self.Left_Entry.Get().isdigit():
                    Error = True
                    self.Global['Message'].Show('Error', 'Incorrect Left Value')
                if not Error and not self.Top_Entry.Get().isdigit():
                    Error = True
                    self.Global['Message'].Show('Error', 'Incorrect Top Value')
                if not Error and not self.Version_Entry.Get().isdigit():
                    Error = True
                    self.Global['Message'].Show('Error', 'Incorrect Version Value')
                if not Error and not self.Revision_Entry.Get().isdigit():
                    Error = True
                    self.Global['Message'].Show('Error', 'Incorrect Revision Value')
                if not Error:
                    self.Display_ID = self.Display_Select.Get()
                    Project_Name = self.Title_Entry.Get()
                    if self.Display_ID=='Root':
                        for File_Name in os.listdir(self.Project_Path):
                            if File_Name.endswith('.ng'):
                                os.remove(f'{self.Project_Path}/{File_Name}')
                        with open(f'{self.Project_Path}/{Project_Name}.ng', 'w') as File:
                            File.write(Project_Name)
                        self.Project_Data['Name'] = Project_Name
                    self.Project_Data['Error_Log'] = str(int(self.Error_Log_Check.Get()))
                    self.Project_Data['Version'] = self.Version_Entry.Get()
                    self.Project_Data['Revision'] = self.Revision_Entry.Get()
                    self.Project_Data['NGD'] = f"{self.Global['Version']}.{self.Global['Revision']}"
                    self.Display_Data['Title'] = Project_Name
                    self.Display_Data['Background'] = self.Background_Color.Config_Get('Background')['Background']
                    self.Display_Data['Alignment'] = self.Alignment_Select.Get()
                    self.Display_Data['Width'] = self.Width_Entry.Get()
                    self.Display_Data['Height'] = self.Height_Entry.Get()
                    self.Display_Data['Left'] = self.Left_Entry.Get()
                    self.Display_Data['Top'] = self.Top_Entry.Get()
                    self.Display_Data['Full_Screen'] = str(int(self.Full_Screen_Check.Get()))
                    self.Display_Data['Resizable'] = str(int(self.Resizable_Check.Get()))
                    self.Display_Data['Persistent'] = str(int(self.Persistent_Check.Get()))
                    self.Display_Data['Menu'] = str(int(self.Menu_Check.Get()))
                    self.Display_Data['Toolbar'] = str(int(self.Toolbar_Check.Get()))
                    self.Display_Data['Topmost'] = str(int(self.Topmost_Check.Get()))
                    TempDatabase = self.Global['Gluonix'].SQL(f'{self.Project_Path}/Data/NGD.dll')
                    Display_Data_Temp = TempDatabase.Get(f"SELECT * FROM `Display` WHERE `ID`='{self.Display_ID}'", Keys=True)
                    TempDatabase.Post(f"UPDATE `Display` SET `Title`='{self.Display_Data['Title']}' WHERE `ID`='{self.Display_ID}'")
                    TempDatabase.Post(f"UPDATE `Display` SET `Background`='{self.Display_Data['Background']}' WHERE `ID`='{self.Display_ID}'")
                    TempDatabase.Post(f"UPDATE `Display` SET `Alignment`='{self.Display_Data['Alignment']}' WHERE `ID`='{self.Display_ID}'")
                    TempDatabase.Post(f"UPDATE `Display` SET `Width`='{self.Display_Data['Width']}' WHERE `ID`='{self.Display_ID}'")
                    TempDatabase.Post(f"UPDATE `Display` SET `Height`='{self.Display_Data['Height']}' WHERE `ID`='{self.Display_ID}'")
                    TempDatabase.Post(f"UPDATE `Display` SET `Left`='{self.Display_Data['Left']}' WHERE `ID`='{self.Display_ID}'")
                    TempDatabase.Post(f"UPDATE `Display` SET `Top`='{self.Display_Data['Top']}' WHERE `ID`='{self.Display_ID}'")
                    TempDatabase.Post(f"UPDATE `Display` SET `Full_Screen`='{self.Display_Data['Full_Screen']}' WHERE `ID`='{self.Display_ID}'")
                    TempDatabase.Post(f"UPDATE `Display` SET `Resizable`='{self.Display_Data['Resizable']}' WHERE `ID`='{self.Display_ID}'")
                    TempDatabase.Post(f"UPDATE `Display` SET `Persistent`='{self.Display_Data['Persistent']}' WHERE `ID`='{self.Display_ID}'")
                    TempDatabase.Post(f"UPDATE `Display` SET `Menu`='{self.Display_Data['Menu']}' WHERE `ID`='{self.Display_ID}'")
                    TempDatabase.Post(f"UPDATE `Display` SET `Toolbar`='{self.Display_Data['Toolbar']}' WHERE `ID`='{self.Display_ID}'")
                    TempDatabase.Post(f"UPDATE `Display` SET `Topmost`='{self.Display_Data['Topmost']}' WHERE `ID`='{self.Display_ID}'")
                    if f"{self.Project_Path}/Data/File/{self.Project_Data['Icon']}"!=self.Icon_Image.Config_Get('Path')['Path']:
                        if os.path.exists(f"{self.Project_Path}/Data/File/{self.Project_Data['Icon']}"):
                            os.remove(f"{self.Project_Path}/Data/File/{self.Project_Data['Icon']}")
                        shutil.copy(self.Icon_Image.Config_Get('Path')['Path'], f"{self.Project_Path}/Data/File/{self.Project_Data['Icon']}")
                    if not self.Direct:
                        self.Direct = False
                        self.Global['Loading'].Hide()
                        self.Global['Message'].Show('Success', 'Save Successfull')
                        self.Global['Message'].Hide(Delay=2)
                    if self.Resize:
                        self.Resize = False
                        self.Display_Data = Display_Data_Temp[0]
                        Old_Width = self.Display_Data['Width']
                        Old_Height = self.Display_Data['Height']
                        Current_Width = int(self.Width_Entry.Get())
                        Current_Height = int(self.Height_Entry.Get())
                        Width_Ratio = float(Current_Width) / Old_Width
                        Height_Ratio = float(Current_Height) / Old_Height
                        if Width_Ratio < 1.0 or Height_Ratio < 1.0:
                            Font_Ratio = min(Width_Ratio, Height_Ratio)
                        else:
                            Font_Ratio = (Width_Ratio * Height_Ratio) ** 0.5
                        def Update_Size(Frame_ID):
                            TempDatabase.Post(f"UPDATE `Frame` SET Width=Width*{Width_Ratio}, Height=Height*{Height_Ratio}, Left=Left*{Width_Ratio}, Top=Top*{Height_Ratio} WHERE `ID`='{Frame_ID}'")
                            TempDatabase.Post(f"UPDATE `Widget` SET Width=Width*{Width_Ratio}, Height=Height*{Height_Ratio}, Left=Left*{Width_Ratio}, Top=Top*{Height_Ratio}, Font_Size=CAST(Font_Size*{Font_Ratio} AS INTEGER) WHERE `Root`='{Frame_ID}'")
                            TempDatabase.Post(f"UPDATE `Item` SET Width=Width*{Width_Ratio}, Height=Height*{Height_Ratio}, Left=Left*{Width_Ratio}, Top=Top*{Height_Ratio}, Size=CAST(Size*{Font_Ratio} AS INTEGER) WHERE `Root`='{Frame_ID}'")
                            Frames = TempDatabase.Get(f"SELECT * FROM `Frame` WHERE `Root`='{Frame_ID}'", Keys=True)
                            for Frame in Frames:
                                Update_Size(Frame['ID'])
                        Update_Size(self.Display_ID)
                    if self.Launch:
                        self.Launch = False
                        self.Panel.Home.Main.Design.Configure.Reset_All()
                        self.Panel.Home.Main.Design.Project_Path = self.Project_Path
                        self.Panel.Home.Main.Design.Project_Data = self.Project_Data
                        self.Panel.Home.Main.Design.Display_ID = self.Display_ID
                        self.Panel.Home.Frame.Hide()
                        self.Panel.Home.Main.Design.Update(Loading=False)
                    TempDatabase.Close()
                    return True
                else:
                    self.Global['Loading'].Hide()
                    return False
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Save_Check(self, Launch=False, Direct=False):
        try:
            self.Launch = Launch
            self.Direct = Direct
            Save = True
            TempDatabase = self.Global['Gluonix'].SQL(f'{self.Project_Path}/Data/NGD.dll')
            Display_Data_Temp = TempDatabase.Get(f"SELECT * FROM `Display` WHERE `ID`='{self.Display_ID}'", Keys=True)
            self.Display_Data = Display_Data_Temp[0]
            Old_Alignment = self.Display_Data['Alignment']
            Old_Width = self.Display_Data['Width']
            Old_Height = self.Display_Data['Height']
            Current_Alignment = self.Alignment_Select.Get()
            Current_Width = int(self.Width_Entry.Get())
            Current_Height = int(self.Height_Entry.Get())
            if Old_Alignment=='Pixel' and Current_Alignment=='Pixel':
                if Old_Width!=Current_Width or Old_Height!=Current_Height:
                    Save = False
                    self.Resize_Frame.Show()
            if Save:
                self.Save()
            return True
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Resize_Accept(self):
        try:
            self.Resize_Frame.Hide()
            self.Resize = True
            self.Save()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Resize_Reject(self):
        try:
            self.Resize_Frame.Hide()
            self.Resize = False
            self.Save()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Deploy(self, Loading=True):
        try:
            if Loading:
                if self.Runtime_Path:
                    Initial = self.Runtime_Path
                else:
                    Initial = os.path.join(os.path.expanduser('~'), 'Documents')
                Path = self.Global['GUI'].Folder(Initial=Initial, Title='Select Runtime Folder')
                if Path:
                    Temp_Path = Path.replace('/', '\\')
                    if Temp_Path!=self.Project_Path:
                        self.Runtime_Path = Path
                        self.Global['Loading'].Show()
                        self.Global['GUI'].After(500, lambda:self.Deploy(Loading=False))
                    else:
                        self.Global['Message'].Show('Error', 'Project Path Cannot Be Runtime Path')
            else:
                if self.Save_Check(Direct=True):
                    if os.path.exists(f'{self.Runtime_Path}/Nucleon'):
                        shutil.rmtree(f'{self.Runtime_Path}/Nucleon')
                    shutil.copytree(self.Global['Relative_Path']('Nucleon'), f'{self.Runtime_Path}/Nucleon')
                    shutil.copytree(f'{self.Project_Path}/Data', f'{self.Runtime_Path}/Nucleon/Data')
                    Temp_Name = self.Title_Entry.Get()
                    if not os.path.exists(f'{self.Runtime_Path}/{Temp_Name}.py'):
                        shutil.copy(self.Global['Relative_Path']('Program/Base/GUI.py'), f'{self.Runtime_Path}/{Temp_Name}.py')
                    self.Global['Message'].Show('Success', 'Project Deployed')
                    if self.Global['GUI']._Window:
                        os.startfile(self.Runtime_Path)
                self.Global['Loading'].Hide()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Add(self):
        try:
            TempDatabase = self.Global['Gluonix'].SQL(f'{self.Project_Path}/Data/NGD.dll')
            X = 1
            Popup_Data = TempDatabase.Get(f"SELECT * FROM `Display` WHERE `ID`='Popup{X}'", Keys=True)
            while len(Popup_Data)>0:
                X+=1
                Popup_Data = TempDatabase.Get(f"SELECT * FROM `Display` WHERE `ID`='Popup{X}'", Keys=True)
            ID = f'Popup{X}'
            TempDatabase.Post(f"INSERT INTO `Display` (`ID`) VALUES ('{ID}')")
            self.Display_Select.Add(ID)
            self.Display_Select.Set(ID)
            self.Update(Partial=True)
            TempDatabase.Close()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Delete_Show(self):
        try:
            self.Delete_Image.Hide()
            self.Delete_Confirm_Image.Show()
            self.Delete_Cancel_Image.Show()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Delete_Hide(self):
        try:
            self.Delete_Confirm_Image.Hide()
            self.Delete_Cancel_Image.Hide()
            if self.Display_Select.Get()!='Root':
                self.Delete_Image.Show()
            else:
                self.Delete_Image.Hide()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Delete(self):
        try:
            self.TempDatabase = self.Global['Gluonix'].SQL(f'{self.Project_Path}/Data/NGD.dll')
            Display_ID = self.Display_Select.Get()
            if Display_ID==self.Display_ID and Display_ID!='Root' and self.Display_ID!='Root':
                self.Delete_All(Display_ID)
            self.TempDatabase.Close()
            self.TempDatabase = False
            self.Display_Select.Remove(Display_ID)
            self.Display_Select.Set('Root')
            self.Update(Partial=True)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Delete_All(self, Parent=False):
        try:
            if Parent:
                Frames = self.TempDatabase.Get(f"SELECT * FROM `Frame` WHERE `Root`='{Parent}'", Keys=True)
                for Frame in Frames:
                    self.Delete_All(Parent=Frame['ID'])
                self.TempDatabase.Post(f"Delete FROM `Widget` WHERE `Root`='{Parent}'")
                self.TempDatabase.Post(f"Delete FROM `Frame` WHERE `ID`='{Parent}'")
                self.TempDatabase.Post(f"Delete FROM `Display` WHERE `ID`='{Parent}'")
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update(self, Partial=False):
        try:
            if os.path.exists(f'{self.Project_Path}/Data/NGD.dll'):
                TempDatabase = self.Global['Gluonix'].SQL(f'{self.Project_Path}/Data/NGD.dll')
                if not Partial:
                    self.Project_Data = {}
                    Project_Data_Temp = TempDatabase.Get("SELECT * FROM `Variable`", Keys=True)
                    for Each in Project_Data_Temp:
                        self.Project_Data[Each['ID']] = Each['Data']
                    Display_Data_Temp = TempDatabase.Get("SELECT * FROM `Display`", Keys=True)
                    self.Display_Select.Clear()
                    for Each in Display_Data_Temp:
                        self.Display_Select.Add(Each['ID'])
                    self.Display_Select.Set('Root')
                    self.Error_Log_Check.Set(bool(int(self.Project_Data['Error_Log'])))
                    self.Version_Entry.Set(self.Project_Data['Version'])
                    self.Revision_Entry.Set(self.Project_Data['Revision'])
                    self.Icon_Image.Set(f"{self.Project_Path}/Data/File/{self.Project_Data['Icon']}")
                self.Display_ID = self.Display_Select.Get()
                self.Display_Select.Sort()
                Display_Data_Temp = TempDatabase.Get(f"SELECT * FROM `Display` WHERE `ID`='{self.Display_ID}'", Keys=True)
                self.Display_Data = Display_Data_Temp[0]
                self.Title_Entry.Set(self.Display_Data['Title'])
                self.Background_Color.Config(Background=self.Display_Data['Background'])
                self.Alignment_Select.Set(self.Display_Data['Alignment'])
                self.Width_Entry.Set(self.Display_Data['Width'])
                self.Height_Entry.Set(self.Display_Data['Height'])
                self.Left_Entry.Set(self.Display_Data['Left'])
                self.Top_Entry.Set(self.Display_Data['Top'])
                self.Full_Screen_Check.Set(bool(int(self.Display_Data['Full_Screen'])))
                self.Resizable_Check.Set(bool(int(self.Display_Data['Resizable'])))
                self.Persistent_Check.Set(bool(int(self.Display_Data['Persistent'])))
                self.Menu_Check.Set(bool(int(self.Display_Data['Menu'])))
                self.Toolbar_Check.Set(bool(int(self.Display_Data['Toolbar'])))
                self.Topmost_Check.Set(bool(int(self.Display_Data['Topmost'])))
                if self.Display_ID=='Root':
                    self.Error_Log_Label.Show()
                    self.Error_Log_Check.Show()
                    self.Topmost_Label.Hide()
                    self.Topmost_Check.Hide()
                    self.Version_Label.Show()
                    self.Version_Entry.Show()
                    self.Revision_Label.Show()
                    self.Revision_Entry.Show()
                    self.Icon_Label.Show()
                    self.Icon_Image.Show()
                    self.Icon_Browser.Show()
                else:
                    self.Topmost_Label.Show()
                    self.Topmost_Check.Show()
                    self.Error_Log_Label.Hide()
                    self.Error_Log_Check.Hide()
                    self.Version_Label.Hide()
                    self.Version_Entry.Hide()
                    self.Revision_Label.Hide()
                    self.Revision_Entry.Hide()
                    self.Icon_Label.Hide()
                    self.Icon_Image.Hide()
                    self.Icon_Browser.Hide()
                self.Delete_Hide()
                self.Frame.Show()
                TempDatabase.Close()
            else:
                self.Global['Message'].Show('Error', 'Project files not found')
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Select_Color(self):
        try:
            Color = colorchooser.askcolor(color=self.Background_Color.Config_Get('Background')['Background'], title ="Choose Background Color")[1]
            if Color is not None:
                self.Background_Color.Config(Background=Color)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
    
    def Select_Icon(self):
        try:
            Icon_File_Path = self.Global['GUI'].File(Initial=os.path.join(os.path.expanduser('~'), 'Documents'), Title='Select Icon', Default='.ico', Type=[["Icon (*.ico)", "*.ico"]])
            if Icon_File_Path:
                self.Icon_Image.Set(Icon_File_Path)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))