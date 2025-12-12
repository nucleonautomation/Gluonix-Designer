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
                self._Config = ['Name', 'Auto_Dark', 'Background', 'Light_Background', 'Dark_Background', 'Foreground', 'Light_Foreground', 'Dark_Foreground', 'Border_Color', 'Light_Border_Color', 'Dark_Border_Color', 'Highlight_Background_Color', 'Highlight_Foreground_Color', 'Border_Size', 'Resize', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height', 'Align', 'Popup_Font_Size', 'Font_Size', 'Font_Weight', 'Font_Family','Height_List', 'Disable', 'Values', 'Hover_Background', 'Light_Hover_Background', 'Dark_Hover_Background', 'Hover_Foreground', 'Light_Hover_Foreground', 'Dark_Hover_Foreground', 'Hover_Border_Color', 'Light_Hover_Border_Color', 'Dark_Hover_Border_Color']
                self._Initialized = False
                self._Name = False
                self._Last_Name = False
                self._Widget = []
                self._Values = []
                self._Current = None
                self._Resize = True
                self._Popup = False
                self._Display = True
                self._Size_Update = False
                self._Main = Main
                self._Frame = Frame(self._Main)
                self._Style_Name = "CustomStyle_" + str(id(self)) + ".TCombobox"
                self._GUI._Style.layout(self._Style_Name, [("Combobox.field", {"sticky": "nswe", "children": [("Combobox.downarrow", {"side": "right", "sticky": "ns"}), ("Combobox.padding", {"sticky": "nswe", "children": [("Combobox.textarea", {"sticky": "nswe"})]})]})])
                self._Widget = TK.ttk.Combobox(self._Frame._Frame)
                self._Widget.configure(style=self._Style_Name)
                self._Widget.bind('<<ComboboxSelected>>', self.On_Change)
                self._Highlight_Background_Color = '#aed6f1'
                self._Highlight_Foreground_Color = '#000000'
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
                self._Popup_Font_Size = 0
                self._Font_Size = 12
                self._Font_Weight = 'normal'
                self._Font_Family = 'Helvetica'
                self._Height_List = 10
                self._Disable = False
                self._On_Change = False
                self._Auto_Dark = True
                self._On_Show = False
                self._On_Hide = False
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
                if hasattr(self, "_"+Key):
                    setattr(Instance, "_"+Key, getattr(self, "_"+Key))
            if Name:
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
            self._Frame.Show()
            self._Widget.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
            self._Display = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Show -> {E}")
            
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
            
    def Animate(self, Hide=False, Thread=True):
        try:
            self._Frame.Animate(Widget=self._Widget, Thread=Thread)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Animate -> {E}")
            self.Animate_Cancel()
            
    def Animate_Cancel(self):
        try:
            self._Frame.Animate_Cancel()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Animate_Cancel -> {E}")
            
    def Get(self):
        try:
            return self._Widget.get()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get -> {E}")
            
    def Set(self, Value):
        try:
            if isinstance(Value, int):
                self._Widget.current(Value)
                self._Current = Value
            else:
                if Value in self._Values:
                    self._Widget.current(self._Values.index(Value))
                    self._Current = self._Values.index(Value)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Set -> {E}")
            
    def Clear(self):
        try:
            if len(self._Values)>0:
                self._Values = []
                self._Current = None
                self._Widget.config(values=self._Values)
                self._Widget.set('')
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Clear -> {E}")
            
    def Refresh(self, Value=False):
        try:
            Values = self._Values.copy()
            self._Values = []
            self._Widget.config(values=self._Values)
            self._Widget.set('')
            self._Values = Values
            self._Widget.config(values=self._Values)
            if self._Current is not None:
                self.Set(self._Current)
            if Value:
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
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Hover_In -> {E}")
            
    def On_Hover_Out(self, E):
        try:
            Config = {}
            if self._Hover_Background and self._Last_Background:
                Config['Background'] = self._Last_Background if self._Background==self._Hover_Background else self._Background
            if self._Hover_Foreground and self._Last_Foreground:
                Config['Foreground'] = self._Last_Foreground if self._Foreground==self._Hover_Foreground else self._Foreground
            if self._Hover_Border_Color and self._Last_Border_Color:
                Config['Border_Color'] = self._Last_Border_Color if self._Border_Color==self._Hover_Border_Color else self._Border_Color
            if len(Config)>0:
                self.Config(**Config)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Hover_Out -> {E}")
            
    def On_Change(self, E):
        try:
            self._Current = self._Values.index(self._Widget.get())
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
            if "Width" in Input or "Height" in Input or "Left" in Input or "Top" in Input:
                self._Size_Update = True
            if self._Initialized and Run:
                self.Create()
            if "Background" in Input:
                self._Background_Main = not bool(Input["Background"])
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Config -> {E}")
            
    def Move(self, Left=None, Top=None):
        try:
            if Left is not None:
                self._Left += Left
            if Top is not None:
                self._Top += Top
            if Left is not None or Top is not None:
                self.Position(Left=self._Left, Top=self._Top)
            return True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Move -> {E}")
            
    def Center(self, Left=None, Top=None):
        try:
            if Left is not None:
                self._Left = Left-self._Width/2
            if Top is not None:
                self._Top = Top-self._Height/2
            if Left is not None or Top is not None:
                self.Position(Left=self._Left, Top=self._Top)
            return [self._Left+self._Width/2, self._Top+self._Height/2]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Center -> {E}")
            
    def Position(self, Left=None, Top=None):
        try:
            if Left is not None:
                self._Left = Left
            if Top is not None:
                self._Top = Top
            if Left is not None or Top is not None:
                self._Frame.Position(Left=self._Left, Top=self._Top)
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
                self._Frame.Size(Width=self._Width, Height=self._Height)
                self.Create()
            return self._Frame.Size()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Size -> {E}")
            
    def Box(self):
        try:
            return self._Frame.Box()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Box -> {E}")
        
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
            if self._Auto_Dark and not self._GUI._Dark_Mode:
                self.Update_Color()
            if not self._Initialized:
                self.Update_Color()
                self._Frame.Config(Width=self._Width, Height=self._Height, Left=self._Left, Top=self._Top)
                self._Frame.Config(Background=self._Background, Border_Size=self._Border_Size, Border_Color=self._Border_Color)
                self._Frame.Create()
                Event_Bind(self._Widget, On_Hover_In=lambda E: self.On_Hover_In(E), On_Hover_Out=lambda E: self.On_Hover_Out(E))
                self._Widget.bind("<Button-1>", lambda E: self._Widget.after(0, lambda: self._Widget.tk.eval(f'catch {{set w [ttk::combobox::PopdownWindow {str(self._Widget)}]; $w.f.l configure -font {{{str(self._Popup_Font)}}} -background {{{self._Background}}} -foreground {{{self._Foreground}}} -selectbackground {{{self._Highlight_Background_Color}}} -selectforeground {{{self._Highlight_Foreground_Color}}} -activestyle none}}')), add="+")
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                self._Initialized = True
            if self._Disable:
                State = "disabled"
            else:
                State = "readonly"
            self._Font = TK.font.Font(family=self._Font_Family, size=self._Font_Size, weight=self._Font_Weight)
            self._Popup_Font = TK.font.Font(family=self._Font_Family, size=self._Popup_Font_Size, weight=self._Font_Weight) if hasattr(self, "_Popup_Font_Size") and isinstance(self._Popup_Font_Size, (int, float)) and self._Popup_Font_Size > 0 else self._Font
            self._Widget.config(foreground=self._Foreground, font=self._Font, values=self._Values, state=State)
            self._Widget.configure(height=self._Height_List)
            self._Widget['justify'] = self._Align
            self._GUI._Style.configure(self._Style_Name, background=self._Background, fieldbackground=self._Background, foreground=self._Foreground, arrowcolor=self._Foreground, bordercolor=self._Background, lightcolor=self._Background, darkcolor=self._Background, focuscolor=self._Background, relief="flat", borderwidth=0, padding=0)
            self._GUI._Style.map(self._Style_Name, background=[("active", self._Background), ("pressed", self._Background), ("focus", self._Background), ("readonly", self._Background), ("disabled", self._Background)], fieldbackground=[("active", self._Background), ("pressed", self._Background), ("focus", self._Background), ("readonly", self._Background), ("disabled", self._Background)], foreground=[("active", self._Foreground), ("pressed", self._Foreground), ("focus", self._Foreground), ("readonly", self._Foreground), ("disabled", self._Foreground)], arrowcolor=[("active", self._Foreground), ("pressed", self._Foreground), ("focus", self._Foreground), ("readonly", self._Foreground), ("disabled", self._Foreground)], bordercolor=[("active", self._Background), ("pressed", self._Background), ("focus", self._Background), ("readonly", self._Background), ("disabled", self._Background)], lightcolor=[("active", self._Background), ("pressed", self._Background), ("focus", self._Background), ("readonly", self._Background), ("disabled", self._Background)], darkcolor=[("active", self._Background), ("pressed", self._Background), ("focus", self._Background), ("readonly", self._Background), ("disabled", self._Background)], selectbackground=[("focus", self._Background), ("readonly", self._Background)], selectforeground=[("focus", self._Foreground), ("readonly", self._Foreground)])
            self._Widget.configure(style=self._Style_Name)
            self._Widget.after(0, lambda: self._Widget.tk.eval(f'catch {{set w [ttk::combobox::PopdownWindow {str(self._Widget)}]; $w.f.l configure -font {{{str(self._Popup_Font)}}} -background {{{self._Background}}} -foreground {{{self._Foreground}}} -selectbackground {{{self._Highlight_Background_Color}}} -selectforeground {{{self._Highlight_Foreground_Color}}} -activestyle none}}'))
            self.Refresh()
            if self._Display:
                self.Show()
            else:
                self.Hide()
            if self._Name!=self._Last_Name:
                if self._Last_Name:
                    if self._Last_Name in self._Main.__dict__:
                        del self._Main.__dict__[self._Last_Name]
                if self._Name:
                    self._Main.__dict__[self._Name] = self
                self._Last_Name = self._Name
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Create -> {E}")
            
    def Update_Color(self):
        try:
            self._GUI.Initiate_Colors(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Color -> {E}")