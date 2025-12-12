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
                self._Config = ['Name', 'Auto_Dark', 'Background', 'Light_Background', 'Dark_Background', 'Resize', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height', 'Orient', 'Hover_Background']
                self._Initialized = False
                self._Name = False
                self._Last_Name = False
                self._Widget = []
                self._Resize = True
                self._Popup = False
                self._Display = True
                self._Size_Update = False
                self._Resize_Index = 0
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
                self._Auto_Dark = True
                self._On_Show = False
                self._On_Hide = False
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
            if self._Resizable and self._Resize_Index<self._GUI._Resize_Index:
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
                Config['Background'] = self._Last_Background if self._Background==self._Hover_Background else self._Background
            if len(Config)>0:
                self.Config(**Config)
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
                self._Frame.Config(Background=self._Background, Border_Size=0, Border_Color='#000000')
                self._Frame.Bind(On_Click=self.Drag_Start, On_Drag=self.Drag, On_Release=self.Drag_End)
                self._Frame.Bind(On_Hover_In=lambda E: self.On_Hover_In(E), On_Hover_Out=lambda E: self.On_Hover_Out(E))
                self._Frame.Create()
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                self._Initialized = True
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
                Difference = (E.x_root - self._GUI._Frame.winfo_rootx() - self._Coord['X'])
                Temp_Left = self.Config_Get('Left')['Left']+Difference
                self.Config(Left=Temp_Left)
                self._GUI._Frame.config(cursor='sb_h_double_arrow')
            if self._Orient=='Horizontal':
                self._GUI._Frame.config(cursor='sb_v_double_arrow')
                Difference = (E.y_root - self._GUI._Frame.winfo_rooty() - self._Coord['Y'])
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