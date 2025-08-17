# IMPORT LIBRARIES
import threading, math, time
from .N_Custom import Event_Bind_Canvas

class Canvas_Polygon:
    def __init__(self, Main):
        self._Canvas = Main
        self._Config = ['Name', 'Outline', 'Fill', 'Thickness', 'Resize', 'Translucent', 'Alpha']
        self._Display = True
        self._Resize_Index = 0
        self._Resize = True
        self._Name = False
        self._Last_Name = False
        self._Type = 'Canvas_Polygon'
        self._Points = []
        self._Points_Current = []
        self._Outline = '#000000'
        self._Fill = '#000000'
        self._Thickness = 1
        self._Translucent = False
        self._Alpha = 25
        Points = [0, 0, 0, 0]
        self._Widget = self._Canvas._Frame.create_polygon(Points, outline=self._Outline, width=self._Thickness, fill=self._Fill)
        self._Canvas._Widget.append(self)
        self._Resizable = self._Canvas._Resizable
        self._On_Show = False
        self._On_Hide = False

    def __str__(self):
        return "Nucleon_Glunoix_Canvas_Polygon[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Canvas_Polygon[]"

    def Copy(self, Name=False, Main=False):
        try:
            if not Main:
                Main = self._Canvas
            if Main._Type in ['Canvas', 'Scroll', 'Group']:
                Temp_Main = Main
                Temp_Type = Temp_Main._Type
                while Temp_Type=='Group':
                    Temp_Main = Main._Main
                    Temp_Type = Temp_Main._Type
                if Temp_Type=='Canvas' or Temp_Type=='Scroll':
                    Instance = type(self)(Main)
                    for Key in self._Config:
                        if hasattr(self, "_"+Key):
                            setattr(Instance, "_"+Key, getattr(self, "_"+Key))
                    if Name:
                        setattr(Instance, "_Name", Name)
                    Instance.Relocate()
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
            self._Display = True
            if self._Resizable and self._Resize_Index<self._Canvas._GUI._Resize_Index:
                self.Resize()
            else:
                self.Display()
            if self._On_Show:
                self._On_Show()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Show -> {E}")

    def Display(self):
        try:
            self._Canvas._Frame.itemconfigure(self._Widget, state='normal')
            self._Canvas._Frame.tag_raise(self._Widget)
            self._Display = True
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Display -> {E}")
    
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
                self.Relocate()
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
                self.Relocate()
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

    def Add(self, X, Y):
        try:
            self._Points.append([X, Y])
            self._Points_Current.append([X, Y])
            self.Relocate()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Add -> {E}")

    def Remove(self, Index):
        try:
            if 0 <= Index < len(self._Points):
                self._Points.pop(Index)
                self._Points_Current.pop(Index)
                self.Relocate()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Remove -> {E}")

    def Replace(self, Points):
        try:
            self._Points = Points
            self._Points_Current = Points
            self.Relocate()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Replace -> {E}")
            
    def Stripple(self):
        try:
            if 0 <= self._Alpha <= 12:
                return 12
            elif 13 <= self._Alpha <= 25:
                return 25
            elif 26 <= self._Alpha <= 50:
                return 50
            elif 51 <= self._Alpha <= 75:
                return 75
            else:
                return 100
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Stripple -> {E}")

    def Create(self):
        try:
            Stripple = f'gray{self.Stripple()}' if self._Translucent else ''
            self._Canvas._Frame.itemconfig(self._Widget, outline=self._Outline, width=self._Thickness, fill=self._Fill, stipple=Stripple)
            if len(self._Points)>1:
                Points = [Item for Pair in self._Points_Current for Item in Pair]
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

    def Adjustment(self):
        try:
            self._Width_Ratio = self._Canvas._Width_Current / self._Canvas._Width
            self._Height_Ratio = self._Canvas._Height_Current / self._Canvas._Height
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Adjustment -> {E}")
            
    def Relocate(self, Direct=False):
        try:
            if Direct or (self._Resize and self._Resizable):
                self.Adjustment()
                self._Points_Current = [[X * self._Width_Ratio, Y * self._Height_Ratio] for X, Y in self._Points]
            else:
                self._Points_Current = self._Points.copy()
            self.Create()
            if self._Display:
                self.Display()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Relocate -> {E}")
            
    def Resize(self):
        try:
            self._Resize_Index = self._Canvas._GUI._Resize_Index
            self.Relocate()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Resize -> {E}")