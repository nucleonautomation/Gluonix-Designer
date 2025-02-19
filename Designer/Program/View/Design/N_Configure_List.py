################################################################################################################################
#Configure_List
################################################################################################################################
import inspect
from tkinter import colorchooser

class Configure_List:
    def __init__(self, Global, Configure):
        try:
            self.Global = Global
            self.Configure = Configure
            self.Widget = []
            self.ID = False
            self.Root = False
            self.Root_ID = False
            self.Element = False
            
            #Frame
            Fixture = self.Configure.Frame.Locate(100, 95, 0, 5)
            self.Frame = self.Global['Gluonix'].Scroll(self.Configure.Frame)
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Background='#FFFFFF', Border_Size=0, Display=False)
            self.Frame.Config(Resize=False, Move=False)
            self.Frame.Create()
            self.Configure.Widget.append(self)
            
            #Name Label
            Fixture = self.Frame.Locate(25, 5, 3, 2)
            self.Name_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Name_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Name_Label.Config(Foreground='#000000', Value="Name:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Name_Label.Create()
            
            #Name Entry
            Fixture = self.Frame.Locate(60, 5, 28, 2)
            self.Name_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Name_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Name_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='left', Border_Size=1)
            self.Name_Entry.Bind(On_Key_Release=lambda E: self.Update_Name())
            self.Name_Entry.Create()
            
            #Background Label
            Fixture = self.Frame.Locate(25, 5, 3, 9)
            self.Background_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Background_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Background_Label.Config(Foreground='#000000', Value="Background:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Background_Label.Create()
            
            #Background Color
            Fixture = self.Frame.Locate(7, 5, 28, 9)
            self.Background_Color = self.Global['Gluonix'].Label(self.Frame)
            self.Background_Color.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Background_Color.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='w', Border_Size=1)
            self.Background_Color.Bind(On_Click=lambda E: self.Select_Color(self.Background_Color))
            self.Background_Color.Bind(On_Change=lambda : self.Update_Background())
            self.Background_Color.Create()
            
            #Background Check
            Fixture = self.Frame.Locate(7, 5, 37, 9)
            self.Background_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Background_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Background_Check.Config(Border_Size=0)
            self.Background_Check.Bind(On_Change=lambda : self.Update_Background())
            self.Background_Check.Create()
            
            #Foreground Label
            Fixture = self.Frame.Locate(25, 5, 53, 9)
            self.Foreground_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Foreground_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Foreground_Label.Config(Foreground='#000000', Value="Foreground:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Foreground_Label.Create()
            
            #Foreground Color
            Fixture = self.Frame.Locate(7, 5, 78, 9)
            self.Foreground_Color = self.Global['Gluonix'].Label(self.Frame)
            self.Foreground_Color.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Foreground_Color.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='w', Border_Size=1)
            self.Foreground_Color.Bind(On_Click=lambda E: self.Select_Color(self.Foreground_Color))
            self.Foreground_Color.Bind(On_Change=lambda : self.Update_Foreground())
            self.Foreground_Color.Create()
            
            #Border Color Label
            Fixture = self.Frame.Locate(25, 5, 3, 16)
            self.Border_Color_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Border_Color_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Border_Color_Label.Config(Foreground='#000000', Value="Border Color:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Border_Color_Label.Create()
            
            #Border Color
            Fixture = self.Frame.Locate(7, 5, 28, 16)
            self.Border_Color = self.Global['Gluonix'].Label(self.Frame)
            self.Border_Color.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Border_Color.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='w', Border_Size=1)
            self.Border_Color.Bind(On_Click=lambda E: self.Select_Color(self.Border_Color))
            self.Border_Color.Bind(On_Change=lambda : self.Update_Border_Color())
            self.Border_Color.Create()
            
            #Border_Size Label
            Fixture = self.Frame.Locate(25, 5, 3, 23)
            self.Border_Size_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Border_Size_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Border_Size_Label.Config(Foreground='#000000', Value="Border Size:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Border_Size_Label.Create()
            
            #Border_Size Entry
            Fixture = self.Frame.Locate(40, 5, 28, 23)
            self.Border_Size_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Border_Size_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Border_Size_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Border_Size_Entry.Bind(On_Key_Release=lambda E: self.Update_Border_Size())
            self.Border_Size_Entry.Create()
            
            #Alignment Label
            Fixture = self.Frame.Locate(25, 5, 3, 30)
            self.Alignment_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Alignment_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Alignment_Label.Config(Foreground='#000000', Value="Alignment:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Alignment_Label.Create()
            
            #Alignment Select
            Fixture = self.Frame.Locate(40, 5, 28, 30)
            self.Alignment_Select = self.Global['Gluonix'].Select(self.Frame)
            self.Alignment_Select.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Alignment_Select.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Alignment_Select.Add('Percentage')
            self.Alignment_Select.Add('Pixel')
            self.Alignment_Select.Bind(On_Change=lambda E: self.Update_Alignment())
            self.Alignment_Select.Create()
            
            #Alignment Lock
            Fixture = self.Frame.Locate(7, 5, 70, 30)
            self.Lock = False
            self.Lock_Image = {True: 'Lock_Closed', False: 'Lock_Open'}
            self.Alignment_Lock = self.Global['Gluonix'].Image(self.Frame)
            self.Alignment_Lock.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Alignment_Lock.Config(Border_Size=0)
            self.Alignment_Lock.Bind(On_Click=lambda E: self.Update_Lock())
            self.Alignment_Lock.Create()
            
            #Width Label
            Fixture = self.Frame.Locate(25, 5, 3, 37)
            self.Width_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Width_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Width_Label.Config(Foreground='#000000', Value="Width:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Width_Label.Create()
            
            #Width Entry
            Fixture = self.Frame.Locate(40, 5, 28, 37)
            self.Width_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Width_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Width_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Width_Entry.Bind(On_Key_Release=lambda E: self.Update_Width())
            self.Width_Entry.Create()
            
            #Height Label
            Fixture = self.Frame.Locate(25, 5, 3, 44)
            self.Height_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Height_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Height_Label.Config(Foreground='#000000', Value="Height:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Height_Label.Create()
            
            #Height Entry
            Fixture = self.Frame.Locate(40, 5, 28, 44)
            self.Height_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Height_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Height_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Height_Entry.Bind(On_Key_Release=lambda E: self.Update_Height())
            self.Height_Entry.Create()
            
            #Left Label
            Fixture = self.Frame.Locate(25, 5, 3, 51)
            self.Left_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Left_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Left_Label.Config(Foreground='#000000', Value="Left:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Left_Label.Create()
            
            #Left Entry
            Fixture = self.Frame.Locate(40, 5, 28, 51)
            self.Left_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Left_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Left_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Left_Entry.Bind(On_Key_Release=lambda E: self.Update_Left())
            self.Left_Entry.Create()
            
            #Top Label
            Fixture = self.Frame.Locate(25, 5, 3, 58)
            self.Top_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Top_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Top_Label.Config(Foreground='#000000', Value="Top:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Top_Label.Create()
            
            #Top Entry
            Fixture = self.Frame.Locate(40, 5, 28, 58)
            self.Top_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Top_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Top_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Top_Entry.Bind(On_Key_Release=lambda E: self.Update_Top())
            self.Top_Entry.Create()
            
            #Display Label
            Fixture = self.Frame.Locate(25, 5, 3, 65)
            self.Display_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Display_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Display_Label.Config(Foreground='#000000', Value="Display:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Display_Label.Create()
            
            #Display Check
            Fixture = self.Frame.Locate(7, 5, 27.7, 65)
            self.Display_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Display_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Display_Check.Config(Border_Size=0)
            self.Display_Check.Bind(On_Change=lambda : self.Update_Display())
            self.Display_Check.Create()
            
            #Resize Width Label
            Fixture = self.Frame.Locate(25, 5, 3, 72)
            self.Resize_Width_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Resize_Width_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Resize_Width_Label.Config(Foreground='#000000', Value="Resize Width:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Resize_Width_Label.Create()
            
            #Resize Width Check
            Fixture = self.Frame.Locate(7, 5, 27.7, 72)
            self.Resize_Width_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Resize_Width_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Resize_Width_Check.Config(Border_Size=0)
            self.Resize_Width_Check.Bind(On_Change=lambda : self.Update_Resize_Width())
            self.Resize_Width_Check.Create()
            
            #Resize Height Label
            Fixture = self.Frame.Locate(25, 5, 3, 79)
            self.Resize_Height_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Resize_Height_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Resize_Height_Label.Config(Foreground='#000000', Value="Resize Height:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Resize_Height_Label.Create()
            
            #Resize Height Check
            Fixture = self.Frame.Locate(7, 5, 27.7, 79)
            self.Resize_Height_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Resize_Height_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Resize_Height_Check.Config(Border_Size=0)
            self.Resize_Height_Check.Bind(On_Change=lambda : self.Update_Resize_Height())
            self.Resize_Height_Check.Create()
            
            #Move Left Label
            Fixture = self.Frame.Locate(25, 5, 3, 86)
            self.Move_Left_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Move_Left_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Move_Left_Label.Config(Foreground='#000000', Value="Move Left:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Move_Left_Label.Create()
            
            #Move Left Check
            Fixture = self.Frame.Locate(7, 5, 27.7, 86)
            self.Move_Left_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Move_Left_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Move_Left_Check.Config(Border_Size=0)
            self.Move_Left_Check.Bind(On_Change=lambda : self.Update_Move_Left())
            self.Move_Left_Check.Create()
            
            #Move Top Label
            Fixture = self.Frame.Locate(25, 5, 3, 93)
            self.Move_Top_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Move_Top_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Move_Top_Label.Config(Foreground='#000000', Value="Move Top:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Move_Top_Label.Create()
            
            #Move Top Check
            Fixture = self.Frame.Locate(7, 5, 27.7, 93)
            self.Move_Top_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Move_Top_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Move_Top_Check.Config(Border_Size=0)
            self.Move_Top_Check.Bind(On_Change=lambda : self.Update_Move_Top())
            self.Move_Top_Check.Create()
            
            #Anchor Label
            Fixture = self.Frame.Locate(25, 5, 3, 99)
            self.Anchor_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Anchor_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Anchor_Label.Config(Foreground='#000000', Value="Anchor:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Anchor_Label.Create()
            
            #Anchor Select
            Fixture = self.Frame.Locate(40, 5, 28, 99)
            self.Anchor_Select = self.Global['Gluonix'].Select(self.Frame)
            self.Anchor_Select.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Anchor_Select.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Anchor_Select.Add('center')
            self.Anchor_Select.Add('left')
            self.Anchor_Select.Add('right')
            self.Anchor_Select.Bind(On_Change=lambda E: self.Update_Anchor())
            self.Anchor_Select.Create()
            
            #Font Size Label
            Fixture = self.Frame.Locate(25, 5, 3, 106)
            self.Font_Size_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Font_Size_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Font_Size_Label.Config(Foreground='#000000', Value="Font Size:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Font_Size_Label.Create()
            
            #Font Size Entry
            Fixture = self.Frame.Locate(40, 5, 28, 106)
            self.Font_Size_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Font_Size_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Font_Size_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Font_Size_Entry.Bind(On_Key_Release=lambda E: self.Update_Font_Size())
            self.Font_Size_Entry.Create()
            
            #Font Weight Label
            Fixture = self.Frame.Locate(25, 5, 3, 113)
            self.Font_Weight_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Font_Weight_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Font_Weight_Label.Config(Foreground='#000000', Value="Font Weight:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Font_Weight_Label.Create()
            
            #Font Weight Select
            Fixture = self.Frame.Locate(40, 5, 28, 113)
            self.Font_Weight_Select = self.Global['Gluonix'].Select(self.Frame)
            self.Font_Weight_Select.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Font_Weight_Select.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Font_Weight_Select.Add('normal')
            self.Font_Weight_Select.Add('bold')
            self.Font_Weight_Select.Bind(On_Change=lambda E: self.Update_Font_Weight())
            self.Font_Weight_Select.Create()
            
            #Font Family Label
            Fixture = self.Frame.Locate(25, 5, 3, 120)
            self.Font_Family_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Font_Family_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Font_Family_Label.Config(Foreground='#000000', Value="Font Family:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Font_Family_Label.Create()
            
            #Font Family Select
            Fixture = self.Frame.Locate(40, 5, 28, 120)
            self.Font_Family_Select = self.Global['Gluonix'].Select(self.Frame)
            self.Font_Family_Select.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Font_Family_Select.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Font_Family_Select.Add('Arial')
            self.Font_Family_Select.Add('Courier')
            self.Font_Family_Select.Add('Courier New')
            self.Font_Family_Select.Add('Georgia')
            self.Font_Family_Select.Add('Lucida Console')
            self.Font_Family_Select.Add('Symbol')
            self.Font_Family_Select.Add('Times New Roman')
            self.Font_Family_Select.Add('Verdana')
            self.Font_Family_Select.Add('Comic Sans MS')
            self.Font_Family_Select.Add('Helvetica')
            self.Font_Family_Select.Bind(On_Change=lambda E: self.Update_Font_Family())
            self.Font_Family_Select.Create()
            
            #Update Scroll
            self.Frame.Update(self.Font_Family_Select)
            
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Load(self, ID=False):
        try:
            if ID!=self.ID:
                self.Root = False
                self.Root_ID = False
                self.Element = False
                self.ID = ID
                Widget_Data = self.Configure.Design.Database.Get(f"SELECT * FROM `Widget` WHERE `ID`='{self.ID}'", Keys=True)
                if len(Widget_Data)==1:
                    Widget_Data = Widget_Data[0]
                    self.Root_ID = Widget_Data['Root']
                    self.Name_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Border_Size_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Width_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Height_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Left_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Top_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Name_Label.Set(Widget_Data['Type'])
                    self.Name_Entry.Set(Widget_Data['Name'])
                    if Widget_Data['Background']=='False':
                        self.Background_Check.Set(False)
                    else:
                        self.Background_Check.Set(True)
                        self.Background_Color.Config(Background=Widget_Data['Background'])
                    self.Foreground_Color.Config(Background=Widget_Data['Foreground'])
                    self.Border_Color.Config(Background=Widget_Data['Border_Color'])
                    self.Border_Size_Entry.Set(Widget_Data['Border_Size'])
                    self.Alignment_Select.Set(Widget_Data['Alignment'])
                    self.Lock = bool(Widget_Data['Lock'])
                    self.Alignment_Lock.Set(self.Global['Image'](self.Lock_Image[self.Lock]))
                    self.Width_Entry.Set(Widget_Data['Width'])
                    self.Height_Entry.Set(Widget_Data['Height'])
                    self.Left_Entry.Set(Widget_Data['Left'])
                    self.Top_Entry.Set(Widget_Data['Top'])
                    self.Display_Check.Set(bool(Widget_Data['Display']))
                    self.Resize_Width_Check.Set(bool(Widget_Data['Resize_Width']))
                    self.Resize_Height_Check.Set(bool(Widget_Data['Resize_Height']))
                    self.Move_Left_Check.Set(bool(Widget_Data['Move_Left']))
                    self.Move_Top_Check.Set(bool(Widget_Data['Move_Top']))
                    self.Anchor_Select.Set(Widget_Data['Align'])
                    self.Font_Weight_Select.Set(Widget_Data['Font_Weight'])
                    self.Font_Size_Entry.Set(Widget_Data['Font_Size'])
                    self.Font_Family_Select.Set(Widget_Data['Font_Family'])
                    self.Configure.Hide_All()
                    self.Configure.Current = self
                    self.Frame.Show()
                    Temp_Root = Widget_Data['Root']
                    Root = Temp_Root
                    while Temp_Root!='Root':
                        Widget_Data = self.Configure.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Temp_Root}'", Keys=True)
                        if len(Widget_Data)==1:
                            Widget_Data = Widget_Data[0]
                            Temp_Root = Widget_Data['Root']
                            Root = Temp_Root+'.'+Root
                        else:
                            break
                    Root_Split = Root.split('.')
                    Current = ''
                    for Each in Root_Split:
                        if Current:
                            Current = Current+'.'+Each
                        else:
                            Current = Each
                        if Current!='Root':
                            Temp_Root = self.Global['Custom'].Get_Attr_Class(self.Configure.Design, Current)
                            Temp_Root.Show()
                    self.Root = self.Global['Custom'].Get_Attr_Class(self.Configure.Design, Root)
                    self.Element = getattr(self.Root, self.ID)
                    self.Element.Show()
                else:
                    self.Global['Message'].Show('Error', 'Project Files Corrupted\nReopen Project')
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        self.Global['Loading'].Hide()
            
    def Movement_Update(self):
        try:
            if self.ID:
                Widget_Data = self.Configure.Design.Database.Get(f"SELECT * FROM `Widget` WHERE `ID`='{self.ID}'", Keys=True)
                Widget_Data = Widget_Data[0]
                self.Width_Entry.Set(Widget_Data['Width'])
                self.Height_Entry.Set(Widget_Data['Height'])
                self.Left_Entry.Set(Widget_Data['Left'])
                self.Top_Entry.Set(Widget_Data['Top'])
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Select_Color(self, Element):
        try:
            Color = colorchooser.askcolor(color=Element.Config_Get('Background')['Background'], title ="Choose Background Color")[1]
            if Color is not None:
                Element.Config(Background=Color)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Name(self):
        try:
            Name = self.Name_Entry.Get()
            TempName = self.Configure.Design.Database.Get(f"SELECT * FROM `Widget` WHERE (`ID`!='{self.ID}' AND `Root`=='{self.Root_ID}' AND `Name`='{Name}')")
            if self.Global['Custom'].Valid_Variable(Name) and len(TempName)==0:
                self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Name`='{Name}' WHERE `ID`='{self.ID}'")
                self.Configure.Design.Element.Tree.Edit(Name=f' {Name}')
                self.Name_Entry.Config(Border_Color='#000000', Border_Size=1)
            else:
                self.Name_Entry.Config(Border_Color='red', Border_Size=2)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Background(self):
        try:
            if self.Background_Check.Get():
                Background = self.Background_Color.Config_Get('Background')['Background']
                self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Background`='{Background}' WHERE `ID`='{self.ID}'")
                if self.Element:
                    self.Element.Config(Background=Background)
            else:
                self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Background`='False' WHERE `ID`='{self.ID}'")
                if self.Element:
                    self.Element.Config(Background=False)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Foreground(self):
        try:
            Foreground = self.Foreground_Color.Config_Get('Background')['Background']
            self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Foreground`='{Foreground}' WHERE `ID`='{self.ID}'")
            if self.Element:
                self.Element.Config(Foreground=Foreground)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Border_Color(self):
        try:
            Border_Color = self.Border_Color.Config_Get('Background')['Background']
            self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Border_Color`='{Border_Color}' WHERE `ID`='{self.ID}'")
            if self.Element:
                self.Element.Config(Border_Color=Border_Color)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Border_Size(self):
        try:
            Border_Size = self.Border_Size_Entry.Get()
            if Border_Size.isdigit():
                Border_Size = int(Border_Size)
                self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Border_Size`='{Border_Size}' WHERE `ID`='{self.ID}'")
                self.Border_Size_Entry.Config(Border_Color='#000000', Border_Size=1)
                if self.Element:
                    self.Element.Config(Border_Size=Border_Size)
            else:
                self.Border_Size_Entry.Config(Border_Color='red', Border_Size=2)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Alignment(self):
        try:
            Alignment = self.Alignment_Select.Get()
            self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Alignment`='{Alignment}' WHERE `ID`='{self.ID}'")
            if self.Element:
                Width = float(self.Width_Entry.Get())
                Height = float(self.Height_Entry.Get())
                Left = float(self.Left_Entry.Get())
                Top = float(self.Top_Entry.Get())
                if Alignment=='Percentage':
                    Fixture = self.Root.Locate(Width, Height, Left, Top)
                else:
                    Fixture = [Width, Height, Left, Top]
                self.Element.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Lock(self):
        try:
            self.Lock = not self.Lock
            self.Alignment_Lock.Set(self.Global['Image'](self.Lock_Image[self.Lock]))
            self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Lock`='{int(self.Lock)}' WHERE `ID`='{self.ID}'")
            if self.Element:
                self.Element.Lock = self.Lock
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Width(self):
        try:
            Width = self.Width_Entry.Get()
            if self.Global['Custom'].Is_Float(Width):
                Width = float(Width)
                self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Width`='{Width}' WHERE `ID`='{self.ID}'")
                self.Width_Entry.Config(Border_Color='#000000', Border_Size=1)
                if self.Element:
                    if self.Alignment_Select.Get()=='Percentage':
                        Fixture = self.Root.Locate(Width, 0, 0, 0)
                    else:
                        Fixture = [Width, 0, 0, 0]
                    self.Element.Config(Width=Fixture[0])
            else:
                self.Width_Entry.Config(Border_Color='red', Border_Size=2)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Height(self):
        try:
            Height = self.Height_Entry.Get()
            if self.Global['Custom'].Is_Float(Height):
                Height = float(Height)
                self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Height`='{Height}' WHERE `ID`='{self.ID}'")
                self.Height_Entry.Config(Border_Color='#000000', Border_Size=1)
                if self.Element:
                    if self.Alignment_Select.Get()=='Percentage':
                        Fixture = self.Root.Locate(0, Height, 0, 0)
                    else:
                        Fixture = [0, Height, 0, 0]
                    self.Element.Config(Height=Fixture[1])
            else:
                self.Height_Entry.Config(Border_Color='red', Border_Size=2)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Left(self):
        try:
            Left = self.Left_Entry.Get()
            if self.Global['Custom'].Is_Float(Left):
                Left = float(Left)
                self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Left`='{Left}' WHERE `ID`='{self.ID}'")
                self.Left_Entry.Config(Border_Color='#000000', Border_Size=1)
                if self.Element:
                    if self.Alignment_Select.Get()=='Percentage':
                        Fixture = self.Root.Locate(0, 0, Left, 0)
                    else:
                        Fixture = [0, 0, Left, 0]
                    self.Element.Config(Left=Fixture[2])
            else:
                self.Left_Entry.Config(Border_Color='red', Border_Size=2)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Top(self):
        try:
            Top = self.Top_Entry.Get()
            if self.Global['Custom'].Is_Float(Top):
                Top = float(Top)
                self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Top`='{Top}' WHERE `ID`='{self.ID}'")
                self.Top_Entry.Config(Border_Color='#000000', Border_Size=1)
                if self.Element:
                    if self.Alignment_Select.Get()=='Percentage':
                        Fixture = self.Root.Locate(0, 0, 0, Top)
                    else:
                        Fixture = [0, 0, 0, Top]
                    self.Element.Config(Top=Fixture[3])
            else:
                self.Top_Entry.Config(Border_Color='red', Border_Size=2)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Display(self):
        try:
            Display = self.Display_Check.Get()
            self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Display`='{int(Display)}' WHERE `ID`='{self.ID}'")
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Resize_Width(self):
        try:
            Resize_Width = self.Resize_Width_Check.Get()
            self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Resize_Width`='{int(Resize_Width)}' WHERE `ID`='{self.ID}'")
            if self.Element:
                self.Element.Config(Resize_Width=Resize_Width)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Resize_Height(self):
        try:
            Resize_Height = self.Resize_Height_Check.Get()
            self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Resize_Height`='{int(Resize_Height)}' WHERE `ID`='{self.ID}'")
            if self.Element:
                self.Element.Config(Resize_Height=Resize_Height)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Move_Left(self):
        try:
            Move_Left = self.Move_Left_Check.Get()
            self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Move_Left`='{int(Move_Left)}' WHERE `ID`='{self.ID}'")
            if self.Element:
                self.Element.Config(Move_Left=Move_Left)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Move_Top(self):
        try:
            Move_Top = self.Move_Top_Check.Get()
            self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Move_Top`='{int(Move_Top)}' WHERE `ID`='{self.ID}'")
            if self.Element:
                self.Element.Config(Move_Top=Move_Top)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Anchor(self):
        try:
            Anchor = self.Anchor_Select.Get()
            self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Align`='{Anchor}' WHERE `ID`='{self.ID}'")
            self.Element.Config(Align=Anchor)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Font_Weight(self):
        try:
            Font_Weight = self.Font_Weight_Select.Get()
            self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Font_Weight`='{Font_Weight}' WHERE `ID`='{self.ID}'")
            self.Element.Config(Font_Weight=Font_Weight)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Font_Size(self):
        try:
            Font_Size = self.Font_Size_Entry.Get()
            if Font_Size.isdigit():
                Font_Size = int(Font_Size)
                self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Font_Size`='{Font_Size}' WHERE `ID`='{self.ID}'")
                self.Font_Size_Entry.Config(Border_Color='#000000', Border_Size=1)
                if self.Element:
                    self.Element.Config(Font_Size=Font_Size)
            else:
                self.Font_Size_Entry.Config(Border_Color='red', Border_Size=2)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Font_Family(self):
        try:
            Font_Family = self.Font_Family_Select.Get()
            self.Configure.Design.Database.Post(f"UPDATE `Widget` SET `Font_Family`='{Font_Family}' WHERE `ID`='{self.ID}'")
            self.Element.Config(Font_Family=Font_Family)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))