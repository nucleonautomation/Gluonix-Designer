################################################################################################################################
#Configure
################################################################################################################################
#Default Libraries
import inspect

#Program
from .N_Configure_Frame import Configure_Frame
from .N_Configure_Canvas import Configure_Canvas
from .N_Configure_Scroll import Configure_Scroll
from .N_Configure_Label import Configure_Label
from .N_Configure_Roubel import Configure_Roubel
from .N_Configure_Label_Lite import Configure_Label_Lite
from .N_Configure_Bar import Configure_Bar
from .N_Configure_Button import Configure_Button
from .N_Configure_Button_Lite import Configure_Button_Lite
from .N_Configure_Compound import Configure_Compound
from .N_Configure_Compound_Lite import Configure_Compound_Lite
from .N_Configure_Image import Configure_Image
from .N_Configure_Image_Lite import Configure_Image_Lite
from .N_Configure_Line import Configure_Line
from .N_Configure_Entry import Configure_Entry
from .N_Configure_List import Configure_List
from .N_Configure_Select import Configure_Select
from .N_Configure_Spinner import Configure_Spinner
from .N_Configure_Scale import Configure_Scale
from .N_Configure_Check import Configure_Check
from .N_Configure_Radio import Configure_Radio
from .N_Configure_Switch import Configure_Switch
from .N_Configure_Text import Configure_Text
from .N_Configure_Tree import Configure_Tree
from .N_Configure_Canvas_Line import Configure_Canvas_Line
from .N_Configure_Canvas_Rectangle import Configure_Canvas_Rectangle
from .N_Configure_Canvas_Pie import Configure_Canvas_Pie
from .N_Configure_Canvas_Arc import Configure_Canvas_Arc
from .N_Configure_Canvas_Circle import Configure_Canvas_Circle
from .N_Configure_Canvas_Oval import Configure_Canvas_Oval
from .N_Configure_Canvas_Image import Configure_Canvas_Image
from .N_Configure_Canvas_Text import Configure_Canvas_Text

class Configure:
    def __init__(self, Global, Design):
        try:
            self.Global = Global
            self.Design = Design
            self.Widget= []
            self.Current = False
            
            #Frame
            Fixture = self.Design.Frame.Locate(40, 90, 60, 10)
            self.Frame = self.Global['Gluonix'].Frame(self.Design.Frame)
            self.Frame.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Frame.Config(Background='#FFFFFF', Border_Size=0, Display=True)
            self.Frame.Config(Resize=False, Move=False)
            self.Frame.Create()
            self.Design.Widget.append(self.Frame)
            
            #Label
            Fixture = self.Frame.Locate(100, 3, 0, 1)
            self.Label = self.Global['Gluonix'].Label(self.Frame)
            self.Label.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Label.Config(Background='#FFFFFF', Border_Size=0, Display=True)
            self.Label.Config(Foreground='#000000', Font_Size=16, Font_Weight='normal', Align='w')
            self.Label.Config(Resize=False, Move=False)
            self.Label.Set(' CONFIGURE')
            self.Label.Create()
            
            #Configure Frame
            self.Configure_Frame = Configure_Frame(self.Global, self)
            
            #Configure Canvas
            self.Configure_Canvas = Configure_Canvas(self.Global, self)
            
            #Configure Scroll
            self.Configure_Scroll = Configure_Scroll(self.Global, self)
            
            #Configure Label
            self.Configure_Label = Configure_Label(self.Global, self)
            
            #Configure Roubel
            self.Configure_Roubel = Configure_Roubel(self.Global, self)
            
            #Configure Bar
            self.Configure_Bar = Configure_Bar(self.Global, self)
            
            #Configure Button
            self.Configure_Button = Configure_Button(self.Global, self)
            
            #Configure Compound
            self.Configure_Compound = Configure_Compound(self.Global, self)
            
            #Configure Image
            self.Configure_Image = Configure_Image(self.Global, self)
            
            #Configure Line
            self.Configure_Line = Configure_Line(self.Global, self)
            
            #Configure Entry
            self.Configure_Entry = Configure_Entry(self.Global, self)
            
            #Configure List
            self.Configure_List = Configure_List(self.Global, self)
            
            #Configure Select
            self.Configure_Select = Configure_Select(self.Global, self)
            
            #Configure Spinner
            self.Configure_Spinner = Configure_Spinner(self.Global, self)
            
            #Configure Scale
            self.Configure_Scale = Configure_Scale(self.Global, self)
            
            #Configure Check
            self.Configure_Check = Configure_Check(self.Global, self)
            
            #Configure Radio
            self.Configure_Radio = Configure_Radio(self.Global, self)
            
            #Configure Switch
            self.Configure_Switch = Configure_Switch(self.Global, self)
            
            #Configure Text
            self.Configure_Text = Configure_Text(self.Global, self)
            
            #Configure Text
            self.Configure_Tree = Configure_Tree(self.Global, self)
            
            #Configure Text
            self.Configure_Label_Lite = Configure_Label_Lite(self.Global, self)
            
            #Configure Text
            self.Configure_Compound_Lite = Configure_Compound_Lite(self.Global, self)
            
            #Configure Text
            self.Configure_Image_Lite = Configure_Image_Lite(self.Global, self)
            
            #Configure Text
            self.Configure_Button_Lite = Configure_Button_Lite(self.Global, self)
            
            #Configure Canvas Line
            self.Configure_Canvas_Line = Configure_Canvas_Line(self.Global, self)
            
            #Configure Canvas Rectangle
            self.Configure_Canvas_Rectangle = Configure_Canvas_Rectangle(self.Global, self)
            
            #Configure Canvas Arc
            self.Configure_Canvas_Pie = Configure_Canvas_Pie(self.Global, self)
            
            #Configure Canvas Arc
            self.Configure_Canvas_Arc = Configure_Canvas_Arc(self.Global, self)
            
            #Configure Canvas Circle
            self.Configure_Canvas_Circle = Configure_Canvas_Circle(self.Global, self)
            
            #Configure Canvas Oval
            self.Configure_Canvas_Oval = Configure_Canvas_Oval(self.Global, self)
            
            #Configure Canvas Image
            self.Configure_Canvas_Image = Configure_Canvas_Image(self.Global, self)
            
            #Configure Canvas Text
            self.Configure_Canvas_Text = Configure_Canvas_Text(self.Global, self)
            
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Hide_All(self):
        try:
            self.Current = False
            for Each in self.Widget:
                Each.Frame.Top()
                Each.Frame.Hide()
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))
            
    def Reset_All(self):
        try:
            for Each in self.Widget:
                Each.ID = False
                Each.Root = False
                Each.Root_ID = False
                Each.Element = False
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))