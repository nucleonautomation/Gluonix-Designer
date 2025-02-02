################################################################################################################################
#Element
################################################################################################################################
import inspect
import os
import shutil
import random
import string
import time
import traceback

class Element:
    def __init__(self, Global, Design):
        try:
            self.Global = Global
            self.Design = Design
            self.Widget = []
            self.Grid_Lock = True
            self.Copy_ID = False
            self.Current = False
            self.Dragging = False
            self.Current = False
            self._Coord = {'X': 0, 'Y': 0}
            self.Element_Fixture = {}
            
            #Frame
            Fixture = self.Design.Frame.Locate(29.5, 90, 30, 10)
            self.Frame = self.Global['Gluonix'].Frame(self.Design.Frame)
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Background='#FFFFFF', Border_Size=0, Display=True)
            self.Frame.Config(Resize=False, Move=False)
            self.Frame.Create()
            self.Design.Widget.append(self.Frame)
            
            #Label
            Fixture = self.Frame.Locate(30, 3, 0, 1)
            self.Label = self.Global['Gluonix'].Label(self.Frame)
            self.Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Label.Config(Background='#FFFFFF', Border_Size=0, Display=True)
            self.Label.Config(Foreground='#000000', Font_Size=16, Font_Weight='normal', Align='w')
            self.Label.Config(Resize=False, Move=False)
            self.Label.Set(' PROJECT')
            self.Label.Create()
            
            #Grid
            Fixture = self.Frame.Locate(10, 4.7, 30, 0)
            self.Grid_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Grid_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Grid_Image.Config(Path=self.Global['Image']('Grid_Lock'), Border_Size=0, Hand_Cursor=True, Display=True)
            self.Grid_Image.Bind(On_Click=lambda E: self.Grid())
            self.Grid_Image.Create()
            
            #Paste
            Fixture = self.Frame.Locate(10, 4.7, 60, 0)
            self.Paste_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Paste_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Paste_Image.Config(Path=self.Global['Image']('Paste'), Border_Size=0, Hand_Cursor=True, Display=False)
            self.Paste_Image.Bind(On_Click=lambda E: self.Paste())
            self.Paste_Image.Create()
            
            #Copy
            Fixture = self.Frame.Locate(10, 5, 70, 0)
            self.Copy_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Copy_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Copy_Image.Config(Path=self.Global['Image']('Copy'), Border_Size=0, Hand_Cursor=True, Display=True)
            self.Copy_Image.Bind(On_Click=lambda E: self.Copy())
            self.Copy_Image.Create()
            
            #Export
            Fixture = self.Frame.Locate(10, 3.8, 80, 0.5)
            self.Export_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Export_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Export_Image.Config(Path=self.Global['Image']('Export'), Border_Size=0, Hand_Cursor=True, Display=True)
            self.Export_Image.Bind(On_Click=lambda E: self.Export())
            self.Export_Image.Create()
            
            #Delete
            Fixture = self.Frame.Locate(10, 5, 90, 0)
            self.Delete_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Delete_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Delete_Image.Config(Path=self.Global['Image']('Delete'), Border_Size=0, Hand_Cursor=True, Display=True)
            self.Delete_Image.Bind(On_Click=lambda E: self.Show_Delete())
            self.Delete_Image.Create()
            
            #Delete Comfirm
            Fixture = self.Frame.Locate(10, 5, 79, 0)
            self.Delete_Confirm_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Delete_Confirm_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Delete_Confirm_Image.Config(Path=self.Global['Image']('Success'), Border_Size=0, Hand_Cursor=True, Display=False)
            self.Delete_Confirm_Image.Bind(On_Click=lambda E: self.Delete())
            self.Delete_Confirm_Image.Create()
            
            #Delete Cancel
            Fixture = self.Frame.Locate(10, 5, 90, 0)
            self.Delete_Cancel_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Delete_Cancel_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Delete_Cancel_Image.Config(Path=self.Global['Image']('Close'), Border_Size=0, Hand_Cursor=True, Display=False)
            self.Delete_Cancel_Image.Bind(On_Click=lambda E: self.Hide_Delete())
            self.Delete_Cancel_Image.Create()
            
            #Tree
            Fixture = self.Frame.Locate(100, 95, 0, 5)
            self.Tree = self.Global['Gluonix'].Tree(self.Frame)
            self.Tree.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Tree.Config(Background='#FFFFFF', Border_Size=0, Scroll_Width=Fixture[0]*3, Display=True)
            self.Tree.Config(Foreground='#000000', Font_Size=16, Font_Weight='normal')
            self.Tree.Config(Resize=False, Move=False)
            self.Tree.Bind(On_Release=lambda E: self.Reset_All(), On_Double_Click=lambda E: self.Get_Current(), On_Right_Click=lambda E: self.Get_Current())
            self.Tree.Create()
                   
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Load(self):
        try:
            self.Load_Child(self.Parent)
            self.Tree.Expand(getattr(self, self.Parent))
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Load_Child(self, Parent='Root'):
        try:
            Widgets = self.Design.Database.Get(f"SELECT * FROM `Widget` WHERE `Root`='{Parent}'", Keys=True)
            for Widget in Widgets:
                Stock = getattr(self.Design.Stock, f"Stock_{Widget['Type']}")
                Stock.Create(Widget['ID'])
                Root = getattr(self, Widget['Root'])
                Image = self.Global['Image'](Widget['Type'])
                setattr(self, Widget['ID'], self.Tree.Add(Name=Widget['Name'], Parent=Root, Value=[Widget['ID'], Widget['Type'], 0], Path=Image))
            Widgets = self.Design.Database.Get(f"SELECT * FROM `Item` WHERE `Root`='{Parent}'", Keys=True)
            for Widget in Widgets:
                Stock = getattr(self.Design.Stock, f"Stock_{Widget['Type']}")
                Stock.Create(Widget['ID'])
                Root = getattr(self, Widget['Root'])
                Image = self.Global['Image'](Widget['Type'])
                setattr(self, Widget['ID'], self.Tree.Add(Name=Widget['Name'], Parent=Root, Value=[Widget['ID'], Widget['Type'], 0], Path=Image))
            Widgets = self.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `Root`='{Parent}'", Keys=True)
            for Widget in Widgets:
                Stock = getattr(self.Design.Stock, f"Stock_{Widget['Type']}")
                Stock.Create(Widget['ID'])
                Root = getattr(self, Widget['Root'])
                Image = self.Global['Image'](Widget['Type'])
                setattr(self, Widget['ID'], self.Tree.Add(Name=Widget['Name'], Parent=Root, Value=[Widget['ID'], Widget['Type'], Widget['Level']], Path=Image))
                self.Load_Child(Widget['ID'])
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Intractive(self, Element):
        try:
            Element.Bind(On_Click=lambda E: self.Drag_Start(E, Element), On_Drag=lambda E: self.Drag(E, Element), On_Release=lambda E: self.Drag_Release(E, Element))
            Element.Bind(On_Right_Click=lambda E: self.Drag_Start_Size(E, Element), On_Right_Drag=lambda E: self.Drag_Size(E, Element), On_Right_Release=lambda E: self.Drag_Release(E, Element))
            Element.Bind(On_Double_Click=lambda E: self.Show_Current(Element))
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Drag_Release(self, E, Element):
        try:
            self.Dragging = False
            self.Current = False
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Drag_Start(self, E, Element):
        try:
            if not Element.Lock and not self.Dragging:
                self._Coord = {'X': 0, 'Y': 0}
                self._Coord['X'] = E.x_root
                self._Coord['Y'] = E.y_root
                self.Element_Fixture = Element.Config_Get('Left', 'Top')
                if self.Grid_Lock:
                    Temp_Root = getattr(self.Design, self.Design.Display_ID)
                    Window_Size = Temp_Root.Size()
                    self.Grid_Width = Window_Size[0]/100
                    self.Grid_Height = Window_Size[1]/100
                self.Dragging = True
                self.Current = Element._ID
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        self.Global['Loading'].Hide()
            
    def Drag(self, E, Element):
        try:
            if not Element.Lock and self.Dragging and self.Current==Element._ID and 'Left' in self.Element_Fixture and 'Top' in self.Element_Fixture:
                Difference_Left = (E.x_root - self._Coord['X'])
                Difference_Top = (E.y_root - self._Coord['Y'])
                New_Left = self.Element_Fixture['Left']+Difference_Left
                New_Top = self.Element_Fixture['Top']+Difference_Top
                if self.Grid_Lock:
                    New_Left = round(New_Left / self.Grid_Width)*self.Grid_Width
                    New_Top = round(New_Top / self.Grid_Height)*self.Grid_Height
                Element.Position(Left=New_Left, Top=New_Top)
                if Element._Type=='Frame' or Element._Type=='Canvas' or Element._Type=='Scroll' or Element._Type=='Popup':
                    Element_Type = 'Frame'
                elif 'Canvas_' in Element._Type:
                    Element_Type = 'Item'
                else:
                    Element_Type = 'Widget'
                Element_Data = self.Design.Database.Get(f"SELECT * FROM `{Element_Type}` WHERE `ID`='{Element._ID}'", Keys=True)
                Element_Data = Element_Data[0]
                if Element_Data['Alignment']=='Percentage':
                    Fixture_Reverse = Element._Main.Locate_Reverse(0, 0, New_Left, New_Top)
                else:
                    Fixture_Reverse = [0, 0, round(New_Left, 3), round(New_Top, 3)]
                self.Design.Database.Post(f"UPDATE `{Element_Type}` SET `Left`={Fixture_Reverse[2]}, `Top`={Fixture_Reverse[3]} WHERE `ID`='{Element._ID}'")
                if self.Design.Configure.Current:
                    self.Design.Configure.Current.Movement_Update()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Drag_Start_Size(self, E, Element):
        try:
            if not Element.Lock and not self.Dragging:
                self._Coord = {'X': 0, 'Y': 0}
                self._Coord['X'] = E.x_root
                self._Coord['Y'] = E.y_root
                self.Element_Fixture = Element.Config_Get('Width', 'Height')
                if len(self.Element_Fixture)==2:
                    if self.Grid_Lock:
                        Temp_Root = getattr(self.Design, self.Design.Display_ID)
                        Window_Size = Temp_Root.Size()
                        self.Grid_Width = Window_Size[0]/100
                        self.Grid_Height = Window_Size[1]/100
                    self.Dragging = True
                    self.Current = Element._ID
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        self.Global['Loading'].Hide()
            
    def Drag_Size(self, E, Element):
        try:
            if not Element.Lock and self.Dragging and self.Current==Element._ID and 'Width' in self.Element_Fixture and 'Height' in self.Element_Fixture:
                Difference_Width = (E.x_root - self._Coord['X'])
                Difference_Height = (E.y_root - self._Coord['Y'])
                New_Width = self.Element_Fixture['Width']+Difference_Width
                New_Height = self.Element_Fixture['Height']+Difference_Height
                if self.Grid_Lock:
                    New_Width = round(New_Width / self.Grid_Width)*self.Grid_Width
                    New_Height = round(New_Height / self.Grid_Height)*self.Grid_Height
                Element.Size(Width=New_Width, Height=New_Height)
                if Element._Type=='Frame' or Element._Type=='Canvas' or Element._Type=='Scroll' or Element._Type=='Popup':
                    Element_Type = 'Frame'
                elif 'Canvas_' in Element._Type:
                    Element_Type = 'Item'
                else:
                    Element_Type = 'Widget'
                Element_Data = self.Design.Database.Get(f"SELECT * FROM `{Element_Type}` WHERE `ID`='{Element._ID}'", Keys=True)
                Element_Data = Element_Data[0]
                if Element_Data['Alignment']=='Percentage':
                    Fixture_Reverse = Element._Main.Locate_Reverse(New_Width, New_Height, 0, 0)
                else:
                    Fixture_Reverse = [round(New_Width, 3), round(New_Height, 3), 0, 0]
                self.Design.Database.Post(f"UPDATE `{Element_Type}` SET `Width`={Fixture_Reverse[0]}, `Height`={Fixture_Reverse[1]} WHERE `ID`='{Element._ID}'")
                if self.Design.Configure.Current:
                    self.Design.Configure.Current.Movement_Update()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Show_Current(self, Element, Loading=True):
        try:
            if Loading and not self.Dragging:
                self.Hide_Delete()
                self.Global['Loading'].Show()
                self.Global['GUI'].After(10, lambda: self.Show_Current(Element, Loading=False))
                self.Dragging = True
            else:
                self.Design.Configure.Hide_All()
                self.Design.Configure.Reset_All()
                ID_Tree = getattr(self, Element._ID)
                Parent = self.Tree.Parent(ID_Tree)
                self.Expand_Parent(Parent)
                self.Tree.Select(ID_Tree)
                Configure = getattr(self.Design.Configure, f'Configure_{Element._Type}')
                Configure.Load(Element._ID)
                self.Dragging = False
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Expand_Parent(self, ID):
        try:
            self.Tree.Expand(ID)
            Name = self.Tree.Get(ID)[0]
            if Name and Name!=self.Parent:
                Parent = self.Tree.Parent(ID)
                self.Expand_Parent(Parent)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Default(self, Parent='Root'):
        try:
            self.Parent = Parent
            self.Tree.Remove_All()
            setattr(self, self.Parent, self.Tree.Add(self.Parent, Value=[self.Parent, 'Frame', 0]))
            self.Load()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Reset_All(self):
        try:
            Widget = self.Tree.Get()
            if len(Widget)>0:
                if Widget[0]!=self.Current:
                    self.Current = Widget[0]
                    self.Design.Configure.Hide_All()
                    self.Design.Configure.Reset_All()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Get_Current(self, Loading=True):
        try:
            if Loading:
                self.Hide_Delete()
                self.Global['Loading'].Show()
                self.Global['GUI'].After(10, lambda: self.Get_Current(Loading=False))
            else:
                Widget = self.Tree.Get()
                self.Current = Widget[0]
                if Widget:
                    self.Design.Configure.Hide_All()
                    self.Design.Configure.Reset_All()
                    if Widget[0]!=self.Parent:
                        Configure = getattr(self.Design.Configure, f'Configure_{Widget[1]}')
                        Configure.Load(Widget[0])
                    else:
                        self.Delete_Image.Hide()
                        self.Copy_Image.Hide()
                        if not self.Copy_ID:
                            self.Paste_Image.Hide()
                        self.Global['Loading'].Hide()
                else:
                    self.Global['Loading'].Hide()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Show_Delete(self):
        try:
            self.Delete_Image.Hide()
            self.Copy_Image.Hide()
            self.Paste_Image.Hide()
            self.Delete_Confirm_Image.Show()
            self.Delete_Cancel_Image.Show()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Hide_Delete(self):
        try:
            self.Delete_Confirm_Image.Hide()
            self.Delete_Cancel_Image.Hide()
            self.Delete_Image.Show()
            self.Copy_Image.Show()
            self.Export_Image.Show()
            if self.Copy_ID:
                self.Paste_Image.Show()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Copy(self):
        try:
            ID = self.Tree.Current()
            if ID:
                Element_ID = self.Tree.Get(ID)[0]
                if Element_ID!=self.Parent:
                    self.Copy_ID = ID
                    self.Paste_Image.Show()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Delete(self):
        try:
            ID = self.Tree.Selected()
            for Each in ID:
                self.Delete_All(Each)
            self.Hide_Delete()
            self.Design.Configure.Hide_All()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Delete_All(self, ID=False):
        try:
            if ID:
                if self.Copy_ID==ID:
                    self.Copy_ID = False
                    self.Paste_Image.Hide()
                for Each in self.Tree.Child(ID):
                    self.Delete_All(Each)
                Element_ID = self.Tree.Get(ID)[0]
                if Element_ID!=self.Parent:
                    if len(self.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Element_ID}'", Keys=True))>0:
                        Frame_Data = self.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Element_ID}'", Keys=True)[0]
                    elif len(self.Design.Database.Get(f"SELECT * FROM `Item` WHERE `ID`='{Element_ID}'", Keys=True))>0:
                        Frame_Data = self.Design.Database.Get(f"SELECT * FROM `Item` WHERE `ID`='{Element_ID}'", Keys=True)[0]
                    else:
                        Frame_Data = self.Design.Database.Get(f"SELECT * FROM `Widget` WHERE `ID`='{Element_ID}'", Keys=True)[0]
                    Temp_Root = Frame_Data['Root']
                    Root = Temp_Root
                    while Temp_Root!=self.Parent:
                        Frame_Data = self.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Temp_Root}'", Keys=True)
                        if len(Frame_Data)==1:
                            Frame_Data = Frame_Data[0]
                            Temp_Root = Frame_Data['Root']
                            Root = Temp_Root+'.'+Root
                        else:
                            break
                    if os.path.exists(f"{self.Design.Project_Path}/Data/File/{Element_ID}"):
                        os.remove(f"{self.Design.Project_Path}/Data/File/{Element_ID}")
                    Root = self.Global['Custom'].Get_Attr_Class(self.Design, Root)
                    Element = getattr(Root, Element_ID)
                    Element.Delete()
                    self.Tree.Remove(ID)
                    self.Design.Database.Post(f"DELETE FROM `Frame` WHERE `ID`='{Element_ID}'")
                    self.Design.Database.Post(f"DELETE FROM `Item` WHERE `ID`='{Element_ID}'")
                    self.Design.Database.Post(f"DELETE FROM `Widget` WHERE `ID`='{Element_ID}'")
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
    
    def Export(self):
        try:
            if not os.path.exists(f"{self.Design.Project_Path}/Structure"):
                os.mkdir(f"{self.Design.Project_Path}/Structure")
            self.Tree.Export(Path=f"{self.Design.Project_Path}/Structure/{self.Parent}.txt")
            self.Global['Message'].Show('Success', 'Structure Exported To Project Folder')
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Paste(self):
        try:
            Root_ID = self.Tree.Current()
            if Root_ID:
                Root_Type = self.Tree.Get(Root_ID)[1]
                if Root_Type=='Frame' or Root_Type=='Canvas' or Root_Type=='Scroll':
                    Error = False
                    Parent = Root_ID
                    while self.Tree.Get(Parent)[0]!=self.Parent:
                        if Parent==self.Copy_ID:
                            Error = True
                            break
                        Parent = self.Tree.Parent(Parent)
                    if not Error:
                        self.Paste_All(self.Copy_ID, Root_ID)
                    else:
                        self.Global['Message'].Show('Error', 'Copy Not Possible Into Same Widget')
                else:
                    self.Global['Message'].Show('Error', 'Copy To Selected Widget Not Posiible')
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Paste_All(self, ID=False, Root=False):
        try:
            if ID and Root:
                Root_ID = self.Tree.Get(Root)[0]
                Element_ID = self.Tree.Get(ID)[0]
                if len(self.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Element_ID}'", Keys=True))>0:
                    Type = 'Frame'
                elif len(self.Design.Database.Get(f"SELECT * FROM `Item` WHERE `ID`='{Element_ID}'", Keys=True))>0:
                    Type = 'Item'
                else:
                    Type = 'Widget'
                self.Design.Database.Post(f"DELETE FROM `{Type}_Copy`")
                self.Design.Database.Post(f"INSERT INTO `{Type}_Copy` SELECT * FROM `{Type}` WHERE `ID`='{Element_ID}'")
                Frame_Data = self.Design.Database.Get(f"SELECT * FROM `{Type}_Copy` WHERE `ID`='{Element_ID}'", Keys=True)[0]
                Number = 0
                Exist = self.Design.Database.Get(f"SELECT * FROM `{Type}` WHERE (`Name`='{Frame_Data['Name']}' AND `Root`='{Root_ID}')")
                while len(Exist)>0:
                    Number += 1
                    Exist = self.Design.Database.Get(f"SELECT * FROM `{Type}` WHERE (`Name`='{Frame_Data['Name']}{Number}' AND `Root`='{Root_ID}')")
                if Number>0:
                    Name = f"{Frame_Data['Name']}{Number}"
                else:
                    Name = Frame_Data['Name']
                Random_Letter = ''.join(random.choices(string.ascii_letters, k=10))
                New_ID = Random_Letter+self.Global['Custom'].MD5(Root_ID+Name+str(time.time()*1000000))
                self.Design.Database.Post(f"UPDATE `{Type}_Copy` SET `ID`='{New_ID}',`Name`='{Name}',`Root`='{Root_ID}' WHERE `ID`='{Element_ID}'")
                self.Design.Database.Post(f"INSERT INTO `{Type}` SELECT * FROM `{Type}_Copy` WHERE `ID`='{New_ID}'")
                self.Design.Database.Post(f"DELETE FROM `{Type}_Copy` WHERE `ID`='{New_ID}'")
                if os.path.exists(f"{self.Design.Project_Path}/Data/File/{Element_ID}"):
                    shutil.copy(f"{self.Design.Project_Path}/Data/File/{Element_ID}", f"{self.Design.Project_Path}/Data/File/{New_ID}")
                if Type=='Frame':
                    Root_Level = self.Tree.Get(Root)[2]
                    self.Design.Database.Post(f"UPDATE `{Type}` SET `Level`='{Root_Level+1}' WHERE `ID`='{New_ID}'")
                Widget = self.Design.Database.Get(f"SELECT * FROM `{Type}` WHERE `ID`='{New_ID}'", Keys=True)[0]
                Stock = getattr(self.Design.Stock, f"Stock_{Widget['Type']}")
                Stock.Create(Widget['ID'])
                Level = 0
                if Type=='Frame':
                    Level = Widget['Level']
                Image = self.Global['Image'](Widget['Type'])
                setattr(self, Widget['ID'], self.Tree.Add(Name=Widget['Name'], Parent=Root, Value=[Widget['ID'], Widget['Type'], Level], Path=Image))
                for Each in self.Tree.Child(ID):
                    self.Paste_All(Each, getattr(self, Widget['ID']))
        except Exception as E:
            traceback.print_exc()
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Grid(self):
        try:
            if self.Grid_Lock:
                self.Grid_Lock = False
                self.Grid_Image.Config(Path=self.Global['Image']('Grid_Unlock'))
            else:
                self.Grid_Lock = True
                self.Grid_Image.Config(Path=self.Global['Image']('Grid_Lock'))
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))