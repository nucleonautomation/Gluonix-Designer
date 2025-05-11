# IMPORT LIBRARIES
import math
import os
from io import BytesIO
from requests import get as requests_get
from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk
import tkinter as TK
from .N_GUI import GUI
from .N_Frame import Frame
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

class Scroll:

    def __init__(self, Main, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Scroll"
            try:
                self._Config = ['Name', 'Background', 'Light_Background', 'Dark_Background', 'Border_Color', 'Light_Border_Color', 'Dark_Border_Color', 'Border_Size', 'Resize_Width', 'Resize', 'Resize_Height', 'Move', 'Move_Left', 'Move_Top', 'Popup', 'Left', 'Top', 'Width', 'Height', 'Scrollbar', 'Vertical', 'Horizontal', 'Last']
                self._Initialized = False
                self._Name = False
                self._Last_Name = False
                self._Widget = []
                self._Resize_Font, self._Resize, self._Resize_Width, self._Resize_Height, self._Move, self._Move_Left, self._Move_Top = False, True, True, True, True, True, True
                self._Popup = False
                self._Display = True
                self._Main = Main
                self._Frame_Canvas = Frame(self._Main)
                self._Canvas_Scroll = TK.Canvas(self._Frame_Canvas._Frame)
                self._Scrollbar_Vertical = TK.Scrollbar(self._Frame_Canvas._Frame)
                self._Scrollbar_Horizontal = TK.Scrollbar(self._Frame_Canvas._Frame)
                self._Frame = TK.Canvas(self._Canvas_Scroll)
                self._Frame_Scroll = False
                self._Border_Color = '#000000'
                self._Border_Size = 0
                self._Background = self._Main._Background
                self._Background_Main = True
                self._Scrollbar = 25
                self._Vertical = False
                self._Horizontal = False
                self._Width_Frame = False
                self._Height_Frame = False
                self._Last = False
                self._On_Resize = False
                self._Resizable = self._Main._Resizable
                self._On_Show = False
                self._On_Hide = False
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Scroll[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Scroll[]"
    
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
            self._Main._Widget.remove(self)
            self._Frame.destroy()
            self._Scrollbar_Vertical.destroy()
            self._Scrollbar_Horizontal.destroy()
            self._Canvas_Scroll.destroy()
            self._Frame_Canvas.Delete()
            if self:
                del self
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete -> {E}")

    def Clear(self):
        try:
            for Each in self._Widget:
                Each.Delete()
            for Each in self._Frame.winfo_children():
                Each.destroy()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Clear -> {E}")

    def Refresh(self):
        try:
            self._Frame.update_idletasks()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Refresh -> {E}")
            
    def Hide(self):
        try:
            self._Frame_Canvas.Hide()
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
            self._Frame_Canvas.Show()
            self._Display = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Display -> {E}")
    
    def Grab(self, Path=False):
        try:
            return self._GUI.Grab_Widget(Path=Path, Widget=self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Grab -> {E}")
            
    def Top(self):
        try:
            self._Canvas_Scroll.yview_moveto(0)
            self._Canvas_Scroll.xview_moveto(0)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Top -> {E}")
            
    def Reset(self):
        try:
            self.Top()
            self._Width_Frame = self._Width
            self._Height_Frame = self._Height
            self._Frame.config(width=self._Width_Frame, height=self._Height_Frame)
            self._Scrollbar_Horizontal.place_forget()
            self._Scrollbar_Vertical.place_forget()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Reset -> {E}")
            
    def Scroll(self, E):
        try:
            if E.delta:
                self._Canvas_Scroll.yview_scroll(int(-1*(E.delta/120)), "units")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Scroll -> {E}")
            
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
            Event_Bind(self._Frame, **Input)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind -> {E}")
            
    def Bind_Item(self, Item, **Input):
        try:
            Event_Bind_Canvas(self._Frame, Item, **Input)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind_Item -> {E}")
            
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
            self._Frame_Canvas.Config(**Input)
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
                self.Resize()
            return self._Frame_Canvas.Position(Left, Top)
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
            return self._Frame_Canvas.Size(Width, Height)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Size -> {E}")
        
    def Locate(self, Width, Height, Left, Top):
        try:
            Width = self._Width*(Width/100)
            Height = self._Height*(Height/100)
            Left = self._Width*(Left/100)-self._Border_Size
            Top = self._Height*(Top/100)-self._Border_Size
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
            if not self._Initialized:
                self._GUI.Initiate_Colors(self)
                self._Width_Current, self._Width_Frame, self._Height_Current, self._Height_Frame, self._Left_Current, self._Top_Current = self._Width, self._Width, self._Height, self._Height, self._Left, self._Top
                self._Frame_Canvas.Config(Width=self._Width_Current, Height=self._Height_Current, Left=self._Left_Current, Top=self._Top_Current)
                self._Frame_Canvas.Config(Background=self._Background, Border_Size=self._Border_Size, Border_Color=self._Border_Color)
                self._Frame_Canvas.Create()
                self._Frame.bind("<MouseWheel>", self.Scroll)
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                self._Initialized = True
            self._Canvas_Scroll.config(background=self._Background, width=self._Width_Frame, height=self._Height_Frame, highlightthickness=0)
            self._Scrollbar_Vertical.config(orient="vertical", command=self._Canvas_Scroll.yview, width=self._Scrollbar)
            self._Scrollbar_Horizontal.config(orient="horizontal", command=self._Canvas_Scroll.xview, width=self._Scrollbar)
            self._Frame.config(background=self._Background, width=self._Width_Frame, height=self._Height_Frame)
            self._Frame['highlightthickness']=0
            self._Frame.bind("<Configure>", lambda e: self._Canvas_Scroll.configure(scrollregion=self._Canvas_Scroll.bbox("all")))
            if not self._Frame_Scroll:
                self._Frame_Scroll = self._Canvas_Scroll.create_window((0, 0), window=self._Frame, anchor="nw")
                self._Canvas_Scroll.configure(yscrollcommand=self._Scrollbar_Vertical.set)
                self._Canvas_Scroll.configure(xscrollcommand=self._Scrollbar_Horizontal.set)
                self._Canvas_Scroll.pack(side="left", fill="both", expand=True)
            if self._Vertical:
                self._Scrollbar_Vertical.place(relx=1, rely=0, relheight=1, anchor="ne")
            if self._Horizontal:
                self._Scrollbar_Horizontal.place(relx=0, rely=1, relwidth=1, anchor="sw")
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
             
    def Update(self, Widget):
        try:
            try:
                Widget.Resize()
                self._Last = Widget
            except Exception:
                self.Nothing = False
            if self._Width_Frame < (Widget._Left_Current+Widget._Width_Current):
                Extra_Space = self._Scrollbar
                self._Width_Frame = Widget._Left_Current+Widget._Width_Current+Extra_Space
            if self._Height_Frame < (Widget._Top_Current+Widget._Height_Current):
                Extra_Space = self._Scrollbar
                self._Height_Frame = Widget._Top_Current+Widget._Height_Current+Extra_Space
            self._Frame.config(width=self._Width_Frame, height=self._Height_Frame)
            if self._Width_Current >= self._Width_Frame:
                self._Scrollbar_Horizontal.place_forget()
            else:
                self._Scrollbar_Horizontal.place(relx=0, rely=1, relwidth=1, anchor="sw")
            if self._Height_Current >= self._Height_Frame:
                self._Scrollbar_Vertical.place_forget()
            else:
                self._Scrollbar_Vertical.place(relx=1, rely=0, relheight=1, anchor="ne")
            if self._Vertical:
                self._Scrollbar_Vertical.place(relx=1, rely=0, relheight=1, anchor="ne")
            if self._Horizontal:
                self._Scrollbar_Horizontal.place(relx=0, rely=1, relwidth=1, anchor="sw")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update -> {E}")
             
    def Update_All(self):
        try:
            for Widget in self._Widget:
                try:
                    Widget.Resize()
                except Exception:
                    self.Nothing = False
                if self._Width_Frame < (Widget._Left_Current+Widget._Width_Current):
                    Extra_Space = self._Scrollbar
                    self._Width_Frame = Widget._Left_Current+Widget._Width_Current+Extra_Space
                if self._Height_Frame < (Widget._Top_Current+Widget._Height_Current):
                    Extra_Space = self._Scrollbar
                    self._Height_Frame = Widget._Top_Current+Widget._Height_Current+Extra_Space
            self._Frame.config(width=self._Width_Frame, height=self._Height_Frame)
            if self._Width_Current >= self._Width_Frame:
                self._Scrollbar_Horizontal.place_forget()
            else:
                self._Scrollbar_Horizontal.place(relx=0, rely=1, relwidth=1, anchor="sw")
            if self._Height_Current >= self._Height_Frame:
                self._Scrollbar_Vertical.place_forget()
            else:
                self._Scrollbar_Vertical.place(relx=1, rely=0, relheight=1, anchor="ne")
            if self._Vertical:
                self._Scrollbar_Vertical.place(relx=1, rely=0, relheight=1, anchor="ne")
            if self._Horizontal:
                self._Scrollbar_Horizontal.place(relx=0, rely=1, relwidth=1, anchor="sw")
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_All -> {E}")
            
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
            self._Width_Frame = self._Width_Current
            self._Height_Frame = self._Height_Current
            self._Frame.config(width=self._Width_Frame, height=self._Height_Frame)
            if self._Display:
                self.Display()
            if self._Last:
                self.Update(self._Last)
            else:
                self.Update_All()
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