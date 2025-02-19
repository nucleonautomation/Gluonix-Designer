################################################################################################################################
#Configure_Text
################################################################################################################################
import inspect
from tkinter import colorchooser

class Configure_Canvas_Text:
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
            
            #Color Label
            Fixture = self.Frame.Locate(25, 5, 3, 9)
            self.Color_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Color_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Color_Label.Config(Foreground='#000000', Value="Color:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Color_Label.Create()
            
            #Color Color
            Fixture = self.Frame.Locate(7, 5, 28, 9)
            self.Color_Color = self.Global['Gluonix'].Label(self.Frame)
            self.Color_Color.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Color_Color.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='w', Border_Size=1)
            self.Color_Color.Bind(On_Click=lambda E: self.Select_Color(self.Color_Color))
            self.Color_Color.Bind(On_Change=lambda : self.Update_Color())
            self.Color_Color.Create()
            
            #Alignment Lock
            Fixture = self.Frame.Locate(7, 5, 37, 9)
            self.Lock = False
            self.Lock_Image = {True: 'Lock_Closed', False: 'Lock_Open'}
            self.Alignment_Lock = self.Global['Gluonix'].Image(self.Frame)
            self.Alignment_Lock.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Alignment_Lock.Config(Border_Size=0)
            self.Alignment_Lock.Bind(On_Click=lambda E: self.Update_Lock())
            self.Alignment_Lock.Create()
            
            #Thickness Label
            Fixture = self.Frame.Locate(25, 5, 3, 16)
            self.Thickness_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Thickness_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Thickness_Label.Config(Foreground='#000000', Value="Thickness:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Thickness_Label.Create()
            
            #Thickness Entry
            Fixture = self.Frame.Locate(40, 5, 28, 16)
            self.Thickness_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Thickness_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Thickness_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Thickness_Entry.Bind(On_Key_Release=lambda E: self.Update_Thickness())
            self.Thickness_Entry.Create()
            
            #Width Label
            Fixture = self.Frame.Locate(25, 5, 3, 23)
            self.Width_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Width_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Width_Label.Config(Foreground='#000000', Value="Width:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Width_Label.Create()
            
            #Width Entry
            Fixture = self.Frame.Locate(40, 5, 28, 23)
            self.Width_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Width_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Width_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Width_Entry.Bind(On_Key_Release=lambda E: self.Update_Width())
            self.Width_Entry.Create()
            
            #Height Label
            Fixture = self.Frame.Locate(25, 5, 3, 30)
            self.Height_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Height_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Height_Label.Config(Foreground='#000000', Value="Height:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Height_Label.Create()
            
            #Height Entry
            Fixture = self.Frame.Locate(40, 5, 28, 30)
            self.Height_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Height_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Height_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Height_Entry.Bind(On_Key_Release=lambda E: self.Update_Height())
            self.Height_Entry.Create()
            
            #Left Label
            Fixture = self.Frame.Locate(25, 5, 3, 37)
            self.Left_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Left_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Left_Label.Config(Foreground='#000000', Value="Left:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Left_Label.Create()
            
            #Left Entry
            Fixture = self.Frame.Locate(40, 5, 28, 37)
            self.Left_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Left_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Left_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Left_Entry.Bind(On_Key_Release=lambda E: self.Update_Left())
            self.Left_Entry.Create()
            
            #Top Label
            Fixture = self.Frame.Locate(25, 5, 3, 44)
            self.Top_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Top_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Top_Label.Config(Foreground='#000000', Value="Top:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Top_Label.Create()
            
            #Top Entry
            Fixture = self.Frame.Locate(40, 5, 28, 44)
            self.Top_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Top_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Top_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Top_Entry.Bind(On_Key_Release=lambda E: self.Update_Top())
            self.Top_Entry.Create()
            
            #Resize Label
            Fixture = self.Frame.Locate(25, 5, 3, 51)
            self.Resize_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Resize_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Resize_Label.Config(Foreground='#000000', Value="Resize Width:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Resize_Label.Create()
            
            #Resize Check
            Fixture = self.Frame.Locate(7, 5, 27.7, 51)
            self.Resize_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Resize_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Resize_Check.Config(Border_Size=0)
            self.Resize_Check.Bind(On_Change=lambda : self.Update_Resize())
            self.Resize_Check.Create()
            
            #Move Label
            Fixture = self.Frame.Locate(25, 5, 3, 58)
            self.Move_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Move_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Move_Label.Config(Foreground='#000000', Value="Move Left:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Move_Label.Create()
            
            #Move Check
            Fixture = self.Frame.Locate(7, 5, 27.7, 58)
            self.Move_Check = self.Global['Gluonix'].Check(self.Frame)
            self.Move_Check.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Move_Check.Config(Border_Size=0)
            self.Move_Check.Bind(On_Change=lambda : self.Update_Move())
            self.Move_Check.Create()
            
            #Value Label
            Fixture = self.Frame.Locate(25, 5, 3, 65)
            self.Value_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Value_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Value_Label.Config(Foreground='#000000', Value="Value:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Value_Label.Create()
            
            #Value Entry
            Fixture = self.Frame.Locate(60, 5, 28, 65)
            self.Value_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Value_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Value_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='left', Border_Size=1)
            self.Value_Entry.Bind(On_Key_Release=lambda E: self.Update_Value())
            self.Value_Entry.Create()
            
            #Size Label
            Fixture = self.Frame.Locate(25, 5, 3, 72)
            self.Size_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Size_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Size_Label.Config(Foreground='#000000', Value="Size:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Size_Label.Create()
            
            #Size Entry
            Fixture = self.Frame.Locate(40, 5, 28, 72)
            self.Size_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Size_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Size_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Size_Entry.Bind(On_Key_Release=lambda E: self.Update_Size())
            self.Size_Entry.Create()
            
            #Weight Label
            Fixture = self.Frame.Locate(25, 5, 3, 79)
            self.Weight_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Weight_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Weight_Label.Config(Foreground='#000000', Value="Weight:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Weight_Label.Create()
            
            #Weight Select
            Fixture = self.Frame.Locate(40, 5, 28, 79)
            self.Weight_Select = self.Global['Gluonix'].Select(self.Frame)
            self.Weight_Select.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Weight_Select.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Weight_Select.Add('normal')
            self.Weight_Select.Add('bold')
            self.Weight_Select.Bind(On_Change=lambda E: self.Update_Weight())
            self.Weight_Select.Create()
            
            #Font Label
            Fixture = self.Frame.Locate(25, 5, 3, 86)
            self.Font_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Font_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Font_Label.Config(Foreground='#000000', Value="Font:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Font_Label.Create()
            
            #Font Select
            Fixture = self.Frame.Locate(40, 5, 28, 86)
            self.Font_Select = self.Global['Gluonix'].Select(self.Frame)
            self.Font_Select.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Font_Select.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Font_Select.Add('Arial')
            self.Font_Select.Add('Courier')
            self.Font_Select.Add('Courier New')
            self.Font_Select.Add('Georgia')
            self.Font_Select.Add('Lucida Console')
            self.Font_Select.Add('Symbol')
            self.Font_Select.Add('Times New Roman')
            self.Font_Select.Add('Verdana')
            self.Font_Select.Add('Comic Sans MS')
            self.Font_Select.Add('Helvetica')
            self.Font_Select.Bind(On_Change=lambda E: self.Update_Font())
            self.Font_Select.Create()
            
            #Update Scroll
            self.Frame.Update(self.Font_Select)
            
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Load(self, ID=False):
        try:
            if ID!=self.ID:
                self.Root = False
                self.Root_ID = False
                self.Element = False
                self.ID = ID
                Widget_Data = self.Configure.Design.Database.Get(f"SELECT * FROM `Item` WHERE `ID`='{self.ID}'", Keys=True)
                if len(Widget_Data)==1:
                    Widget_Data = Widget_Data[0]
                    self.Root_ID = Widget_Data['Root']
                    self.Name_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Width_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Height_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Left_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Top_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Size_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Name_Label.Set(Widget_Data['Type'])
                    self.Name_Entry.Set(Widget_Data['Name'])
                    self.Color_Color.Config(Background=Widget_Data['Color'])
                    self.Lock = bool(Widget_Data['Lock'])
                    self.Alignment_Lock.Set(self.Global['Image'](self.Lock_Image[self.Lock]))
                    self.Thickness_Entry.Set(Widget_Data['Thickness'])
                    self.Width_Entry.Set(Widget_Data['Width'])
                    self.Height_Entry.Set(Widget_Data['Height'])
                    self.Left_Entry.Set(Widget_Data['Left'])
                    self.Top_Entry.Set(Widget_Data['Top'])
                    self.Resize_Check.Set(bool(Widget_Data['Resize']))
                    self.Move_Check.Set(bool(Widget_Data['Move']))
                    self.Value_Entry.Set(Widget_Data['Value'])
                    self.Weight_Select.Set(Widget_Data['Weight'])
                    self.Size_Entry.Set(Widget_Data['Size'])
                    self.Font_Select.Set(Widget_Data['Font'])
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
            else:
                self.Element.Show()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        self.Global['Loading'].Hide()
            
    def Movement_Update(self):
        try:
            if self.ID:
                Widget_Data = self.Configure.Design.Database.Get(f"SELECT * FROM `Item` WHERE `ID`='{self.ID}'", Keys=True)
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
            TempName = self.Configure.Design.Database.Get(f"SELECT * FROM `Item` WHERE (`ID`!='{self.ID}' AND `Root`=='{self.Root_ID}' AND `Name`='{Name}')")
            if self.Global['Custom'].Valid_Variable(Name) and len(TempName)==0:
                self.Configure.Design.Database.Post(f"UPDATE `Item` SET `Name`='{Name}' WHERE `ID`='{self.ID}'")
                self.Configure.Design.Element.Tree.Edit(Name=f' {Name}')
                self.Name_Entry.Config(Border_Color='#000000', Border_Size=1)
            else:
                self.Name_Entry.Config(Border_Color='red', Border_Size=2)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Color(self):
        try:
            Color = self.Color_Color.Config_Get('Background')['Background']
            self.Configure.Design.Database.Post(f"UPDATE `Item` SET `Color`='{Color}' WHERE `ID`='{self.ID}'")
            if self.Element:
                self.Element.Config(Color=Color)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Lock(self):
        try:
            self.Lock = not self.Lock
            self.Alignment_Lock.Set(self.Global['Image'](self.Lock_Image[self.Lock]))
            self.Configure.Design.Database.Post(f"UPDATE `Item` SET `Lock`='{int(self.Lock)}' WHERE `ID`='{self.ID}'")
            if self.Element:
                self.Element.Lock = self.Lock
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Thickness(self):
        try:
            Thickness = self.Thickness_Entry.Get()
            if self.Global['Custom'].Is_Float(Thickness):
                Thickness = float(Thickness)
                self.Configure.Design.Database.Post(f"UPDATE `Item` SET `Thickness`='{Thickness}' WHERE `ID`='{self.ID}'")
                self.Thickness_Entry.Config(Border_Color='#000000', Border_Size=1)
                if self.Element:
                    self.Element.Config(Thickness=Thickness)
            else:
                self.Thickness_Entry.Config(Border_Color='red', Border_Size=2)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Width(self):
        try:
            Width = self.Width_Entry.Get()
            if self.Global['Custom'].Is_Float(Width):
                Width = float(Width)
                self.Configure.Design.Database.Post(f"UPDATE `Item` SET `Width`='{Width}' WHERE `ID`='{self.ID}'")
                self.Width_Entry.Config(Border_Color='#000000', Border_Size=1)
                if self.Element:
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
                self.Configure.Design.Database.Post(f"UPDATE `Item` SET `Height`='{Height}' WHERE `ID`='{self.ID}'")
                self.Height_Entry.Config(Border_Color='#000000', Border_Size=1)
                if self.Element:
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
                self.Configure.Design.Database.Post(f"UPDATE `Item` SET `Left`='{Left}' WHERE `ID`='{self.ID}'")
                self.Left_Entry.Config(Border_Color='#000000', Border_Size=1)
                if self.Element:
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
                self.Configure.Design.Database.Post(f"UPDATE `Item` SET `Top`='{Top}' WHERE `ID`='{self.ID}'")
                self.Top_Entry.Config(Border_Color='#000000', Border_Size=1)
                if self.Element:
                    Fixture = [0, 0, 0, Top]
                    self.Element.Config(Top=Fixture[3])
            else:
                self.Top_Entry.Config(Border_Color='red', Border_Size=2)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Resize(self):
        try:
            Resize = self.Resize_Check.Get()
            self.Configure.Design.Database.Post(f"UPDATE `Item` SET `Resize`='{int(Resize)}' WHERE `ID`='{self.ID}'")
            if self.Element:
                self.Element.Config(Resize=Resize)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Move(self):
        try:
            Move = self.Move_Check.Get()
            self.Configure.Design.Database.Post(f"UPDATE `Item` SET `Move`='{int(Move)}' WHERE `ID`='{self.ID}'")
            if self.Element:
                self.Element.Config(Move=Move)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Value(self):
        try:
            Value = self.Value_Entry.Get()
            self.Configure.Design.Database.Post(f"UPDATE `Item` SET `Value`='{Value}' WHERE `ID`='{self.ID}'")
            self.Element.Set(Value)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Weight(self):
        try:
            Weight = self.Weight_Select.Get()
            self.Configure.Design.Database.Post(f"UPDATE `Item` SET `Weight`='{Weight}' WHERE `ID`='{self.ID}'")
            self.Element.Config(Weight=Weight)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Size(self):
        try:
            Size = self.Size_Entry.Get()
            if Size.isdigit():
                Size = int(Size)
                self.Configure.Design.Database.Post(f"UPDATE `Item` SET `Size`='{Size}' WHERE `ID`='{self.ID}'")
                self.Size_Entry.Config(Border_Color='#000000', Border_Size=1)
                if self.Element:
                    self.Element.Config(Size=Size)
            else:
                self.Size_Entry.Config(Border_Color='red', Border_Size=2)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Font(self):
        try:
            Font = self.Font_Select.Get()
            self.Configure.Design.Database.Post(f"UPDATE `Item` SET `Font`='{Font}' WHERE `ID`='{self.ID}'")
            self.Element.Config(Font=Font)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))