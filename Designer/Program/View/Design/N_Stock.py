################################################################################################################################
#Stock
################################################################################################################################
#Default Libraries
import inspect

#Program
from .N_Stock_Frame import Stock_Frame
from .N_Stock_Canvas import Stock_Canvas
from .N_Stock_Scroll import Stock_Scroll
from .N_Stock_Label import Stock_Label
from .N_Stock_Roubel import Stock_Roubel
from .N_Stock_Label_Lite import Stock_Label_Lite
from .N_Stock_Bar import Stock_Bar
from .N_Stock_Button import Stock_Button
from .N_Stock_Button_Lite import Stock_Button_Lite
from .N_Stock_Compound import Stock_Compound
from .N_Stock_Compound_Lite import Stock_Compound_Lite
from .N_Stock_Image import Stock_Image
from .N_Stock_Image_Lite import Stock_Image_Lite
from .N_Stock_Line import Stock_Line
from .N_Stock_Entry import Stock_Entry
from .N_Stock_List import Stock_List
from .N_Stock_Select import Stock_Select
from .N_Stock_Spinner import Stock_Spinner
from .N_Stock_Scale import Stock_Scale
from .N_Stock_Check import Stock_Check
from .N_Stock_Radio import Stock_Radio
from .N_Stock_Switch import Stock_Switch
from .N_Stock_Text import Stock_Text
from .N_Stock_Tree import Stock_Tree
from .N_Stock_Canvas_Line import Stock_Canvas_Line
from .N_Stock_Canvas_Rectangle import Stock_Canvas_Rectangle
from .N_Stock_Canvas_Pie import Stock_Canvas_Pie
from .N_Stock_Canvas_Arc import Stock_Canvas_Arc
from .N_Stock_Canvas_Circle import Stock_Canvas_Circle
from .N_Stock_Canvas_Oval import Stock_Canvas_Oval
from .N_Stock_Canvas_Image import Stock_Canvas_Image
from .N_Stock_Canvas_Text import Stock_Canvas_Text

