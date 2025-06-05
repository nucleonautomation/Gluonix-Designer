#################################################################################################################################
# Import Variables
#################################################################################################################################

import time
import _thread
from PIL import Image as Pil_Image

from . import Variable
Root = Variable.Root
Global = Variable.Global

#################################################################################################################################
# Prgramming
#################################################################################################################################
Header = Root.Header
Background = Header.Config_Get('Background')['Background']

# Window Move

Header.Bind(On_Click = lambda E: Start_Window_Move(E), On_Drag = lambda E: Do_Window_Move(E))

def Start_Window_Move(E):
    Header.X, Header.Y = E.x, E.y

def Do_Window_Move(E):
    X, Y = E.x - Header.X, E.y - Header.Y
    Position = Root.Config_Get('Left', 'Top')
    Root.Widget().geometry(f"+{Position['Left']+X}+{Position['Top']+Y}")

# Window Close
Exit = Header.Control.Exit
Exit.Bind(On_Click = lambda E: Root.Close())
Exit.Button.Bind(On_Click = lambda E: Root.Close())
Exit.Bind(On_Hover_In = lambda E: (Exit.Config(Background='#e81123'), Exit.Button.Config(Background='#e81123')))
Exit.Bind(On_Hover_Out = lambda E: (Exit.Config(Background=Background), Exit.Button.Config(Background=Background)))
        
# Window Minimize
Minimize = Header.Control.Minimize
Minimize.Bind(On_Click = lambda E: Root.Minimize())
Minimize.Button.Bind(On_Click = lambda E: Root.Minimize())
Minimize.Bind(On_Hover_In = lambda E: (Minimize.Config(Background='#868686'), Minimize.Button.Config(Background='#868686')))
Minimize.Bind(On_Hover_Out = lambda E: (Minimize.Config(Background=Background), Minimize.Button.Config(Background=Background)))

Header.Bind(On_Double_Click = lambda E: Root.Maximize())

#Top Menu
class Menu_Frame_Item:

    def __init__(self, Frame):
        self.Frame = Frame
        self.Background = self.Frame.Config_Get('Background')['Background']
        self.Frame.Bind(On_Hover_In=lambda E: self.Hover_In(), On_Hover_Out=lambda E: self.Hover_Out())
        self.Frame.Left.Bind(On_Hover_In=lambda E: self.Hover_In(), On_Hover_Out=lambda E: self.Hover_Out())
        self.Frame.Right.Bind(On_Hover_In=lambda E: self.Hover_In(), On_Hover_Out=lambda E: self.Hover_Out())

    def Hover_In(self):
        self.Frame.Config(Background='#0366d6', Foreground='#FFFFFF')
        self.Frame.Left.Config(Background='#0366d6', Foreground='#FFFFFF')
        self.Frame.Right.Config(Background='#0366d6', Foreground='#FFFFFF')
            
    def Hover_Out(self):
        self.Frame.Config(Background=self.Background, Foreground='#000000')
        self.Frame.Left.Config(Background=self.Background, Foreground='#000000')
        self.Frame.Right.Config(Background=self.Background, Foreground='#000000')

class Menu_Frame:

    def __init__(self, Frame):
        self.Frame = Frame
        self.Item = []
        X = 1
        while True:
            if hasattr(self.Frame, f'Frame{X}'):
                self.Item.append(Menu_Frame_Item(getattr(self.Frame, f'Frame{X}')))
                X += 1
            else:
                break
            
    def Hide(self):
        self.Frame.Hide()
            
    def Show(self):
        self.Frame.Show()
            
    def Reset(self):
        for Each in self.Item:
            Each.Hover_Out()
        
File_Frame = Menu_Frame(Root.File_Menu)
        
Edit_Frame = Menu_Frame(Root.Edit_Menu)
            
            
class Menu_Item:
    
    Instances = {}
    Open = False

    def __init__(self, Button, Frame=False):
        self.Button = Button
        self.Frame = Frame
        Menu_Item.Instances[self] = False
        self.Button.Bind(On_Click=lambda E: self.Click(), 
                         On_Hover_In=lambda E: self.Hover_In(), 
                         On_Hover_Out=lambda E: self.Hover_Out())
            
    def Reset(self):
        if self.Frame:
            self.Frame.Hide()
        Menu_Item.Instances[self] = True
        self.Button.Config(Background=Background, Foreground='#FFFFFF')

    def Hover_In(self):
        if Menu_Item.Open:
            for Key, Value in Menu_Item.Instances.items():
                Key.Reset()
            if self.Frame:
                self.Frame.Show()
            self.Button.Config(Background='#FFFFFF', Foreground='#000000')
        else:
            self.Button.Config(Background='#2f363d', Foreground='#FFFFFF')
            
    def Hover_Out(self):
        if Menu_Item.Open:
            if Menu_Item.Instances[self]:
                self.Button.Config(Background='#FFFFFF', Foreground='#000000')
            else:
                self.Button.Config(Background=Background, Foreground='#FFFFFF')
        else:
            self.Button.Config(Background=Background, Foreground='#FFFFFF')

    def Click(self):
        if not Menu_Item.Open:
            Cover_Image = Root.Main.Grab()
            Black_Image = Pil_Image.new('RGB', Cover_Image.size, (0, 0, 0))
            Cover_Image = Pil_Image.blend(Cover_Image, Black_Image, 0.5)
            Root.Main.Cover.Set(Cover_Image)
            Root.Main.Cover.Show()
            Menu_Item.Open = True
            Menu_Item.Instances[self] = True
            self.Button.Config(Background='#FFFFFF', Foreground='#000000')
            if self.Frame:
                self.Frame.Reset()
                self.Frame.Show()
        
File = Menu_Item(Header.File_Menu, File_Frame)
Edit = Menu_Item(Header.Edit_Menu, Edit_Frame)
View = Menu_Item(Header.View_Menu)
Repository = Menu_Item(Header.Repository_Menu)
Branch = Menu_Item(Header.Branch_Menu)
Help = Menu_Item(Header.Help_Menu)

Root.Main.Cover.Config(Pil=True, Top=-1)
Root.Main.Cover.Hide()
Root.Main.Cover.Bind(On_Click = lambda E: Hide_Menu())

def Hide_Menu():
    Root.Main.Cover.Hide()
    Menu_Item.Open = False
    for Key, Value in Menu_Item.Instances.items():
        Key.Reset()