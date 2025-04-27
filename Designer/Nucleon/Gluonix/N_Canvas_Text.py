# IMPORT LIBRARIES
import math
from .N_Custom import Event_Bind_Canvas
        
class Canvas_Text:
    def __init__(self, Main):
        self._Canvas = Main
        self._Config = ['Name', 'Left', 'Top', 'Width', 'Height', 'Color', 'Size', 'Value', 'Weight', 'Font', 'Resize', 'Anchor', 'Resize_Font']
        self._Display = True
        self._Resize = True
        self._Name = False
        self._Last_Name = False
        self._Resize_Font = True
        self._Type = 'Canvas_Text'
        self._Left, self._Top, self._Width = 0, 0, 0
        self._Value = ''
        self._Color = '#000000'
        self._Size = 20
        self._Height = 0
        self._Weight = 'normal'
        self._Font = 'Helvetica'
        self._Anchor = 'nw'
        self._Justify = 'center'
        self._Widget = self._Canvas._Frame.create_text(0, 0, text=self._Value, fill=self._Color, font=(self._Font, self._Size, self._Weight), anchor=self._Anchor, width=self._Width, justify=self._Justify)
        self._Canvas._Widget.append(self)
        self._Resizable = self._Canvas._Resizable
        self._On_Show = False
        self._On_Hide = False

    def Copy(self, Name=False, Main=False):
        try:
            if not Main:
                Main = self._Canvas
            Instance = type(self)(Main)
            for Key in self._Config:
                setattr(Instance, "_"+Key, getattr(self, "_"+Key))
            if Name:
                setattr(Instance, "_Name", Name)
            Instance.Create()
            return Instance
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
            if self._Resizable:
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
    
    def Set(self, Value):
        try:
            self._Value = Value
            self._Canvas._Frame.itemconfig(self._Widget, text=self._Value)
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Set -> {E}")
        
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
        
    def Position(self, Left=None, Top=None):
        try:
            if Left is not None:
                self._Left = Left
            if Top is not None:
                self._Top = Top
            if Left is not None or Top is not None:
                self.Relocate()
            Box = self._Canvas._Frame.bbox(self._Widget)
            X1, Y1, X2, Y2 = Box
            return [X1, Y1]
        except Exception as E:
            self.Error(f"{self._Type} -> Position -> {E}")
            
    def Size(self, Width=False, Height=False):
        try:
            if Width:
                self._Width = Width
            if Height:
                self._Height = Height
            if Width or Height:
                self.Relocate()
            Box = self._Canvas._Frame.bbox(self._Widget)
            X1, Y1, X2, Y2 = Box
            Width = X2 - X1
            Height = Y2 - Y1
            return [Width, Height]
        except Exception as E:
            self.Error(f"{self._Type} -> Size -> {E}")
        
    def Create(self):
        try:
            self._Canvas._Frame.itemconfig(self._Widget, text=self._Value, fill=self._Color, font=(self._Font, self._Size_Current, self._Weight), anchor=self._Anchor, width=self._Width_Current, justify=self._Justify)
            self._Canvas._Frame.coords(self._Widget, self._X_Current, self._Y_Current)
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
            if self._Resize:
                self.Adjustment()
                self._X_Current = self._Left * self._Width_Ratio
                self._Y_Current = self._Top * self._Height_Ratio
                self._Width_Current = self._Width * self._Width_Ratio
                if self._Resize_Font:
                    if self._Width_Ratio < self._Height_Ratio:
                        self._Size_Current = math.floor(self._Size * self._Width_Ratio)
                    else:
                        self._Size_Current = math.floor(self._Size * self._Height_Ratio)
                else:
                    self._Size_Current = self._Size
            self.Create()
            if self._Display:
                self.Display()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Relocate -> {E}")
            
    def Resize(self):
        try:
            self.Relocate()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Resize -> {E}")