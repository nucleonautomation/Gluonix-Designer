################################################################################################################################
#Element
################################################################################################################################
import inspect
import os
import re
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
            self.Window = False
            self.Widget = []
            self.Grid_Lock = True
            self.Grid_Width = 10
            self.Grid_Height = 10
            self.Copy_ID = False
            self.Current = False
            self.Dragging = False
            self.Current = False
            self.Selected = []
            self._Coord = {'X': 0, 'Y': 0}
            self.Element_Fixture = {}
            
            #Frame
            Fixture = self.Design.Frame.Locate(29.5, 90, 30, 10)
            self.Frame = self.Global['Gluonix'].Frame(self.Design.Frame)
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Background='#FFFFFF', Border_Size=0, Display=True)
            self.Frame.Config(Resize=True, Move=True)
            self.Frame.Create()
            self.Design.Widget.append(self.Frame)
            
            #Label
            Fixture = self.Frame.Locate(30, 3, 0, 1)
            self.Label = self.Global['Gluonix'].Label(self.Frame)
            self.Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Label.Config(Background='#FFFFFF', Border_Size=0, Display=True)
            self.Label.Config(Foreground='#000000', Font_Size=16, Font_Weight='normal', Align='w')
            self.Label.Config(Resize=True, Move=True)
            self.Label.Set(' PROJECT')
            self.Label.Create()
            
            #Paste
            Fixture = self.Frame.Locate(10, 4, 60, 0.5)
            self.Paste_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Paste_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Paste_Image.Config(Path=self.Global['Image']('Paste'), Border_Size=0, Hand_Cursor=True, Display=False)
            self.Paste_Image.Bind(On_Click=lambda E: self.Paste())
            self.Paste_Image.Bind(On_Hover_In=lambda E: self.Paste_Image.Enlarge(2))
            self.Paste_Image.Bind(On_Hover_Out=lambda E: self.Paste_Image.Shrink(2))
            self.Paste_Image.Create()
            
            #Copy
            Fixture = self.Frame.Locate(10, 4, 70, 0.5)
            self.Copy_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Copy_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Copy_Image.Config(Path=self.Global['Image']('Copy'), Border_Size=0, Hand_Cursor=True, Display=True)
            self.Copy_Image.Bind(On_Click=lambda E: self.Copy())
            self.Copy_Image.Bind(On_Hover_In=lambda E: self.Copy_Image.Enlarge(2))
            self.Copy_Image.Bind(On_Hover_Out=lambda E: self.Copy_Image.Shrink(2))
            self.Copy_Image.Create()
            
            #Delete Comfirm
            Fixture = self.Frame.Locate(10, 4, 70, 0.5)
            self.Delete_Confirm_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Delete_Confirm_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Delete_Confirm_Image.Config(Path=self.Global['Image']('Success'), Border_Size=0, Hand_Cursor=True, Display=False)
            self.Delete_Confirm_Image.Bind(On_Click=lambda E: self.Delete())
            self.Delete_Confirm_Image.Bind(On_Hover_In=lambda E: self.Delete_Confirm_Image.Enlarge(2))
            self.Delete_Confirm_Image.Bind(On_Hover_Out=lambda E: self.Delete_Confirm_Image.Shrink(2))
            self.Delete_Confirm_Image.Create()
            
            #Delete
            Fixture = self.Frame.Locate(10, 4, 80, 0.5)
            self.Delete_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Delete_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Delete_Image.Config(Path=self.Global['Image']('Delete'), Border_Size=0, Hand_Cursor=True, Display=True)
            self.Delete_Image.Bind(Add=False, On_Click=lambda E: self.Show_Delete())
            self.Delete_Image.Bind(On_Hover_In=lambda E: self.Delete_Image.Enlarge(2))
            self.Delete_Image.Bind(On_Hover_Out=lambda E: self.Delete_Image.Shrink(2))
            self.Delete_Image.Create()
            
            #Grid
            Fixture = self.Frame.Locate(10, 3.5, 90, 0.75)
            self.Grid_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Grid_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Grid_Image.Config(Path=self.Global['Image']('Grid_Lock'), Border_Size=0, Hand_Cursor=True, Display=True)
            self.Grid_Image.Bind(On_Click=lambda E: self.Grid())
            self.Grid_Image.Bind(On_Hover_In=lambda E: self.Grid_Image.Enlarge(2))
            self.Grid_Image.Bind(On_Hover_Out=lambda E: self.Grid_Image.Shrink(2))
            self.Grid_Image.Create()
            
            #Align Left
            Fixture = self.Frame.Locate(10, 4.5, 50, 5)
            self.Align_Left_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Align_Left_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Align_Left_Image.Config(Path=self.Global['Image']('Align_Left'), Border_Size=0, Hand_Cursor=True, Display=True)
            self.Align_Left_Image.Bind(On_Click=lambda E: self.Align_Left())
            self.Align_Left_Image.Bind(On_Hover_In=lambda E: self.Align_Left_Image.Enlarge(2))
            self.Align_Left_Image.Bind(On_Hover_Out=lambda E: self.Align_Left_Image.Shrink(2))
            self.Align_Left_Image.Create()
            
            #Align Top
            Fixture = self.Frame.Locate(10, 4.5, 60, 5)
            self.Align_Top_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Align_Top_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Align_Top_Image.Config(Path=self.Global['Image']('Align_Top'), Border_Size=0, Hand_Cursor=True, Display=True)
            self.Align_Top_Image.Bind(On_Click=lambda E: self.Align_Top())
            self.Align_Top_Image.Bind(On_Hover_In=lambda E: self.Align_Top_Image.Enlarge(2))
            self.Align_Top_Image.Bind(On_Hover_Out=lambda E: self.Align_Top_Image.Shrink(2))
            self.Align_Top_Image.Create()
            
            #Align Right
            Fixture = self.Frame.Locate(10, 4.5, 70, 5)
            self.Align_Right_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Align_Right_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Align_Right_Image.Config(Path=self.Global['Image']('Align_Right'), Border_Size=0, Hand_Cursor=True, Display=True)
            self.Align_Right_Image.Bind(On_Click=lambda E: self.Align_Right())
            self.Align_Right_Image.Bind(On_Hover_In=lambda E: self.Align_Right_Image.Enlarge(2))
            self.Align_Right_Image.Bind(On_Hover_Out=lambda E: self.Align_Right_Image.Shrink(2))
            self.Align_Right_Image.Create()
            
            #Align Bottom
            Fixture = self.Frame.Locate(10, 4.5, 80, 5)
            self.Align_Bottom_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Align_Bottom_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Align_Bottom_Image.Config(Path=self.Global['Image']('Align_Bottom'), Border_Size=0, Hand_Cursor=True, Display=True)
            self.Align_Bottom_Image.Bind(On_Click=lambda E: self.Align_Bottom())
            self.Align_Bottom_Image.Bind(On_Hover_In=lambda E: self.Align_Bottom_Image.Enlarge(2))
            self.Align_Bottom_Image.Bind(On_Hover_Out=lambda E: self.Align_Bottom_Image.Shrink(2))
            self.Align_Bottom_Image.Create()
            
            #Align Center
            Fixture = self.Frame.Locate(10, 4.5, 90, 5)
            self.Align_Center_Image = self.Global['Gluonix'].Image(self.Frame)
            self.Align_Center_Image.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Align_Center_Image.Config(Path=self.Global['Image']('Align_Center'), Border_Size=0, Hand_Cursor=True, Display=True)
            self.Align_Center_Image.Bind(On_Click=lambda E: self.Align_Center())
            self.Align_Center_Image.Bind(On_Hover_In=lambda E: self.Align_Center_Image.Enlarge(2))
            self.Align_Center_Image.Bind(On_Hover_Out=lambda E: self.Align_Center_Image.Shrink(2))
            self.Align_Center_Image.Create()
            
            #Tree
            Fixture = self.Frame.Locate(100, 90, 0, 10)
            self.Tree = self.Global['Gluonix'].Tree(self.Frame)
            self.Tree.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Tree.Config(Background='#FFFFFF', Border_Size=0, Display=True)
            self.Tree.Config(Foreground='#000000', Font_Size=16, Font_Weight='normal')
            self.Tree.Config(Resize=True, Move=True)
            self.Tree.Bind(On_Click=lambda E: self.Clear_Selection())
            self.Tree.Bind(On_Release=lambda E: self.Get_Current())
            self.Tree.Bind(On_Control_Click=lambda E: None)
            self.Tree.Bind(On_Control_Release=lambda E: self.Get_Control_Current())
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
                setattr(self, Widget['ID'], self.Tree.Add(Name=f" {Widget['Name']}", Parent=Root, Value=[Widget['ID'], Widget['Type'], 0], Path=Image))
            Widgets = self.Design.Database.Get(f"SELECT * FROM `Item` WHERE `Root`='{Parent}'", Keys=True)
            for Widget in Widgets:
                Stock = getattr(self.Design.Stock, f"Stock_{Widget['Type']}")
                Stock.Create(Widget['ID'])
                Root = getattr(self, Widget['Root'])
                Image = self.Global['Image'](Widget['Type'])
                setattr(self, Widget['ID'], self.Tree.Add(Name=f" {Widget['Name']}", Parent=Root, Value=[Widget['ID'], Widget['Type'], 0], Path=Image))
            Widgets = self.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `Root`='{Parent}'", Keys=True)
            for Widget in Widgets:
                Stock = getattr(self.Design.Stock, f"Stock_{Widget['Type']}")
                Stock.Create(Widget['ID'])
                Root = getattr(self, Widget['Root'])
                Image = self.Global['Image'](Widget['Type'])
                setattr(self, Widget['ID'], self.Tree.Add(Name=f" {Widget['Name']}", Parent=Root, Value=[Widget['ID'], Widget['Type'], Widget['Level']], Path=Image))
                self.Load_Child(Widget['ID'])
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Intractive(self, Element):
        try:
            Element.Bind(On_Click=lambda E: self.Drag_Start(E, Element), On_Drag=lambda E: self.Drag(E, Element), On_Release=lambda E: self.Drag_Release(E, Element))
            Element.Bind(On_Right_Click=lambda E: self.Drag_Start_Size(E, Element), On_Right_Drag=lambda E: self.Drag_Size(E, Element), On_Right_Release=lambda E: self.Drag_Release(E, Element))
            Element.Bind(On_Double_Click=lambda E: self.Show_Current(Element))
            Element.Bind(On_Control_Click=lambda E: self.Select_Current(Element))
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Drag_Release(self, E, Element):
        try:
            if self.Dragging and self.Current == Element._ID:
                Moved = False
                if hasattr(self, '_Coord'):
                    Dist_X = abs(E.x_root - self._Coord['X'])
                    Dist_Y = abs(E.y_root - self._Coord['Y'])
                    if Dist_X > 2 or Dist_Y > 2:
                        Moved = True
                if not Moved:
                    if len(self.Selected) > 1 and Element in self.Selected:
                         self.Clear_Selection(Element)
            self.Dragging = False
            self.Current = False
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))

    def Drag_Start(self, E, Element):
        try:
            if Element not in self.Selected:
                self.Clear_Selection(Element)
            if not Element.Lock and not self.Dragging:
                self.Drag_Items = []
                if Element in self.Selected:
                    Reference_Main = self.Selected[0]._Main
                    Same_Parent = True
                    for Item in self.Selected:
                        if Item._Main != Reference_Main:
                            Same_Parent = False
                            break
                    if Same_Parent:
                        self.Drag_Items = self.Selected
                    else:
                        self.Global['Message'].Show('Error', 'Move Same Container Elements Only')
                        return
                else:
                    self.Drag_Items = [Element]
                Any_Locked = False
                for Item in self.Drag_Items:
                    if Item.Lock:
                        Any_Locked = True
                        break
                if Any_Locked:
                    self.Global['Message'].Show('Error', 'Selection Contains Locked Elements')
                    self.Drag_Items = []
                    return
                self._Coord = {'X': E.x_root, 'Y': E.y_root}
                self.Element_Fixtures = {}
                self.Element_Ratios = {}
                for Item in self.Drag_Items:
                    self.Element_Fixtures[Item._ID] = Item.Config_Get('Left', 'Top')
                    Box = Item.Box()
                    Config = Item.Config_Get('Width', 'Height')
                    W_Ratio = 1.0
                    H_Ratio = 1.0
                    if Config['Width'] > 0 and Config['Height'] > 0 and Box[2] > 0 and Box[3] > 0:
                        W_Ratio = Box[2] / Config['Width']
                        H_Ratio = Box[3] / Config['Height']
                    self.Element_Ratios[Item._ID] = {'W': W_Ratio, 'H': H_Ratio}
                self.Dragging = True
                self.Current = Element._ID
                self.Window = getattr(self.Design, self.Parent)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        self.Global['Loading'].Hide()

    def Drag(self, E, Element):
        try:
            if not Element.Lock and self.Dragging and self.Current==Element._ID:
                Raw_Diff_X = E.x_root - self._Coord['X']
                Raw_Diff_Y = E.y_root - self._Coord['Y']
                for Item in self.Drag_Items:
                    if not Item.Lock and Item._ID in self.Element_Fixtures and Item._ID in self.Element_Ratios:
                        Fixture = self.Element_Fixtures[Item._ID]
                        Ratios = self.Element_Ratios[Item._ID]
                        Difference_Left = Raw_Diff_X / Ratios['W']
                        Difference_Top = Raw_Diff_Y / Ratios['H']
                        New_Left = Fixture['Left'] + Difference_Left
                        New_Top = Fixture['Top'] + Difference_Top
                        if self.Grid_Lock:
                            New_Left = round(New_Left / self.Grid_Width)*self.Grid_Width
                            New_Top = round(New_Top / self.Grid_Height)*self.Grid_Height
                        Item.Position(Left=New_Left, Top=New_Top)
                        if Item._Type=='Frame' or Item._Type=='Canvas' or Item._Type=='Scroll' or Item._Type=='Popup':
                            Element_Type = 'Frame'
                        elif 'Canvas_' in Item._Type:
                            Element_Type = 'Item'
                        else:
                            Element_Type = 'Widget'
                        Element_Data = self.Design.Database.Get(f"SELECT * FROM `{Element_Type}` WHERE `ID`='{Item._ID}'", Keys=True)
                        Element_Data = Element_Data[0]
                        if Element_Data['Alignment']=='Percentage':
                            Fixture_Reverse = Item._Main.Locate_Reverse(0, 0, New_Left, New_Top)
                        else:
                            Fixture_Reverse = [0, 0, round(New_Left, 3), round(New_Top, 3)]
                        self.Design.Database.Post(f"UPDATE `{Element_Type}` SET `Left`={Fixture_Reverse[2]}, `Top`={Fixture_Reverse[3]} WHERE `ID`='{Item._ID}'")
                if self.Design.Configure.Current:
                    self.Design.Configure.Current.Movement_Update()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))

    def Drag_Start_Size(self, E, Element):
        try:
            self.Clear_Selection(Element)
            if not Element.Lock and not self.Dragging:
                self._Coord = {'X': E.x_root, 'Y': E.y_root}
                self.Element_Fixture = Element.Config_Get('Width', 'Height', 'Left', 'Top')
                Box = Element.Box()
                if self.Element_Fixture['Width'] > 0 and self.Element_Fixture['Height'] > 0 and Box[2] > 0 and Box[3] > 0:
                    self.Width_Ratio = Box[2] / self.Element_Fixture['Width']
                    self.Height_Ratio = Box[3] / self.Element_Fixture['Height']
                else:
                    self.Width_Ratio = 1.0
                    self.Height_Ratio = 1.0
                self.Resize_Direction = []
                Widget_Width_Px = Box[2]
                Widget_Height_Px = Box[3]
                if E.x < (Widget_Width_Px / 2):
                    self.Resize_Direction.append('Left')
                else:
                    self.Resize_Direction.append('Right')
                if E.y < (Widget_Height_Px / 2):
                    self.Resize_Direction.append('Top')
                else:
                    self.Resize_Direction.append('Bottom')
                if len(self.Element_Fixture) >= 4:
                    self.Dragging = True
                    self.Current = Element._ID
                    self.Window = getattr(self.Design, self.Parent)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
        self.Global['Loading'].Hide()

    def Drag_Size(self, E, Element):
        try:
            if not Element.Lock and self.Dragging and self.Current == Element._ID:
                Diff_X = (E.x_root - self._Coord['X']) / self.Width_Ratio
                Diff_Y = (E.y_root - self._Coord['Y']) / self.Height_Ratio
                New_Width = self.Element_Fixture['Width']
                New_Height = self.Element_Fixture['Height']
                New_Left = self.Element_Fixture['Left']
                New_Top = self.Element_Fixture['Top']
                if 'Left' in self.Resize_Direction:
                    Calculated_Left = self.Element_Fixture['Left'] + Diff_X
                    if self.Grid_Lock:
                        Calculated_Left = round(Calculated_Left / self.Grid_Width) * self.Grid_Width
                    Delta_Left = Calculated_Left - self.Element_Fixture['Left']
                    New_Left = Calculated_Left
                    New_Width = self.Element_Fixture['Width'] - Delta_Left
                elif 'Right' in self.Resize_Direction:
                    New_Width = self.Element_Fixture['Width'] + Diff_X
                    if self.Grid_Lock:
                        New_Width = round(New_Width / self.Grid_Width) * self.Grid_Width
                if 'Top' in self.Resize_Direction:
                    Calculated_Top = self.Element_Fixture['Top'] + Diff_Y
                    if self.Grid_Lock:
                        Calculated_Top = round(Calculated_Top / self.Grid_Height) * self.Grid_Height
                    Delta_Top = Calculated_Top - self.Element_Fixture['Top']
                    New_Top = Calculated_Top
                    New_Height = self.Element_Fixture['Height'] - Delta_Top
                elif 'Bottom' in self.Resize_Direction:
                    New_Height = self.Element_Fixture['Height'] + Diff_Y
                    if self.Grid_Lock:
                        New_Height = round(New_Height / self.Grid_Height) * self.Grid_Height
                Element.Size(Width=New_Width, Height=New_Height)
                Element.Position(Left=New_Left, Top=New_Top)
                if Element._Type=='Frame' or Element._Type=='Canvas' or Element._Type=='Scroll' or Element._Type=='Popup':
                    Element_Type = 'Frame'
                elif 'Canvas_' in Element._Type:
                    Element_Type = 'Item'
                else:
                    Element_Type = 'Widget'
                Element_Data = self.Design.Database.Get(f"SELECT * FROM `{Element_Type}` WHERE `ID`='{Element._ID}'", Keys=True)
                Element_Data = Element_Data[0]
                if Element_Data['Alignment'] == 'Percentage':
                    Fixture_Reverse = Element._Main.Locate_Reverse(New_Width, New_Height, New_Left, New_Top)
                else:
                    Fixture_Reverse = [round(New_Width, 3), round(New_Height, 3), round(New_Left, 3), round(New_Top, 3)]
                self.Design.Database.Post(f"UPDATE `{Element_Type}` SET `Width`={Fixture_Reverse[0]}, `Height`={Fixture_Reverse[1]}, `Left`={Fixture_Reverse[2]}, `Top`={Fixture_Reverse[3]} WHERE `ID`='{Element._ID}'")
                if self.Design.Configure.Current:
                    self.Design.Configure.Current.Movement_Update()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))

    def Show_Current(self, Element, Loading=True):
        try:
            if Loading and not self.Dragging:
                self.Clear_Selection(Element)
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
            
    def Select_Current(self, Element):
        try:
            if len(self.Selected)==0:
                self.Hide_Delete()
                self.Design.Configure.Hide_All()
                self.Design.Configure.Reset_All()
            if Element not in self.Selected:
                self.Selected.append(Element)
                ID_Tree = getattr(self, Element._ID)
                Parent = self.Tree.Parent(ID_Tree)
                self.Expand_Parent(Parent)
                self.Tree.Select(ID_Tree, Keep=True)
            else:
                self.Selected.remove(Element)
                ID_Tree = getattr(self, Element._ID)
                self.Tree.Unselect(ID_Tree)
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Clear_Selection(self, Element=None):
        try:
            self.Tree.Unselect()
            self.Selected = []
            if Element:
                self.Selected = [Element]
                ID_Tree = getattr(self, Element._ID)
                Parent = self.Tree.Parent(ID_Tree)
                self.Expand_Parent(Parent)
                self.Tree.Select(ID_Tree, Keep=True)
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
            setattr(self, self.Parent, self.Tree.Add(f" {self.Parent}", Value=[self.Parent, 'Frame', 0]))
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
            Widget = self.Tree.Get()
            if Widget and self.Current!=Widget[0]:
                if Loading:
                    self.Global['Loading'].Show()
                    self.Global['GUI'].After(10, lambda: self.Get_Current(Loading=False))
                else:
                    Widget = self.Tree.Get()
                    if len(Widget)>0:
                        if self.Current!=Widget[0]:
                            self.Current = Widget[0]
                            self.Hide_Delete()
                            self.Design.Configure.Hide_All()
                            self.Design.Configure.Reset_All()
                            if Widget[0]!=self.Parent:
                                Configure = getattr(self.Design.Configure, f'Configure_{Widget[1]}')
                                Configure.Load(Widget[0])
                                self.Selected = [Configure.Element]
                            else:
                                self.Delete_Image.Hide()
                                self.Copy_Image.Hide()
                                if not self.Copy_ID:
                                    self.Paste_Image.Hide()
                                self.Global['Loading'].Hide()
                        else:
                            self.Global['Loading'].Hide()
                    else:
                        self.Global['Loading'].Hide()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Get_Control_Current(self):
        try:
            Items = self.Tree.Get_Selected()
            if len(Items)>0:
                self.Selected = []
                for Item in Items:
                    Widget = Item['values']
                    if Widget[0]!=self.Parent:
                        self.Selected.append(getattr(self, f"{Widget[0]}_Widget"))
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Show_Delete(self):
        try:
            self.Delete_Image.Set(self.Global['Image']('Close'))
            self.Delete_Image.Bind(Add=False, On_Click=lambda E: self.Hide_Delete())
            self.Copy_Image.Hide()
            self.Paste_Image.Hide()
            self.Delete_Confirm_Image.Show()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Hide_Delete(self):
        try:
            self.Delete_Confirm_Image.Hide()
            self.Delete_Image.Set(self.Global['Image']('Delete'))
            self.Delete_Image.Bind(Add=False, On_Click=lambda E: self.Show_Delete())
            self.Delete_Image.Show()
            self.Copy_Image.Show()
            if self.Copy_ID:
                self.Paste_Image.Show()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Copy(self):
        try:
            Temp_ID = self.Tree.Get_Selected()
            if len(Temp_ID)==1:
                ID = self.Tree.Current()
                if ID:
                    Element_ID = self.Tree.Get(ID)[0]
                    if Element_ID!=self.Parent:
                        self.Copy_ID = ID
                        self.Paste_Image.Show()
            else:
                self.Copy_ID = False
                self.Paste_Image.Hide()
                self.Global['Message'].Show('Error', 'Only Single Widget Copy Supported')
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Paste(self):
        try:
            Root_ID = self.Tree.Current()
            if Root_ID:
                Root_Info = self.Tree.Get(Root_ID)
                while Root_Info[1]!='Frame' and Root_Info[1]!='Canvas' and Root_Info[1]!='Scroll' and Root_Info[1]!='Group':
                    Root_ID = self.Tree.Parent(Root_ID)
                    Root_Info = self.Tree.Get(Root_ID)
                if Root_Info[1]=='Frame' or Root_Info[1]=='Canvas' or Root_Info[1]=='Scroll' or Root_Info[1]=='Group':
                    Error = False
                    if Root_ID!=self.Copy_ID:
                        Parent = Root_ID
                        while self.Tree.Get(Parent)[0]!=self.Parent:
                            if Parent==self.Copy_ID:
                                Error = True
                                break
                            Parent = self.Tree.Parent(Parent)
                    else:
                        Root_ID = self.Tree.Parent(Root_ID)
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
                Run = True
                if Type == 'Item':
                    if Root_ID!='Root':
                        Run = False
                        Widget = self.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Root_ID}'", Keys=True)
                        while Widget[0]['Type']=='Group' and Widget[0]['Root']!='Root':
                            Temp_Root_ID = Widget[0]['Root']
                            Widget = self.Design.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Temp_Root_ID}'", Keys=True)
                        if Widget[0]['Type']=='Canvas' or Widget[0]['Type']=='Scroll':
                            Run = True
                    else:
                        Run = False
                if Run:
                    self.Design.Database.Post(f"DELETE FROM `{Type}_Copy`")
                    self.Design.Database.Post(f"INSERT INTO `{Type}_Copy` SELECT * FROM `{Type}` WHERE `ID`='{Element_ID}'")
                    Frame_Data = self.Design.Database.Get(f"SELECT * FROM `{Type}_Copy` WHERE `ID`='{Element_ID}'", Keys=True)[0]
                    Match = re.match(r'^(.*?)(\d+)?$', Frame_Data['Name'])
                    Base_Name = Match.group(1)
                    Number = int(Match.group(2)) if Match.group(2) else 0
                    Name_Attempt = f"{Base_Name}{Number}" if Number > 0 else Base_Name
                    Exist = self.Design.Database.Get(f"SELECT * FROM `{Type}` WHERE (`Name`='{Name_Attempt}' AND `Root`='{Root_ID}')")
                    while len(Exist) > 0:
                        Number += 1
                        Name_Attempt = f"{Base_Name}{Number}"
                        Exist = self.Design.Database.Get(f"SELECT * FROM `{Type}` WHERE (`Name`='{Name_Attempt}' AND `Root`='{Root_ID}')")
                    Name = Name_Attempt
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
                    setattr(self, Widget['ID'], self.Tree.Add(Name=f" {Widget['Name']}", Parent=Root, Value=[Widget['ID'], Widget['Type'], Level], Path=Image))
                    for Each in self.Tree.Child(ID):
                        self.Paste_All(Each, getattr(self, Widget['ID']))
        except Exception as E:
            traceback.print_exc()
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
            
    def Grid(self):
        try:
            if self.Grid_Lock:
                self.Grid_Lock = False
                self.Grid_Image.Set(self.Global['Image']('Grid_Unlock'))
            else:
                self.Grid_Lock = True
                self.Grid_Image.Set(self.Global['Image']('Grid_Lock'))
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Align_Left(self):
        try:
            if len(self.Selected)>0:
                Reference_Main = self.Selected[0]._Main
                Same_Parent = True
                for Element in self.Selected:
                    if Element._Main != Reference_Main:
                        Same_Parent = False
                        self.Global['Message'].Show('Error', 'Align Same Container Elements Only')
                        break
                if Same_Parent:
                    Left_Values = []
                    for Element in self.Selected:
                        Config = Element.Config_Get('Left')
                        Left_Values.append(Config['Left'])
                    Target_Left = min(Left_Values)
                    for Element in self.Selected:
                        if not Element.Lock:
                            Element.Position(Left=Target_Left)
                            if Element._Type=='Frame' or Element._Type=='Canvas' or Element._Type=='Scroll' or Element._Type=='Popup':
                                Element_Type = 'Frame'
                            elif 'Canvas_' in Element._Type:
                                Element_Type = 'Item'
                            else:
                                Element_Type = 'Widget'
                            Element_Data = self.Design.Database.Get(f"SELECT * FROM `{Element_Type}` WHERE `ID`='{Element._ID}'", Keys=True)
                            Element_Data = Element_Data[0]
                            if Element_Data['Alignment']=='Percentage':
                                Config = Element.Config_Get('Width', 'Height', 'Top')
                                Fixture_Reverse = Element._Main.Locate_Reverse(Config['Width'], Config['Height'], Target_Left, Config['Top'])
                                New_Left = Fixture_Reverse[2]
                            else:
                                New_Left = round(Target_Left, 3)
                            self.Design.Database.Post(f"UPDATE `{Element_Type}` SET `Left`={New_Left} WHERE `ID`='{Element._ID}'")
                            if self.Design.Configure.Current:
                                self.Design.Configure.Current.Movement_Update()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Align_Top(self):
        try:
            if len(self.Selected)>0:
                Reference_Main = self.Selected[0]._Main
                Same_Parent = True
                for Element in self.Selected:
                    if Element._Main != Reference_Main:
                        Same_Parent = False
                        self.Global['Message'].Show('Error', 'Align Same Container Elements Only')
                        break
                if Same_Parent:
                    Top_Values = []
                    for Element in self.Selected:
                        Config = Element.Config_Get('Top')
                        Top_Values.append(Config['Top'])
                    Target_Top = min(Top_Values)
                    for Element in self.Selected:
                        if not Element.Lock:
                            Element.Position(Top=Target_Top)
                            if Element._Type=='Frame' or Element._Type=='Canvas' or Element._Type=='Scroll' or Element._Type=='Popup':
                                Element_Type = 'Frame'
                            elif 'Canvas_' in Element._Type:
                                Element_Type = 'Item'
                            else:
                                Element_Type = 'Widget'
                            Element_Data = self.Design.Database.Get(f"SELECT * FROM `{Element_Type}` WHERE `ID`='{Element._ID}'", Keys=True)
                            Element_Data = Element_Data[0]
                            if Element_Data['Alignment']=='Percentage':
                                Config = Element.Config_Get('Width', 'Height', 'Left')
                                Fixture_Reverse = Element._Main.Locate_Reverse(Config['Width'], Config['Height'], Config['Left'], Target_Top)
                                New_Top = Fixture_Reverse[3]
                            else:
                                New_Top = round(Target_Top, 3)
                            self.Design.Database.Post(f"UPDATE `{Element_Type}` SET `Top`={New_Top} WHERE `ID`='{Element._ID}'")
                            if self.Design.Configure.Current:
                                self.Design.Configure.Current.Movement_Update()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))

    def Align_Right(self):
        try:
            if len(self.Selected)>0:
                Reference_Main = self.Selected[0]._Main
                Same_Parent = True
                for Element in self.Selected:
                    if Element._Main != Reference_Main:
                        Same_Parent = False
                        self.Global['Message'].Show('Error', 'Align Same Container Elements Only')
                        break
                if Same_Parent:
                    Right_Values = []
                    for Element in self.Selected:
                        Config = Element.Config_Get('Left', 'Width')
                        Right_Values.append(Config['Left'] + Config['Width'])
                    Target_Right = max(Right_Values)
                    for Element in self.Selected:
                        if not Element.Lock:
                            Config_Current = Element.Config_Get('Width')
                            Target_Left = Target_Right - Config_Current['Width']
                            Element.Position(Left=Target_Left)
                            if Element._Type=='Frame' or Element._Type=='Canvas' or Element._Type=='Scroll' or Element._Type=='Popup':
                                Element_Type = 'Frame'
                            elif 'Canvas_' in Element._Type:
                                Element_Type = 'Item'
                            else:
                                Element_Type = 'Widget'
                            Element_Data = self.Design.Database.Get(f"SELECT * FROM `{Element_Type}` WHERE `ID`='{Element._ID}'", Keys=True)
                            Element_Data = Element_Data[0]
                            if Element_Data['Alignment']=='Percentage':
                                Config = Element.Config_Get('Width', 'Height', 'Top')
                                Fixture_Reverse = Element._Main.Locate_Reverse(Config['Width'], Config['Height'], Target_Left, Config['Top'])
                                New_Left = Fixture_Reverse[2]
                            else:
                                New_Left = round(Target_Left, 3)
                            self.Design.Database.Post(f"UPDATE `{Element_Type}` SET `Left`={New_Left} WHERE `ID`='{Element._ID}'")
                            if self.Design.Configure.Current:
                                self.Design.Configure.Current.Movement_Update()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))

    def Align_Bottom(self):
        try:
            if len(self.Selected)>0:
                Reference_Main = self.Selected[0]._Main
                Same_Parent = True
                for Element in self.Selected:
                    if Element._Main != Reference_Main:
                        Same_Parent = False
                        self.Global['Message'].Show('Error', 'Align Same Container Elements Only')
                        break
                if Same_Parent:
                    Bottom_Values = []
                    for Element in self.Selected:
                        Config = Element.Config_Get('Top', 'Height')
                        Bottom_Values.append(Config['Top'] + Config['Height'])
                    Target_Bottom = max(Bottom_Values)
                    for Element in self.Selected:
                        if not Element.Lock:
                            Config_Current = Element.Config_Get('Height')
                            Target_Top = Target_Bottom - Config_Current['Height']
                            Element.Position(Top=Target_Top)
                            if Element._Type=='Frame' or Element._Type=='Canvas' or Element._Type=='Scroll' or Element._Type=='Popup':
                                Element_Type = 'Frame'
                            elif 'Canvas_' in Element._Type:
                                Element_Type = 'Item'
                            else:
                                Element_Type = 'Widget'
                            Element_Data = self.Design.Database.Get(f"SELECT * FROM `{Element_Type}` WHERE `ID`='{Element._ID}'", Keys=True)
                            Element_Data = Element_Data[0]
                            if Element_Data['Alignment']=='Percentage':
                                Config = Element.Config_Get('Width', 'Height', 'Left')
                                Fixture_Reverse = Element._Main.Locate_Reverse(Config['Width'], Config['Height'], Config['Left'], Target_Top)
                                New_Top = Fixture_Reverse[3]
                            else:
                                New_Top = round(Target_Top, 3)
                            self.Design.Database.Post(f"UPDATE `{Element_Type}` SET `Top`={New_Top} WHERE `ID`='{Element._ID}'")
                            if self.Design.Configure.Current:
                                self.Design.Configure.Current.Movement_Update()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Align_Center(self):
        try:
            if len(self.Selected)>0:
                Reference_Main = self.Selected[0]._Main
                Same_Parent = True
                for Element in self.Selected:
                    if Element._Main != Reference_Main:
                        Same_Parent = False
                        self.Global['Message'].Show('Error', 'Align Same Container Elements Only')
                        break
                if Same_Parent:
                    Left_Values = []
                    Right_Values = []
                    for Element in self.Selected:
                        Config = Element.Config_Get('Left', 'Width')
                        Left_Values.append(Config['Left'])
                        Right_Values.append(Config['Left'] + Config['Width'])
                    Target_Center = (min(Left_Values) + max(Right_Values)) / 2
                    for Element in self.Selected:
                        if not Element.Lock:
                            Config_Current = Element.Config_Get('Width')
                            Target_Left = Target_Center - (Config_Current['Width'] / 2)
                            Element.Position(Left=Target_Left)
                            if Element._Type=='Frame' or Element._Type=='Canvas' or Element._Type=='Scroll' or Element._Type=='Popup':
                                Element_Type = 'Frame'
                            elif 'Canvas_' in Element._Type:
                                Element_Type = 'Item'
                            else:
                                Element_Type = 'Widget'
                            Element_Data = self.Design.Database.Get(f"SELECT * FROM `{Element_Type}` WHERE `ID`='{Element._ID}'", Keys=True)
                            Element_Data = Element_Data[0]
                            if Element_Data['Alignment']=='Percentage':
                                Config = Element.Config_Get('Width', 'Height', 'Top')
                                Fixture_Reverse = Element._Main.Locate_Reverse(Config['Width'], Config['Height'], Target_Left, Config['Top'])
                                New_Left = Fixture_Reverse[2]
                            else:
                                New_Left = round(Target_Left, 3)
                            self.Design.Database.Post(f"UPDATE `{Element_Type}` SET `Left`={New_Left} WHERE `ID`='{Element._ID}'")
                            if self.Design.Configure.Current:
                                self.Design.Configure.Current.Movement_Update()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))