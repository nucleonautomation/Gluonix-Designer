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
    def __init__(self, Global, Compare):
        try:
            self.Global = Global
            self.Compare = Compare
            self.Widget = []
            self.Parent = False
            self.Database = False
            self.Project_Path = False
            
            #Frame
            Fixture = self.Compare.Frame.Locate(38, 88, 2, 12)
            self.Frame = self.Global['Gluonix'].Frame(self.Compare.Frame)
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Background='#FFFFFF', Border_Size=0, Display=True)
            self.Frame.Config(Resize=True, Move=True)
            self.Frame.Create()
            self.Compare.Widget.append(self.Frame)
            
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
            self.Tree.Config(Resize=True, Move=True)
            self.Tree.Create()
                   
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Load(self):
        try:
            if self.Parent:
                self.Load_Child(self.Parent)
                self.Tree.Expand(getattr(self, self.Parent))
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Load_Child(self, Parent='Root'):
        try:
            Widgets = self.Database.Get(f"SELECT * FROM `Widget` WHERE `Root`='{Parent}'", Keys=True)
            for Widget in Widgets:
                Root = getattr(self, Widget['Root'])
                Image = self.Global['Image'](Widget['Type'])
                setattr(self, Widget['ID'], self.Tree.Add(Name=Widget['Name'], Parent=Root, Value=[Widget['ID'], Widget['Type'], 0], Path=Image))
            Widgets = self.Database.Get(f"SELECT * FROM `Item` WHERE `Root`='{Parent}'", Keys=True)
            for Widget in Widgets:
                Root = getattr(self, Widget['Root'])
                Image = self.Global['Image'](Widget['Type'])
                setattr(self, Widget['ID'], self.Tree.Add(Name=Widget['Name'], Parent=Root, Value=[Widget['ID'], Widget['Type'], 0], Path=Image))
            Widgets = self.Database.Get(f"SELECT * FROM `Frame` WHERE `Root`='{Parent}'", Keys=True)
            for Widget in Widgets:
                Root = getattr(self, Widget['Root'])
                Image = self.Global['Image'](Widget['Type'])
                setattr(self, Widget['ID'], self.Tree.Add(Name=Widget['Name'], Parent=Root, Value=[Widget['ID'], Widget['Type'], Widget['Level']], Path=Image))
                self.Load_Child(Widget['ID'])
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
            
    def Show_Delete(self):
        try:
            self.Delete_Image.Hide()
            self.Delete_Confirm_Image.Show()
            self.Delete_Cancel_Image.Show()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Hide_Delete(self):
        try:
            self.Delete_Confirm_Image.Hide()
            self.Delete_Cancel_Image.Hide()
            self.Delete_Image.Show()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Delete(self):
        try:
            ID = self.Tree.Selected()
            for Each in ID:
                self.Delete_All(Each)
            self.Hide_Delete()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Delete_All(self, ID=False):
        try:
            if ID:
                for Each in self.Tree.Child(ID):
                    self.Delete_All(Each)
                Element_ID = self.Tree.Get(ID)[0]
                if Element_ID!=self.Parent:
                    if len(self.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Element_ID}'", Keys=True))>0:
                        Frame_Data = self.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Element_ID}'", Keys=True)[0]
                    elif len(self.Database.Get(f"SELECT * FROM `Item` WHERE `ID`='{Element_ID}'", Keys=True))>0:
                        Frame_Data = self.Database.Get(f"SELECT * FROM `Item` WHERE `ID`='{Element_ID}'", Keys=True)[0]
                    else:
                        Frame_Data = self.Database.Get(f"SELECT * FROM `Widget` WHERE `ID`='{Element_ID}'", Keys=True)[0]
                    Temp_Root = Frame_Data['Root']
                    Root = Temp_Root
                    while Temp_Root!=self.Parent:
                        Frame_Data = self.Database.Get(f"SELECT * FROM `Frame` WHERE `ID`='{Temp_Root}'", Keys=True)
                        if len(Frame_Data)==1:
                            Frame_Data = Frame_Data[0]
                            Temp_Root = Frame_Data['Root']
                            Root = Temp_Root+'.'+Root
                        else:
                            break
                    if os.path.exists(f"{self.Project_Path}/Data/File/{Element_ID}"):
                        os.remove(f"{self.Project_Path}/Data/File/{Element_ID}")
                    self.Tree.Remove(ID)
                    self.Database.Post(f"DELETE FROM `Frame` WHERE `ID`='{Element_ID}'")
                    self.Database.Post(f"DELETE FROM `Item` WHERE `ID`='{Element_ID}'")
                    self.Database.Post(f"DELETE FROM `Widget` WHERE `ID`='{Element_ID}'")
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))