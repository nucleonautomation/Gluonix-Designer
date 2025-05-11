# IMPORT LIBRARIES
import math
import os
from io import BytesIO
from requests import get as requests_get
from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk
import tkinter as TK
from .N_GUI import GUI
from .N_Custom import Event_Bind
from .N_Custom import Event_Bind_Canvas
from .N_Canvas_Line import Canvas_Line
from .N_Canvas_Polyline import Canvas_Polyline
from .N_Canvas_Pie import Canvas_Pie
from .N_Canvas_Arc import Canvas_Arc
from .N_Canvas_Circle import Canvas_Circle
from .N_Canvas_Oval import Canvas_Oval
from .N_Canvas_Rectangle import Canvas_Rectangle
from .N_Canvas_Rectangle2 import Canvas_Rectangle2
from .N_Canvas_Polygon import Canvas_Polygon
from .N_Canvas_Image import Canvas_Image
from .N_Canvas_Text import Canvas_Text

class Canvas:

    def __init__(self, Main, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Canvas"
            try:
                try:
                    TK.Canvas.tagraise = TK.Canvas.tkraise
                    del TK.Canvas.tkraise, TK.Canvas.lift
                except Exception:
                    self.Nothing = False
                self._Config = ['Name', 'Background', 'Light_Background', 'Dark_Background', 'Border_Color', 'Light_Border_Color', 'Dark_Border_Color', 'Border_Size', 'Resize_Width', 'Resize', 'Resize_Height', 'Move', 'Move_Left', 'Move_Top', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height', 'Radius', 'Shadow_Size', 'Shadow_Color', 'Light_Shadow_Color', 'Dark_Shadow_Color', 'Shadow_Full', 'Hover_Background', 'Light_Hover_Background', 'Dark_Hover_Background', 'Hover_Border_Color', 'Light_Hover_Border_Color', 'Dark_Hover_Border_Color', 'Hover_Shadow_Color', 'Light_Hover_Shadow_Color', 'Dark_Hover_Shadow_Color']
                self._Initialized = False
                self._Name = False
                self._Last_Name = False
                self._Widget = []
                self._Resize_Font, self._Resize, self._Resize_Width, self._Resize_Height, self._Move, self._Move_Left, self._Move_Top = False, True, True, True, True, True, True
                self._Popup = False
                self._Display = True
                self._Main = Main
                self._Frame = TK.Canvas(self._Main._Frame)
                self._Border_Color = '#000000'
                self._Border_Size = 0
                self._Border = []
                self._Shadow_Size = 0
                self._Shadow_Color = '#d5d8dc'
                self._Shadow_Full = True
                self._Radius = 0
                self._Hover_Background = False
                self._Hover_Border_Color = False
                self._Hover_Shadow_Color = False
                self._Last_Background = False
                self._Last_Border_Color = False
                self._Last_Shadow_Color = False
                self._Rounded = []
                self._Background = self._Main._Background
                self._Background_Main = True
                self._On_Resize = False
                self._Resizable = self._Main._Resizable
                self._On_Show = False
                self._On_Hide = False
                self._On_Hover_In = False
                self._On_Hover_Out = False
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Canvas[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Canvas[]"
    
    def Copy(self, Name=False, Main=False):
        try:
            if not Main:
                Main = self._Main
            Instance = type(self)(Main)
            for Key in self._Config:
                setattr(Instance, "_"+Key, getattr(self, "_"+Key))
            if Name:
                setattr(Instance, "_Name", Name)
            Instance.Create()
            for Each in self._Widget:
                Each.Copy(Main=Instance)
            return Instance
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Copy -> {E}")
        
    def Delete(self):
        try:
            self.Clear()
            self._Main._Widget.remove(self)
            self._Frame.delete(self._Border)
            self._Frame.destroy()
            if self:
                del self
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete -> {E}")

    def Clear(self):
        try:
            for Each in self._Widget:
                Each.Delete()
            for Each in self._Frame.find_all():
                self._Frame.delete(Each)
            self.Rounded()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Clear -> {E}")

    def Refresh(self):
        try:
            self._Frame.update_idletasks()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Refresh -> {E}")
            
    def Hide(self):
        try:
            self._Frame.place_forget()
            self._Display = False
            if self._On_Hide:
                self._On_Hide()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Hide -> {E}")
            
    def Show(self):
        try:
            self._Display = True
            if self._Resizable:
                self.Resize()
            else:
                self.Display()
            if self._On_Show:
                self._On_Show()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Show -> {E}")
            
    def Display(self):
        try:
            self._Frame.place(x=self._Left_Current, y=self._Top_Current, width=self._Width_Current, height=self._Height_Current)
            try:
                self._Frame.tagraise()
            except Exception:
                self.Nothing = False
            self._Display = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Display -> {E}")
            
    def Focus(self):
        try:
            self._Widget.focus_set()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Focus -> {E}")
    
    def Grab(self, Path=False):
        try:
            return self._GUI.Grab_Widget(Path=Path, Widget=self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Grab -> {E}")
            
    def Widget(self):
        try:
            return self._Frame
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Widget -> {E}")
            
    def Bind(self, **Input):
        try:
            if 'On_Show' in Input:
                self._On_Show = Input['On_Show']
            if 'On_Hide' in Input:
                self._On_Hide = Input['On_Hide']
            if "On_Resize" in Input:
                self._On_Resize = Input["On_Resize"]
            if 'On_Hover_In' in Input:
                self._On_Hover_In = Input['On_Hover_In']
            Input['On_Hover_In'] = lambda E: self.On_Hover_In(E)
            if 'On_Hover_Out' in Input:
                self._On_Hover_Out = Input['On_Hover_Out']
            Input['On_Hover_Out'] = lambda E: self.On_Hover_Out(E)
            Event_Bind(self._Frame, **Input)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind -> {E}")
            
    def Bind_Item(self, Item, **Input):
        try:
            Event_Bind_Canvas(self._Frame, Item, **Input)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind_Item -> {E}")
            
    def On_Hover_In(self, E):
        try:
            Config = {}
            if self._Hover_Background:
                self._Last_Background = self._Background
                Config['Background'] = self._Hover_Background
            if self._Hover_Border_Color:
                self._Last_Border_Color = self._Border_Color
                Config['Border_Color'] = self._Hover_Border_Color
            if self._Hover_Shadow_Color:
                self._Last_Shadow_Color = self._Shadow_Color
                Config['Shadow_Color'] = self._Hover_Shadow_Color
            if len(Config)>0:
                self.Config(**Config)
            if self._On_Hover_In:
                self._On_Hover_In(E)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Hover_In -> {E}")
            
    def On_Hover_Out(self, E):
        try:
            Config = {}
            if self._Hover_Background and self._Last_Background:
                Config['Background'] = self._Last_Background
            if self._Hover_Border_Color and self._Last_Border_Color:
                Config['Border_Color'] = self._Last_Border_Color
            if self._Hover_Shadow_Color and self._Last_Shadow_Color:
                Config['Shadow_Color'] = self._Last_Shadow_Color
            if len(Config)>0:
                self.Config(**Config)
            if self._On_Hover_Out:
                self._On_Hover_Out(E)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Hover_Out -> {E}")
            
    def Config_Get(self, *Input):
        try:
            Return = {}
            for Each in self._Config:
                if Each in Input:
                    Return[Each] = getattr(self, "_"+Each)
            return Return
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Config_Get -> {E}")
                
    def Config(self, **Input):
        try:
            Run = False
            for Each in self._Config:
                if Each in Input:
                    Value = Input[Each]
                    setattr(self, "_"+Each, Value)
                    Run = True
            if self._Initialized and Run:
                self.Create()
            if "Background" in Input:
                self._Background_Main = not bool(Input["Background"])
                for Each in self._Widget:
                    try:
                        if Each._Background_Main:
                            Each.Config(Background=False)
                        if hasattr(Each, '_Radius'):
                            if Each._Radius>0:
                                Each.Config(Radius=Each._Radius)
                    except Exception:
                        self.Nothing = False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Config -> {E}")
            
    def Position(self, Left=None, Top=None):
        try:
            if Left is not None:
                self._Left = Left
            if Top is not None:
                self._Top = Top
            if Left is not None or Top is not None:
                self.Relocate()
            Left = self._Frame.winfo_x()
            Top = self._Frame.winfo_y()
            return [Left, Top]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Position -> {E}")
            
    def Size(self, Width=False, Height=False):
        try:
            if Width:
                self._Width = Width
            if Height:
                self._Height = Height
            if Width or Height:
                self.Resize()
            return [self._Frame.winfo_width(), self._Frame.winfo_height()]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Size -> {E}")
        
    def Locate(self, Width, Height, Left, Top):
        try:
            Width = self._Width*(Width/100)
            Height = self._Height*(Height/100)
            Left = self._Width*(Left/100)
            Top = self._Height*(Top/100)
            return [Width, Height, Left, Top]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Locate -> {E}")
        
    def Locate_Reverse(self, Width, Height, Left, Top):
        try:
            Width = round((Width/self._Width)*100, 3)
            Height = round((Height/self._Height)*100, 3)
            Left =  round((Left/self._Width)*100, 3)
            Top =  round((Top/self._Height)*100, 3)
            return [Width, Height, Left, Top]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Locate_Reverse -> {E}")
            
    def Create(self):
        try:
            if not self._Background:
                self._Background = self._Main._Background
                if not hasattr(self, "_Light_Background"):
                    setattr(self, "_Light_Background", self._Background)
                if not hasattr(self, "_Dark_Background"):
                    setattr(self, "_Dark_Background", self._GUI.Invert(self._Background))
            Temp_Background = self._Background
            if not self._Initialized:
                self._GUI.Initiate_Colors(self)
                self._Width_Current, self._Height_Current, self._Left_Current, self._Top_Current = self._Width, self._Height, self._Left, self._Top
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                Event_Bind(self._Frame, On_Hover_In=lambda E: self.On_Hover_In(E), On_Hover_Out=lambda E: self.On_Hover_Out(E))
                self._Initialized = True
            if self._Radius:
                Temp_Background = self._Main._Background
            self._Frame.config(background=Temp_Background, width=self._Width_Current, height=self._Height_Current, highlightthickness=0)
            self.Rounded()
            self.Resize(Trigger=False)
            if self._Name!=self._Last_Name:
                if self._Last_Name:
                    if self._Last_Name in self._Main.__dict__:
                        del self._Main.__dict__[self._Last_Name]
                if self._Name:
                    self._Main.__dict__[self._Name] = self
                self._Last_Name = self._Name
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Create -> {E}")
            
    def Rounded(self):
        try:
            for Each in self._Rounded:
                self._Frame.delete(Each)
            self._Rounded = []
            Radius = min(self._Radius, self._Width_Current / 2, self._Height_Current / 2)
            X1 = self._Shadow_Size
            Y1 = self._Shadow_Size
            X2 = self._Width_Current-self._Shadow_Size-1
            Y2 = self._Height_Current-self._Shadow_Size-1
            Reducer = 0
            if not self._Shadow_Full:
                Reducer = self._Shadow_Size
            for i in range(self._Shadow_Size):
                Offset = self._Shadow_Size-i
                Intensity = (self._Shadow_Size-i) / self._Shadow_Size
                Shadow_Fill = self.Fade(self._Shadow_Color, Intensity)
                self._Rounded.append(self.Round_Rectangle(X1-Offset+(Reducer/2), Y1-Offset+Reducer, X2+Offset-(Reducer/2), Y2+Offset, Radius, outline=Shadow_Fill, fill=Shadow_Fill, smooth=True))
            self._Rounded.append(self.Round_Rectangle(X1, Y1, X2, Y2, Radius, outline=self._Border_Color, fill=self._Border_Color, smooth=True))
            X1 = self._Border_Size+self._Shadow_Size
            Y1 = self._Border_Size+self._Shadow_Size
            X2 = self._Width_Current-self._Border_Size-self._Shadow_Size-1
            Y2 = self._Height_Current-self._Border_Size-self._Shadow_Size-1
            self._Rounded.append(self.Round_Rectangle(X1, Y1, X2, Y2, Radius, outline=self._Background, fill=self._Background, smooth=True))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rounded -> {E}")
            
    def RGB(self, Color):
        try:
            return [int(Color[i:i+2], 16) for i in (1, 3, 5)]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> RGB -> {E}")
    
    def HEX(self, Color):
        try:
            return f'#{Color[0]:02x}{Color[1]:02x}{Color[2]:02x}'
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> HEX -> {E}")

    def Fade(self, Color, Intensity):
        try:
            R1, G1, B1 = self.RGB(Color)
            R2, G2, B2 = self.RGB(self._Main._Background)
            R = int(R1 + (R2 - R1) * Intensity)
            G = int(G1 + (G2 - G1) * Intensity)
            B = int(B1 + (B2 - B1) * Intensity)
            return self.HEX([R, G, B])
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> FADE -> {E}")
            
    def Points(self, Radius):
        try:
            Radius = math.ceil(Radius)
            if Radius<1:
                Radius = 1
            for i in range(Radius + 1):
                Angle = math.pi * (i / Radius) * 0.5
                X = (math.cos(Angle) - 1) * Radius
                Y = (math.sin(Angle) - 1) * Radius
                yield (X, Y)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Points -> {E}")
            
    def Round_Rectangle(self, X1, Y1, X2, Y2, Radius, **Args):
        try:
            if Radius>1:
                Points = []
                Cos_Sin_R = tuple(self.Points(Radius))
                for Cos_R, Sin_R in Cos_Sin_R:
                    Points.append((X2 + Sin_R, Y1 - Cos_R))
                for Cos_R, Sin_R in Cos_Sin_R:
                    Points.append((X2 + Cos_R, Y2 + Sin_R))
                for Cos_R, Sin_R in Cos_Sin_R:
                    Points.append((X1 - Sin_R, Y2 + Cos_R))
                for Cos_R, Sin_R in Cos_Sin_R:
                    Points.append((X1 - Cos_R, Y1 - Sin_R))
                return self._Frame.create_polygon(Points, **Args)
            else:
                del Args['smooth']
                return self._Frame.create_rectangle(X1, Y1, X2, Y2, **Args)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Round_Rectangle -> {E}")

    def Adjustment(self):
        try:
            Width_Difference = self._Main._Width_Current - self._Main._Width
            Width_Ratio = self._Width / (self._Main._Width - self._Main._Border_Size*2)
            self._Width_Adjustment = Width_Difference * Width_Ratio
            Height_Difference = self._Main._Height_Current - self._Main._Height
            Height_Ratio = self._Height / (self._Main._Height - self._Main._Border_Size*2)
            self._Height_Adjustment = Height_Difference * Height_Ratio
            Left_Ratio = self._Left / self._Main._Width
            self._Left_Adjustment = Width_Difference * Left_Ratio
            Top_Ratio = self._Top / self._Main._Height
            self._Top_Adjustment = Height_Difference * Top_Ratio
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Adjustment -> {E}")
            
    def Relocate(self, Direct=False):
        try:
            self.Adjustment()
            if Direct or (self._Resize and self._Resize_Width):
                self._Width_Current = self._Width + self._Width_Adjustment
            else:
                self._Width_Current = self._Width
            if Direct or (self._Resize and self._Resize_Height):
                self._Height_Current = self._Height + self._Height_Adjustment
            else:
                self._Height_Current = self._Height
            if Direct or (self._Move and self._Move_Left):
                self._Left_Current = self._Left + self._Left_Adjustment
            else:
                self._Left_Current = self._Left
            if Direct or (self._Move and self._Move_Top):
                self._Top_Current = self._Top + self._Top_Adjustment
            else:
                self._Top_Current = self._Top
            self.Rounded()
            if self._Display:
                self.Display()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Relocate -> {E}")
            
    def Resize(self, Trigger=True):
        try:
            self.Relocate()
            for Each in self._Widget:
                try:
                    if Each._Display:
                        Each.Resize()
                except Exception:
                    self.Nothing = False
            if self._On_Resize and Trigger:
                self._On_Resize()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Resize -> {E}")

    def Hide_Item(self, Item=False):
        try:
            if Item:
                self._Frame.itemconfigure(Item, state='hidden')
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Hide_Item -> {E}")

    def Show_Item(self, Item=False):
        try:
            if Item:
                self._Frame.itemconfigure(Item, state='normal')
                self._Frame.tag_raise(Item)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Show_Item -> {E}")
    
    def Delete_Item(self, Item=False):
        try:
            if Item:
                self._Frame.delete(Item)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete_Item -> {E}")
    
    def Delete_All(self):
        try:
            self._Frame.delete('all')
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete_All -> {E}")
            
            
    def Find_Near(self, X, Y):
        try:
            return self._Frame.find_closest(X, Y)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Find_Near -> {E}")
            
    def Find_Overlap(self, X1, Y1, X2, Y2):
        try:
            return self._Frame.find_overlapping(X1, Y1, X2, Y2)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Find_Overlap -> {E}")
            
    def Line(self):
        try:
            return Canvas_Line(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Line -> {E}")
            
    def Polyline(self):
        try:
            return Canvas_Polyline(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Polyline -> {E}")
                
    def Pie(self):
        try:
            return Canvas_Pie(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Pie -> {E}")
                
    def Arc(self):
        try:
            return Canvas_Arc(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Arc -> {E}")
                
    def Circle(self):
        try:
            return Canvas_Circle(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Circle -> {E}")
                
    def Oval(self):
        try:
            return Canvas_Oval(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Oval -> {E}")
            
    def Polygon(self):
        try:
            return Canvas_Polygon(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Polygon -> {E}")
                
    def Rectangle(self):
        try:
            return Canvas_Rectangle(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rectangle -> {E}")
                
    def Rectangle2(self):
        try:
            return Canvas_Rectangle2(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rectangle2 -> {E}")
                
    def Image(self):
        try:
            return Canvas_Image(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Image -> {E}")
            
    def Text(self):
        try:
            return Canvas_Text(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Text -> {E}")