# IMPORT LIBRARIES
import os
import vlc
from .N_GUI import GUI
from .N_Canvas import Canvas
from .N_Custom import Event_Bind

class Video:

    def __init__(self, Main, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Video"
            try:
                self._Config = ['Name', 'Background', 'Light_Background', 'Dark_Background', 'Border_Color', 'Light_Border_Color', 'Dark_Border_Color', 'Border_Size', 'Resize_Width', 'Resize', 'Resize_Height', 'Move', 'Move_Left', 'Move_Top', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height', 'Path', 'Hover_Background', 'Light_Hover_Background', 'Dark_Hover_Background', 'Hover_Border_Color', 'Light_Hover_Border_Color', 'Dark_Hover_Border_Color']
                self._Initialized = False
                self._Name = False
                self._Last_Name = False
                self._Resize_Font, self._Resize, self._Resize_Width, self._Resize_Height, self._Move, self._Move_Left, self._Move_Top = False, True, True, True, True, True, True
                self._Popup = False
                self._Display = True
                self._Main = Main
                self._Frame = Canvas(self._Main)
                self._Border_Color = '#000000'
                self._Border_Size = 0
                self._Background = self._Main._Background
                self._Hover_Background = False
                self._Hover_Border_Color = False
                self._Last_Background = False
                self._Last_Border_Color = False
                self._VLC_Args = ['--quiet', '--no-xlib']
                self._VLC = vlc.Instance(self._VLC_Args)
                self._Player = self._VLC.media_player_new()
                self._Player.set_hwnd(self._Frame._Frame.winfo_id())
                self._Media = False
                self._Pause = True
                self._Path = False
                self._Path_Memory = False
                self._Subtitle = False
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
        return "Nucleon_Glunoix_Image_Zoom[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Image_Zoom[]"
    
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
            return Instance
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Copy -> {E}")
        
    def Delete(self):
        try:
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
            
    def Set(self, Path):
        try:
            self._Path = Path
            if self._Path!=self._Path_Memory:
                self._Path_Memory = self._Path
                self.Open()
                self.Relocate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Set -> {E}")
            
    def Widget(self):
        try:
            return self._Player
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
            if self._Hover_Border_Color and self._Last_Border_Color:
                Config['Border_Color'] = self._Last_Border_Color
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
            self._Frame.Config(**Input)
            if self._Initialized and Run:
                self.Create()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Config -> {E}")
        
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
                self._Width_Current, self._Height_Current, self._Left_Current, self._Top_Current, = self._Width, self._Height, self._Left, self._Top
                self._Frame.Config(Width=self._Width_Current, Height=self._Height_Current, Left=self._Left_Current, Top=self._Top_Current)
                self._Frame.Config(Background=self._Background, Border_Size=self._Border_Size, Border_Color=self._Border_Color)
                self._Frame.Create()
                self._Frame.Bind(On_Hover_In=lambda E: self.On_Hover_In(E), On_Hover_Out=lambda E: self.On_Hover_Out(E))
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                self._Initialized = True
            if self._Path!=self._Path_Memory:
                self._Path_Memory = self._Path
                self.Open()
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
            
    def Open(self):
        try:
            if self._Path:
                self.Stop()
                if self._Subtitle:
                    self.Subtitle_Off()
                    self._Subtitle = False
                self._Media = self._VLC.media_new(self._Path)
                self._Player.set_media(self._Media)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Open -> {E}")
            
    def Playing(self):
        try:
            return not self._Pause
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> State -> {E}")
            
    def Stop(self):
        try:
            self._Player.stop()
            self._Pause = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Stop -> {E}")
            
    def Pause(self):
        try:
            self._Player.pause()
            self._Pause = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Pause -> {E}")
            
    def Play(self):
        try:
            self._Player.play()
            self._Pause = False
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Play -> {E}")
            
    def Length(self):
        try:
            return self._Player.get_length()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Length -> {E}")
            
    def Time_Get(self):
        try:
            return self._Player.get_time()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Time_Get -> {E}")
            
    def Time_Set(self, Value):
        try:
            return self._Player.set_time(Value)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Time_Set -> {E}")
            
    def Audio_Get(self):
        try:
            return self._Player.audio_get_track_description()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Audio_Get -> {E}")
            
    def Audio_Set(self, ID):
        try:
            return self._Player.audio_set_track(ID)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Audio_Set -> {E}")
            
    def Volume_Get(self):
        try:
            return self._Player.audio_get_volume()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Volume_Get -> {E}")
            
    def Volume_Set(self, Value):
        try:
            return self._Player.audio_set_volume(Value)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Volume_Set -> {E}")
            
    def Subtitle(self, Path):
        try:
            if self._Subtitle:
                self.Subtitle_Off()
                self._Subtitle = False
            self._Player.add_slave(vlc.MediaSlaveType.subtitle, Path, True)
            self._Subtitle = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Subtitle -> {E}")
            
    def Subtitle_On(self):
        try:
            if self._Subtitle:
                self._Player.video_set_spu(0)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Subtitle_On -> {E}")
            
    def Subtitle_Off(self):
        try:
            if self._Subtitle:
                self._Player.video_set_spu(-1)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Subtitle_Off -> {E}")
            
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