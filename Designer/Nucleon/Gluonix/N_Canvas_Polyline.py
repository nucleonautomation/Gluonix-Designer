# IMPORT LIBRARIES
import threading, math, time
from .N_Custom import Event_Bind_Canvas

class Canvas_Polyline:
    def __init__(self, Main):
        self._Canvas = Main
        self._Config = ['Name', 'Outline', 'Thickness', 'Resize']
        self._Display = True
        self._Resize = True
        self._Name = False
        self._Last_Name = False
        self._Type = 'Canvas_Polyline'
        self._Points = []
        self._Points_Current = []
        self._Outline = '#000000'
        self._Thickness = 1
        Points = [0, 0, 0, 0]
        self._Widget = self._Canvas._Frame.create_line(Points, fill=self._Outline, width=self._Thickness)
        self._Canvas._Widget.append(self)
        self._Canvas._Item.append(self)
        self._On_Show = False
        self._On_Hide = False

    def __str__(self):
        return "Nucleon_Glunoix_Canvas_Polyline[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Canvas_Polyline[]"

    def Copy(self, Name=False, Main=False):
        try:
            if not Main:
                Main = self._Canvas
            if Main._Type in ['Canvas', 'Scroll', 'Group']:
                Temp_Main = Main
                Temp_Type = Temp_Main._Type
                while Temp_Type=='Group':
                    Temp_Main = Temp_Main._Main
                    Temp_Type = Temp_Main._Type
                if Temp_Type=='Canvas' or Temp_Type=='Scroll':
                    Instance = type(self)(Main)
                    for Key in self._Config:
                        if hasattr(self, "_"+Key):
                            setattr(Instance, "_"+Key, getattr(self, "_"+Key))
                    if Name:
                        setattr(Instance, "_Name", Name)
                    Instance.Create()
                    return Instance
                else:
                    raise Exception('Widget can only copy to Canvas/Scroll')
            else:
                raise Exception('Widget can only copy to Canvas/Scroll')
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Copy -> {E}")

    def Hide(self):
        try:
            self._Canvas._Frame.itemconfigure(self._Widget, state='hidden')
            self._Display = False
            if self._On_Hide:
                self._On_Hide()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type}-> Hide -> {E}")
            
    def Show(self):
        try:
            if not self._Display and self._Resize and self._Canvas._Type!='Scroll':
                self.Create()
            self._Canvas._Frame.itemconfigure(self._Widget, state='normal')
            self._Canvas._Frame.tag_raise(self._Widget)
            self._Display = True
            if self._On_Show:
                self._On_Show()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Show -> {E}")
    
    def Delete(self):
        try:
            self._Canvas._Widget.remove(self)
            self._Canvas._Frame.delete(self._Widget)
            if self:
                del self
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Delete -> {E}")
        
    def Bind(self, **Input):
        try:
            if 'On_Show' in Input:
                self._On_Show = Input['On_Show']
            if 'On_Hide' in Input:
                self._On_Hide = Input['On_Hide']
            Event_Bind_Canvas(self._Canvas._Frame, self._Widget, **Input)
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Bind -> {E}")
            
    def Config_Get(self, *Input):
        try:
            Return = {}
            for Each in self._Config:
                if Each in Input:
                    Return[Each] = getattr(self, "_"+Each)
            return Return
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Config_Get -> {E}")
                
    def Config(self, **Input):
        try:
            Run = False
            for Each in self._Config:
                if Each in Input:
                    Value = Input[Each]
                    setattr(self, "_"+Each, Value)
                    setattr(self, "_"+Each+"_Current", Value)
                    Run = True
            if Run:
                self.Create()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Config -> {E}")
            
    def Move(self, Left=None, Top=None):
        try:
            if Left is None and Top is None:
                return False
            Left = 0 if Left is None else Left
            Top = 0 if Top is None else Top
            self._Points = [[X + Left, Y + Top] for X, Y in self._Points]
            if Left != 0 or Top != 0:
                self.Create()
            return True
        except Exception as Error:
            self._Canvas._GUI.Error(f"{self._Type} -> Move -> {Error}")
            
    def Center(self, Left=None, Top=None):
        try:
            Box = self._Canvas._Frame.bbox(self._Widget)
            X1, Y1, X2, Y2 = Box
            X = (X1+X2)/2
            Y = (Y1+Y2)/2
            return [X, Y]
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Center -> {E}")
        
    def Position(self, Left=None, Top=None):
        try:
            Box = self._Canvas._Frame.bbox(self._Widget)
            X1, Y1, X2, Y2 = Box
            return [X1, Y1]
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Position -> {E}")
            
    def Size(self, Width=False, Height=False):
        try:
            Box = self._Canvas._Frame.bbox(self._Widget)
            X1, Y1, X2, Y2 = Box
            Width = X2 - X1
            Height = Y2 - Y1
            return [Width, Height]
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Size -> {E}")
            
    def Box(self):
        try:
            Box = self._Canvas._Frame.bbox(self._Widget)
            X1, Y1, X2, Y2 = Box
            Width = X2 - X1
            Height = Y2 - Y1
            return [X1, Y1, Width, Height]
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Box -> {E}")

    def Add(self, X, Y):
        try:
            self._Points.append([X, Y])
            self._Points_Current.append([X, Y])
            self.Create()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Add -> {E}")

    def Remove(self, Index):
        try:
            if 0 <= Index < len(self._Points):
                self._Points.pop(Index)
                self._Points_Current.pop(Index)
                self.Create()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Remove -> {E}")

    def Create(self):
        try:
            if self._Resize and self._Canvas._Type!='Scroll':
                Left, Right, Width, Height = self._Canvas.Box()
                Width_Ratio = Width/self._Canvas._Width
                Height_Ratio = Height/self._Canvas._Height
            else:
                Width_Ratio = 1
                Height_Ratio = 1
            self._Canvas._Frame.itemconfig(self._Widget, fill=self._Outline, width=self._Thickness)
            if len(self._Points)>1:
                Points = [[X * Width_Ratio, Y * Height_Ratio] for X, Y in self._Points]
                Points = [Item for Pair in Points for Item in Pair]
            else:
                Points = [0, 0, 0, 0]
            self._Canvas._Frame.coords(self._Widget, Points)
            if self._Name!=self._Last_Name:
                if self._Last_Name:
                    if self._Last_Name in self._Canvas.__dict__:
                        del self._Canvas.__dict__[self._Last_Name]
                if self._Name:
                    self._Canvas.__dict__[self._Name] = self
                self._Last_Name = self._Name
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Create -> {E}")
            
    def Resize(self, Event):
        try:
            self._Canvas._Frame.itemconfigure(self._Widget, state='normal')
            self._Canvas._Frame.tag_raise(self._Widget)
            if self._Display:
                self.Create()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Resize -> {E}")