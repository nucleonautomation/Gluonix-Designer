# IMPORT LIBRARIES
import math
import tkinter as TK
from .N_GUI import GUI
from .N_Frame import Frame
from .N_Custom import Event_Bind

class Select:

    def __init__(self, Main, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Select"
            try:
                self._Config = ['Name', 'Background', 'Foreground', 'Border_Color', 'Border_Size', 'Resize_Width', 'Resize', 'Resize_Height', 'Move', 'Move_Left', 'Move_Top', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height', 'Align', 'Font_Size', 'Font_Weight', 'Font_Family','Height_List', 'Disable', 'Hover_Background', 'Hover_Foreground', 'Hover_Border_Color']
                self._Initialized = False
                self._Name = False
                self._Last_Name = False
                self._Widget = []
                self._Values = []
                self._Resize_Font, self._Resize, self._Resize_Width, self._Resize_Height, self._Move, self._Move_Left, self._Move_Top = True, True, True, True, True, True, True
                self._Popup = False
                self._Display = True
                self._Main = Main
                self._Frame = Frame(self._Main)
                self._Style = TK.ttk.Style()
                self._Style_Name = "CustomStyle_" + str(id(self))
                self._Style.layout(self._Style_Name, [])
                self._Widget = TK.ttk.Combobox(self._Frame._Frame)
                self._Widget.configure(style=self._Style_Name, exportselection=False)
                self._Widget.bind('<<ComboboxSelected>>', self.On_Change)
                self._Border_Color = '#000000'
                self._Border_Size = 0
                self._Background = self._Main._Background
                self._Background_Main = True
                self._Foreground = '#000000'
                self._Hover_Background = False
                self._Hover_Foreground = False
                self._Hover_Border_Color = False
                self._Last_Background = False
                self._Last_Foreground = False
                self._Last_Border_Color = False
                self._Align = 'center'
                self._Font_Size = 12
                self._Font_Weight = 'normal'
                self._Font_Family = 'Helvetica'
                self._Height_List = 700
                self._Disable = False
                self._On_Change = False
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
        return "Nucleon_Glunoix_Select[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Select[]"
    
    def Copy(self, Name=False, Main=False):
        try:
            if not Main:
                Main = self._Main
            Instance = type(self)(Main)
            for Key in self._Config:
                setattr(Instance, "_"+Key, getattr(self, "_"+Key))
            setattr(Instance, "_Name", Name)
            Instance.Create()
            return Instance
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Copy -> {E}")
        
    def Delete(self):
        try:
            self._Main._Widget.remove(self)
            self._Widget.destroy()
            self._Frame.Delete()
            if self:
                del self
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete -> {E}")
            
    def Hide(self):
        try:
            self._Frame.Hide()
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
            self._Frame.Show()
            self._Widget.place(x=0, y=0, width=self._Width_Current-(self._Border_Size*2), height=self._Height_Current-(self._Border_Size*2))
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
            
    def Get(self):
        try:
            return self._Widget.get()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get -> {E}")
            
    def Set(self, Value):
        try:
            if isinstance(Value, int):
                self._Widget.current(Value)
            else:
                self._Widget.current(self._Values.index(Value))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Set -> {E}")
            
    def Clear(self):
        try:
            if len(self._Values)>0:
                self._Values = []
                self._Widget.config(values=self._Values)
                self._Widget.set('')
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Clear -> {E}")
            
    def Refresh(self, Value):
        try:
            Values = self._Values.copy()
            self._Values = []
            self._Widget.config(values=self._Values)
            self._Widget.set('')
            self._Values = Values
            self._Widget.config(values=self._Values)
            self.Set(Value)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Refresh -> {E}")
            
    def Sort(self):
        try:
            Values = sorted(self._Values)
            self._Values = []
            self._Widget.config(values=self._Values)
            self._Values = Values
            self._Widget.config(values=self._Values)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Sort -> {E}")
            
    def Add(self, Value):
        try:
            self._Values.append(Value)
            self._Widget.config(values=self._Values)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add -> {E}")
            
    def Remove(self, Value):
        try:
            if Value in self._Values:
                self._Values.remove(Value)
                self._Widget.config(values=self._Values)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Remove -> {E}")
            
    def Open(self):
        try:
            self._Widget.event_generate('<Button-1>')
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Open -> {E}")
            
    def Widget(self):
        try:
            return self._Widget
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Widget -> {E}")
            
    def Bind(self, **Input):
        try:
            if 'On_Show' in Input:
                self._On_Show = Input['On_Show']
            if 'On_Hide' in Input:
                self._On_Hide = Input['On_Hide']
            if "On_Change" in Input:
                self._On_Change = Input["On_Change"]
            self._Frame.Bind(**Input)
            if 'On_Hover_In' in Input:
                self._On_Hover_In = Input['On_Hover_In']
            Input['On_Hover_In'] = lambda E: self.On_Hover_In(E)
            if 'On_Hover_Out' in Input:
                self._On_Hover_Out = Input['On_Hover_Out']
            Input['On_Hover_Out'] = lambda E: self.On_Hover_Out(E)
            Event_Bind(self._Widget, **Input)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind -> {E}")
            
    def On_Hover_In(self, E):
        try:
            Config = {}
            if self._Hover_Background:
                self._Last_Background = self._Background
                Config['Background'] = self._Hover_Background
            if self._Hover_Foreground:
                self._Last_Foreground = self._Foreground
                Config['Foreground'] = self._Hover_Foreground
            if self._Hover_Border_Color:
                self._Last_Border_Color = self._Border_Color
                Config['Border_Color'] = self._Hover_Border_Color
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
            if self._Hover_Foreground and self._Last_Foreground:
                Config['Foreground'] = self._Last_Foreground
            if self._Hover_Border_Color and self._Last_Border_Color:
                Config['Border_Color'] = self._Last_Border_Color
            if len(Config)>0:
                self.Config(**Config)
            if self._On_Hover_Out:
                self._On_Hover_Out(E)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Hover_Out -> {E}")
            
    def On_Change(self, E):
        try:
            self._Widget.selection_clear()
            if self._On_Change:
                self._On_Change(E)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Change -> {E}")
            
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
            self._Frame.Config(**Input)
            if self._Initialized and Run:
                self.Create()
            if "Background" in Input:
                self._Background_Main = not bool(Input["Background"])
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Config -> {E}")
            
    def Position(self, Left=None, Top=None):
        try:
            if Left is not None:
                self._Left = Left
            if Top is not None:
                self._Top = Top
            if Left is not None or Top is not None:
                self._Frame.Position(Left=Left, Top=Top)
                self.Relocate()
            return self._Frame.Position()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Position -> {E}")
            
    def Size(self, Width=False, Height=False):
        try:
            if Width:
                self._Width = Width
            if Height:
                self._Height = Height
            if Width or Height:
                self._Frame.Size(Width=Width, Height=Height)
                self.Relocate()
            return self._Frame.Size()
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
            if not self._Initialized:
                self._Width_Current, self._Height_Current, self._Left_Current, self._Top_Current, self._Font_Size_Current = self._Width, self._Height, self._Left, self._Top, self._Font_Size
                self._Frame.Config(Width=self._Width_Current, Height=self._Height_Current, Left=self._Left_Current, Top=self._Top_Current)
                self._Frame.Config(Background=self._Background, Border_Size=self._Border_Size, Border_Color=self._Border_Color)
                self._Frame.Create()
                Event_Bind(self._Widget, On_Hover_In=lambda E: self.On_Hover_In(E), On_Hover_Out=lambda E: self.On_Hover_Out(E))
                Big_Font = TK.font.Font(family=self._Font_Family, size=100)
                self._GUI._Frame.option_add("*TCombobox*Listbox*Font", Big_Font)
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                self._Initialized = True
            if self._Disable:
                State = "disabled"
            else:
                State = "readonly"
            self.Font()
            self._Font = TK.font.Font(family=self._Font_Family, size=self._Font_Size_Current, weight=self._Font_Weight)
            self._Widget.config(foreground=self._Foreground, font=self._Font, values=self._Values, state=State)
            self._Widget.configure(height=self._Height_List)
            self._Widget['justify'] = self._Align
            self._Style.configure(self._Style_Name, background=self._Background, relief='flat')
            self.Resize()
            if self._Name!=self._Last_Name:
                if self._Last_Name:
                    if self._Last_Name in self._Main.__dict__:
                        del self._Main.__dict__[self._Last_Name]
                if self._Name:
                    self._Main.__dict__[self._Name] = self
                self._Last_Name = self._Name
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Create -> {E}")
            
    def Font(self):
        try:
            if self._Resize_Font:
                Width_Ratio = self._Frame._Width_Current / self._Frame._Width
                Height_Ratio = self._Frame._Height_Current / self._Frame._Height
                if Width_Ratio < Height_Ratio:
                    self._Font_Size_Current = math.floor(self._Font_Size * Width_Ratio)
                else:
                    self._Font_Size_Current = math.floor(self._Font_Size * Height_Ratio)
            else:
                self._Font_Size_Current = self._Font_Size
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Font -> {E}")
            
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
            if self._Display:
                self._Font = TK.font.Font(family=self._Font_Family, size=self._Font_Size_Current, weight=self._Font_Weight)
                self._Widget.config(font=self._Font)
                self.Display()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Relocate -> {E}")
            
    def Resize(self):
        try:
            self.Font()
            self.Relocate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Resize -> {E}")
            