class Stock:
    def __init__(self, Global, Design):
        try:
            self.Global = Global
            self.Design = Design
            self.Widget = []
            
            #Line
            Fixture = self.Design.Frame.Locate(0.5, 90, 28.5, 10)
            self.Line = self.Global['Gluonix'].Line(self.Design.Frame)
            self.Line.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Line.Config(Border_Size=0, Display=True)
            self.Line.Config(Resize=False, Move=False)
            self.Line.Create()
            self.Design.Widget.append(self.Line)
            
            #Frame
            Fixture = self.Design.Frame.Locate(29.5, 90, 0, 10)
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
            self.Label.Config(Resize=True, Move=True)
            self.Label.Set(' ELEMENTS')
            self.Label.Create()
            
            #Frame
            Fixture = self.Frame.Locate(100, 95, 0, 5)
            self.Scroll = self.Global['Gluonix'].Scroll(self.Frame)
            self.Scroll.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Scroll.Config(Background='#FFFFFF', Border_Size=0, Display=True)
            self.Scroll.Config(Resize=False, Move=False)
            self.Scroll.Create()
            
            #Objects
            
            self.Top = 3
            self.Left = 2.5
            self.Center = 35
            self.Right = 67.5
            
            # Containers
            
            #Label
            Fixture = self.Scroll.Locate(100, 3, 0, self.Top)
            self.Label_Container = self.Global['Gluonix'].Label(self.Scroll)
            self.Label_Container.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Label_Container.Config(Background='#FFFFFF', Border_Size=0, Display=True)
            self.Label_Container.Config(Foreground='#000000', Font_Size=12, Font_Weight='normal', Align='w')
            self.Label_Container.Config(Resize=True, Move=True)
            self.Label_Container.Set(' CONTAINER')
            self.Label_Container.Create()
            
            #Stock Frame
            self.Top += 4
            self.Stock_Frame = Stock_Frame(self.Global, self, self.Left, self.Top)
            
            #Stock Canvas
            self.Stock_Canvas = Stock_Canvas(self.Global, self, self.Center, self.Top)
            
            #Stock Scroll
            self.Stock_Scroll = Stock_Scroll(self.Global, self, self.Right, self.Top)
            
            # Widget
            
            #Label
            self.Top += 7
            Fixture = self.Scroll.Locate(100, 3, 0, self.Top)
            self.Label_Widget = self.Global['Gluonix'].Label(self.Scroll)
            self.Label_Widget.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Label_Widget.Config(Background='#FFFFFF', Border_Size=0, Display=True)
            self.Label_Widget.Config(Foreground='#000000', Font_Size=12, Font_Weight='normal', Align='w')
            self.Label_Widget.Config(Resize=True, Move=True)
            self.Label_Widget.Set(' WIDGET')
            self.Label_Widget.Create()
            
            #Stock Line
            self.Top += 4
            self.Stock_Line = Stock_Line(self.Global, self, self.Left, self.Top)
            
            #Stock Label
            self.Stock_Label = Stock_Label(self.Global, self, self.Center, self.Top)
            
            #Stock Button
            self.Stock_Button = Stock_Button(self.Global, self, self.Right, self.Top)
            
            #Stock Image
            self.Top += 6
            self.Stock_Image = Stock_Image(self.Global, self, self.Left, self.Top)
            
            #Stock Compound
            self.Stock_Compound = Stock_Compound(self.Global, self, self.Center, self.Top)
            
            #Stock Text
            self.Stock_Text = Stock_Text(self.Global, self, self.Right, self.Top)
            
            #Stock Entry
            self.Top += 6
            self.Stock_Entry = Stock_Entry(self.Global, self, self.Left, self.Top)
            
            #Stock Spinner
            self.Stock_Spinner = Stock_Spinner(self.Global, self, self.Center, self.Top)
            
            #Stock Select
            self.Stock_Select = Stock_Select(self.Global, self, self.Right, self.Top)
            
            #Stock Bar
            self.Top += 6
            self.Stock_Bar = Stock_Bar(self.Global, self, self.Left, self.Top)
            
            #Stock List
            self.Stock_List = Stock_List(self.Global, self, self.Center, self.Top)
            
            #Stock Scale
            self.Stock_Scale = Stock_Scale(self.Global, self, self.Right, self.Top)
            
            #Stock Check
            self.Top += 6
            self.Stock_Check = Stock_Check(self.Global, self, self.Left, self.Top)
            
            #Stock Radio
            self.Stock_Radio = Stock_Radio(self.Global, self, self.Center, self.Top)
            
            #Stock Switch
            self.Stock_Switch = Stock_Switch(self.Global, self, self.Right, self.Top)
            
            #Stock Tree
            self.Top += 6
            self.Stock_Tree = Stock_Tree(self.Global, self, self.Left, self.Top)
            
            #Stock Roubel
            self.Stock_Roubel = Stock_Roubel(self.Global, self, self.Center, self.Top)
            
            # Lite
            
            #Label
            self.Top += 7
            Fixture = self.Scroll.Locate(100, 3, 0, self.Top)
            self.Label_Lite = self.Global['Gluonix'].Label(self.Scroll)
            self.Label_Lite.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Label_Lite.Config(Background='#FFFFFF', Border_Size=0, Display=True)
            self.Label_Lite.Config(Foreground='#000000', Font_Size=12, Font_Weight='normal', Align='w')
            self.Label_Lite.Config(Resize=True, Move=True)
            self.Label_Lite.Set(' LITE WIDGET')
            self.Label_Lite.Create()
            
            #Stock Label Lite
            self.Top += 4
            self.Stock_Label_Lite = Stock_Label_Lite(self.Global, self, self.Left, self.Top)
            
            #Stock Image Lite
            self.Stock_Image_Lite = Stock_Image_Lite(self.Global, self, self.Center, self.Top)
            
            #Stock Compound Lite
            self.Stock_Compound_Lite = Stock_Compound_Lite(self.Global, self, self.Right, self.Top)
            
            #Stock Button Lite
            self.Top += 6
            self.Stock_Button_Lite = Stock_Button_Lite(self.Global, self, self.Left, self.Top)
            
            # Lite
            
            #Label
            self.Top += 7
            Fixture = self.Scroll.Locate(100, 3, 0, self.Top)
            self.Label_Lite = self.Global['Gluonix'].Label(self.Scroll)
            self.Label_Lite.Config(Width=Fixture[0], Height=Fixture[1], Left=Fixture[2], Top=Fixture[3])
            self.Label_Lite.Config(Background='#FFFFFF', Border_Size=0, Display=True)
            self.Label_Lite.Config(Foreground='#000000', Font_Size=12, Font_Weight='normal', Align='w')
            self.Label_Lite.Config(Resize=True, Move=True)
            self.Label_Lite.Set(' CANVAS ITEM')
            self.Label_Lite.Create()
            
            #Stock Canvas Line
            self.Top += 4
            self.Stock_Canvas_Line = Stock_Canvas_Line(self.Global, self, self.Left, self.Top)
            
            #Stock Canvas Rectangle
            self.Stock_Canvas_Rectangle = Stock_Canvas_Rectangle(self.Global, self, self.Center, self.Top)
            
            #Stock Canvas Circle
            self.Stock_Canvas_Circle = Stock_Canvas_Circle(self.Global, self, self.Right, self.Top)
            
            #Stock Canvas Oval
            self.Top += 6
            self.Stock_Canvas_Oval = Stock_Canvas_Oval(self.Global, self, self.Left, self.Top)
            
            #Stock Canvas Image
            self.Stock_Canvas_Image = Stock_Canvas_Image(self.Global, self, self.Center, self.Top)
            
            #Stock Canvas Text
            self.Stock_Canvas_Text = Stock_Canvas_Text(self.Global, self, self.Right, self.Top)
            
            #Stock Canvas Arc
            self.Top += 6
            self.Stock_Canvas_Arc = Stock_Canvas_Arc(self.Global, self, self.Left, self.Top)
            
            #Stock Canvas Pie
            self.Stock_Canvas_Pie = Stock_Canvas_Pie(self.Global, self, self.Center, self.Top)
            
            #Update Scroll
            #self.Scroll.Update(self.Stock_Button_Lite.Label)
                   
        except Exception as E:
            self.Global['Error'](__class__.__name__+" -> "+inspect.currentframe().f_code.co_name+" -> "+str(E))