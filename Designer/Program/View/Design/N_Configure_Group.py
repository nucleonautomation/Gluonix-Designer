################################################################################################################################
#Configure_Circle
################################################################################################################################
import inspect

class Configure_Group:
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
            self.Frame.Config(Resize=True, Move=True)
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
            
            #Visibilty
            Fixture = self.Frame.Locate(7, 5, 90, 2)
            self.Visibilty_Image = {True: 'Visibilty_On', False: 'Visibilty_Off'}
            self.Visibilty = self.Global['Gluonix'].Image(self.Frame)
            self.Visibilty.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Visibilty.Config(Border_Size=0, Path=self.Global['Image'](self.Visibilty_Image[True]))
            self.Visibilty.Bind(On_Click=lambda E: self.Update_Visibilty())
            self.Visibilty.Create()
            
            #Move Label
            Fixture = self.Frame.Locate(25, 5, 3, 9)
            self.Move_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Move_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Move_Label.Config(Foreground='#000000', Value="Relative Move", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Move_Label.Create()
            
            #Left Label
            Fixture = self.Frame.Locate(25, 5, 3, 16)
            self.Left_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Left_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Left_Label.Config(Foreground='#000000', Value="Left:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Left_Label.Create()
            
            #Left Entry
            Fixture = self.Frame.Locate(40, 5, 28, 16)
            self.Left_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Left_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Left_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Left_Entry.Bind(On_Key_Release=lambda E: self.Check_Left())
            self.Left_Entry.Create()
            
            #Top Label
            Fixture = self.Frame.Locate(25, 5, 3, 23)
            self.Top_Label = self.Global['Gluonix'].Label(self.Frame)
            self.Top_Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Top_Label.Config(Foreground='#000000', Value="Top:", Font_Size=10, Font_Weight='normal', Align='w', Border_Size=0)
            self.Top_Label.Create()
            
            #Top Entry
            Fixture = self.Frame.Locate(40, 5, 28, 23)
            self.Top_Entry = self.Global['Gluonix'].Entry(self.Frame)
            self.Top_Entry.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Top_Entry.Config(Background='#FFFFFF', Foreground='#000000', Font_Size=9, Font_Weight='normal', Align='center', Border_Size=1)
            self.Top_Entry.Bind(On_Key_Release=lambda E: self.Check_Top())
            self.Top_Entry.Create()
            
            #Move Button
            Fixture = self.Frame.Locate(40, 5, 28, 30)
            self.Move_Button = self.Global['Gluonix'].Label(self.Frame)
            self.Move_Button.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Move_Button.Config(Background='#e1e1e1', Foreground='black', Value='Move', Font_Size=12, Font_Weight='normal', Border_Size=1, Border_Color='#adadad')
            self.Move_Button.Bind(On_Hover_In=lambda E: self.Move_Button.Config(Border_Color='#0078d7', Background='#d5dcf0'))
            self.Move_Button.Bind(On_Hover_Out=lambda E: self.Move_Button.Config(Border_Color='#adadad', Background='#e1e1e1'))
            self.Move_Button.Bind(On_Click=lambda E: self.Move())
            self.Move_Button.Create()
            
            #Update Scroll
            self.Frame.Update(self.Visibilty)
            
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Load(self, ID=False):
        try:
            if ID!=self.ID:
                self.Root = False
                self.Root_ID = False
                self.Element = False
                self.ID = ID
                Widget_Data = self.Configure.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{self.ID}'", Keys=True)
                if len(Widget_Data)==1:
                    Widget_Data = Widget_Data[0]
                    self.Root_ID = Widget_Data['Root']
                    self.Name_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Left_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Top_Entry.Config(Border_Color='#000000', Border_Size=1)
                    self.Name_Entry.Set(Widget_Data['Name'])
                    self.Left_Entry.Set(0)
                    self.Top_Entry.Set(0)
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
                    self.Visibilty.Set(self.Global['Image'](self.Visibilty_Image[self.Element._Display]))
                    if self.Element._Display:
                        self.Element.Show()
                else:
                    self.Global['Message'].Show('Error', 'Project Files Corrupted\nReopen Project')
            else:
                self.Element.Show()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        self.Global['Loading'].Hide()
            
    def Update_Name(self):
        try:
            Name = self.Name_Entry.Get()
            TempName = self.Configure.Design.Database.Get(f"SELECT * FROM `Frame` WHERE (`ID`!='{self.ID}' AND `Root`='{self.Root_ID}' AND `Name`='{Name}')")
            if self.Global['Custom'].Valid_Variable(Name) and len(TempName)==0:
                self.Configure.Design.Database.Post(f"UPDATE `Frame` SET `Name`='{Name}' WHERE `ID`='{self.ID}'")
                self.Configure.Design.Element.Tree.Edit(Name=f'  {Name}')
                self.Name_Entry.Config(Border_Color='#000000', Border_Size=1)
            else:
                self.Name_Entry.Config(Border_Color='red', Border_Size=1)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Visibilty(self):
        try:
            if self.Element:
                if self.Element._Display:
                    self.Element.Hide()
                else:
                    self.Element.Show()
                self.Visibilty.Set(self.Global['Image'](self.Visibilty_Image[self.Element._Display]))
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Check_Left(self):
        try:
            Left = self.Left_Entry.Get()
            if self.Global['Custom'].Is_Float(Left):
                self.Left_Entry.Config(Border_Color='#000000', Border_Size=1)
                return True
            else:
                self.Left_Entry.Config(Border_Color='red', Border_Size=1)
                return False
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Check_Top(self):
        try:
            Top = self.Top_Entry.Get()
            if self.Global['Custom'].Is_Float(Top):
                self.Top_Entry.Config(Border_Color='#000000', Border_Size=1)
                return True
            else:
                self.Top_Entry.Config(Border_Color='red', Border_Size=1)
                return False
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Update_Move(self, ID, Left, Top):
        try:
            Widgets = self.Configure.Design.Database.Get(f"SELECT * FROM `Item` WHERE `Root`='{ID}'", Keys=True)
            for Widget in Widgets:
                self.Configure.Design.Database.Post(f"UPDATE `Item` SET Left={Widget['Left']+Left}, Top={Widget['Top']+Top} WHERE `ID`='{Widget['ID']}'")
            Widgets = self.Configure.Design.Database.Get(f"SELECT * FROM `Widget` WHERE `Root`='{ID}'", Keys=True)
            for Widget in Widgets:
                self.Configure.Design.Database.Post(f"UPDATE `Widget` SET Left={Widget['Left']+Left}, Top={Widget['Top']+Top} WHERE `ID`='{Widget['ID']}'")
            Widgets = self.Configure.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `Root`='{ID}'", Keys=True)
            for Widget in Widgets:
                self.Configure.Design.Database.Post(f"UPDATE `Frame` SET Left={Widget['Left']+Left}, Top={Widget['Top']+Top} WHERE `ID`='{Widget['ID']}'")
                if Widget['Type']=='Group':
                    self.Update_Move(Widget['ID'], Left, Top)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Move(self):
        try:
            if self.Element:
                if self.Check_Left() and self.Check_Top():
                    Left = float(self.Left_Entry.Get())
                    Top = float(self.Top_Entry.Get())
                    self.Element.Move(Left, Top)
                    self.Left_Entry.Set(0)
                    self.Top_Entry.Set(0)
                    self.Update_Move(self.ID, Left, Top)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))