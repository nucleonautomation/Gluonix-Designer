# IMPORT LIBRARIES
from .N_GUI import GUI
from .N_Frame import Frame
from .N_Custom import Event_Bind

class Separator:

    def __init__(self, Main, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Separator"
            try:
                self._Config = ['Name', 'Background', 'Resize_Width', 'Resize', 'Resize_Height', 'Move', 'Move_Left', 'Move_Top', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height', 'Orient', 'Hover_Background']
                self._Initialized = False
                self._Name = False
                self._Last_Name = False
                self._Widget = []
                self._Resize_Font, self._Resize, self._Resize_Width, self._Resize_Height, self._Move, self._Move_Left, self._Move_Top = False, True, True, True, True, True, True
                self._Popup = False
                self._Display = True
                self._Main = Main
                self._Frame = Frame(self._Main)
                self._Background = self._Main._Background
                self._Background_Main = True
                self._Hover_Background = False
                self._Last_Background = False
                self._Orient = 'Vertical'
                self._Frame_Input = [False, False]
                self._Drag = False
                self._Coord = {'X': 0, 'Y': 0}
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
        return "Nucleon_Glunoix_Separator[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Separator[]"
    
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
            self.Clear()
            self._Main._Widget.remove(self)
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
            self._Display = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Display -> {E}")
    
    def Grab(self, Path=False):
        try:
            return self._GUI.Grab_Widget(Path=Path, Widget=self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Grab -> {E}")
            
    def Add(self, Frame):
        try:
            if not self._Frame_Input[0]:
                self._Frame_Input[0] = Frame
            else:
                if not self._Frame_Input[1]:
                    self._Frame_Input[1] = Frame
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Add -> {E}")
            
    def Widget(self):
        try:
            return self._Frame._Frame
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Widget -> {E}")
            
    def Bind(self, **Input):
        try:
            if 'On_Show' in Input:
                self._On_Show = Input['On_Show']
            if 'On_Hide' in Input:
                self._On_Hide = Input['On_Hide']
            if 'On_Hover_In' in Input:
                self._On_Hover_In = Input['On_Hover_In']
            Input['On_Hover_In'] = lambda E: self.On_Hover_In(E)
            if 'On_Hover_Out' in Input:
                self._On_Hover_Out = Input['On_Hover_Out']
            Input['On_Hover_Out'] = lambda E: self.On_Hover_Out(E)
            self._Frame.Bind(**Input)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind -> {E}")
            
    def On_Hover_In(self, E):
        try:
            Config = {}
            if self._Hover_Background:
                self._Last_Background = self._Background
                Config['Background'] = self._Hover_Background
            if len(Config)>0:
                self.Config(**Config)
            if self._On_Hover_In:
                self._On_Hover_In(E)
            if self._Orient=='Vertical':
                self._GUI._Frame.config(cursor='sb_h_double_arrow')
            if self._Orient=='Horizontal':
                self._GUI._Frame.config(cursor='sb_v_double_arrow')
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Hover_In -> {E}")
            
    def On_Hover_Out(self, E):
        try:
            Config = {}
            if self._Hover_Background and self._Last_Background:
                Config['Background'] = self._Last_Background
            if len(Config)>0:
                self.Config(**Config)
            if self._On_Hover_Out:
                self._On_Hover_Out(E)
            if not self._Drag:
                self._GUI._Frame.config(cursor="")
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
                self._Width_Current, self._Height_Current, self._Left_Current, self._Top_Current, = self._Width, self._Height, self._Left, self._Top
                self._Frame.Config(Width=self._Width_Current, Height=self._Height_Current, Left=self._Left_Current, Top=self._Top_Current)
                self._Frame.Config(Background=self._Background, Border_Size=0, Border_Color='#000000')
                self._Frame.Bind(On_Click=self.Drag_Start, On_Drag=self.Drag, On_Release=self.Drag_End)
                self._Frame.Bind(On_Hover_In=lambda E: self.On_Hover_In(E), On_Hover_Out=lambda E: self.On_Hover_Out(E))
                self._Frame.Create()
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                self._Initialized = True
            self.Relocate()
            if self._Name!=self._Last_Name:
                if self._Last_Name:
                    if self._Last_Name in self._Main.__dict__:
                        del self._Main.__dict__[self._Last_Name]
                if self._Name:
                    self._Main.__dict__[self._Name] = self
                self._Last_Name = self._Name
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Create -> {E}")

    def Drag_Start(self, E):
        try:
            self._Coord['X'] = E.x_root - self._GUI._Frame.winfo_rootx()
            self._Coord['Y'] = E.y_root - self._GUI._Frame.winfo_rooty()
            self._Drag = True
            if self._Orient=='Vertical':
                self._GUI._Frame.config(cursor='sb_h_double_arrow')
            if self._Orient=='Horizontal':
                self._GUI._Frame.config(cursor='sb_v_double_arrow')
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Drag_Start -> {E}")
        
    def Drag(self, E):
        try:
            if self._Orient=='Vertical':
                Difference = (E.x_root - self._GUI._Frame.winfo_rootx() - self._Coord['X'])*(self._GUI._Width/self._GUI._Width_Current)
                Temp_Left = self.Config_Get('Left')['Left']+Difference
                self.Config(Left=Temp_Left)
                self._GUI._Frame.config(cursor='sb_h_double_arrow')
            if self._Orient=='Horizontal':
                self._GUI._Frame.config(cursor='sb_v_double_arrow')
                Difference = (E.y_root - self._GUI._Frame.winfo_rooty() - self._Coord['Y'])*(self._GUI._Height/self._GUI._Height_Current)
                Temp_Top = self.Config_Get('Top')['Top']+Difference
                self.Config(Top=Temp_Top)
            if self._Frame_Input[0]:
                if self._Orient=='Vertical':
                    Temp_Width = self._Frame_Input[0].Config_Get('Width')['Width']+Difference
                    self._Frame_Input[0].Config(Width=Temp_Width)
                if self._Orient=='Horizontal':
                    Temp_Height = self._Frame_Input[0].Config_Get('Height')['Height']+Difference
                    self._Frame_Input[0].Config(Height=Temp_Height)
            if self._Frame_Input[1]:
                if self._Orient=='Vertical':
                    Temp_Left = self._Frame_Input[1].Config_Get('Left')['Left']+Difference
                    Temp_Width = self._Frame_Input[1].Config_Get('Width')['Width']-Difference
                    self._Frame_Input[1].Config(Width=Temp_Width, Left=Temp_Left)
                if self._Orient=='Horizontal':
                    Temp_Top = self._Frame_Input[1].Config_Get('Top')['Top']+Difference
                    Temp_Height = self._Frame_Input[1].Config_Get('Height')['Height']-Difference
                    self._Frame_Input[1].Config(Height=Temp_Height, Top=Temp_Top)
            self._Coord['X'] = E.x_root - self._GUI._Frame.winfo_rootx()
            self._Coord['Y'] = E.y_root - self._GUI._Frame.winfo_rooty()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Drag -> {E}")

    def Drag_End(self, E):
        try:
            self._Drag = False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Drag_End -> {E}")
            
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
                self.Display()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Relocate -> {E}")
            
    def Resize(self):
        try:
            self.Relocate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Resize -> {E}")
            