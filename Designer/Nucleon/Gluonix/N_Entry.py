# IMPORT LIBRARIES
import tkinter as TK
import threading, math, time
from .N_GUI import GUI
from .N_Custom import Event_Bind

class Entry:

    def __init__(self, Main, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Entry"
            try:
                self._Config = ['Name', 'Auto_Dark', 'Background', 'Light_Background', 'Dark_Background', 'Foreground', 'Light_Foreground', 'Dark_Foreground', 'Border_Color', 'Light_Border_Color', 'Dark_Border_Color', 'Border_Size', 'Resize', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height', 'Animate_Left', 'Animate_Top', 'Animate_Width', 'Animate_Height', 'Animate_Time', 'Font_Size', 'Font_Weight', 'Font_Family', 'Align', 'Disable', 'Secure', 'Disable_Background', 'Disable_Foreground', 'Select_Background', 'Select_Foreground', 'Hover_Background', 'Light_Hover_Background', 'Dark_Hover_Background', 'Hover_Foreground', 'Light_Hover_Foreground', 'Dark_Hover_Foreground', 'Hover_Border_Color', 'Light_Hover_Border_Color', 'Dark_Hover_Border_Color']
                self._Initialized = False
                self._Widget = []
                self._Name = False
                self._Last_Name = False
                self._Resize = True
                self._Popup = False
                self._Display = True
                self._Size_Update = False
                self._Main = Main
                self._Widget = TK.Entry(self._Main._Frame)
                self._Background = self._Main._Background
                self._Background_Main = True
                self._Border_Color = '#000000'
                self._Border_Size = 0
                self._Foreground = '#000000'
                self._Disable_Foreground = self._Foreground
                self._Disable_Background = '#d0d3d4'
                self._Select_Foreground = self._Background
                self._Select_Background = self._Foreground
                self._Hover_Background = False
                self._Hover_Foreground = False
                self._Hover_Border_Color = False
                self._Last_Background = False
                self._Last_Foreground = False
                self._Last_Border_Color = False
                self._Animating = False
                self._Anim_Stop = threading.Event()
                self._Anim_Thread = None
                self._Animate_Ease = lambda t: (1 - (1 - t)**3)
                self._Animate_Speed = None
                self._Animate_Left = 0
                self._Animate_Top = 0
                self._Animate_Width = 0
                self._Animate_Height = 0
                self._Animate_Time = 1.0
                self._Font_Size = 12
                self._Font_Weight = 'normal'
                self._Font_Family = 'Helvetica'
                self._Align = 'center'
                self._Disable = False
                self._Secure = False
                self._Auto_Dark = True
                self._On_Show = False
                self._On_Hide = False
                self._On_Animate = False
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Entry[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Entry[]"
    
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
            self.Animate_Cancel()
            self._Main._Widget.remove(self)
            self._Widget.destroy()
            if self:
                del self
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete -> {E}")

    def Hide(self):
        try:
            self.Animate_Cancel()
            self._Widget.place_forget()
            self._Display = False
            if self._On_Hide:
                self._On_Hide()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Hide -> {E}")
            
    def _Build_Place_Args(self, Left, Top, Width, Height):
        try:
            Place_Args = {}
            Parent_Width = float(getattr(self._Main, "_Width", 0) or 0)
            Parent_Height = float(getattr(self._Main, "_Height", 0) or 0)
            if self._Resize and self._Main._Type!='Scroll' and Parent_Width > 0 and Parent_Height > 0:
                Place_Args["relx"] = float(Left) / Parent_Width
                Place_Args["rely"] = float(Top) / Parent_Height
                if Width>0:
                    Place_Args["relwidth"] = float(Width) / Parent_Width
                if Height>0:
                    Place_Args["relheight"] = float(Height) / Parent_Height
            else:
                Place_Args["x"] = int(round(Left))
                Place_Args["y"] = int(round(Top))
                if Width>0:
                    Place_Args["width"] = int(round(Width))
                if Height>0:
                    Place_Args["height"] = int(round(Height))
            return Place_Args
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Build_Place_Args -> {E}")
            return {}

    def _Place_Geometry(self, Left, Top, Width, Height):
        try:
            Place_Args = self._Build_Place_Args(Left, Top, Width, Height)
            self._Widget.place(**Place_Args)
            self._Widget.lift()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Place_Geometry -> {E}")
            
    def Show(self):
        try:
            if self._Animating:
                return
            self._Display = True
            self._Place_Geometry(self._Left, self._Top, self._Width, self._Height)
            if self._On_Show:
                self._On_Show()
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
            self.Animate_Cancel()
            Final_Left = float(getattr(self, "_Left", 0))
            Final_Top = float(getattr(self, "_Top", 0))
            Final_Width = float(getattr(self, "_Width", 0))
            Final_Height = float(getattr(self, "_Height", 0))
            Start_Left = float(self._Animate_Left)
            Start_Top = float(self._Animate_Top)
            Animate_Width = float(getattr(self, "_Animate_Width", 0) or 0)
            Animate_Height = float(getattr(self, "_Animate_Height", 0) or 0)
            Size_Anim = not (Animate_Width == 0 and Animate_Height == 0)
            Start_Width = Animate_Width if Size_Anim else Final_Width
            Start_Height = Animate_Height if Size_Anim else Final_Height
            Same_Pos = int(round(Start_Left)) == int(round(Final_Left)) and int(round(Start_Top)) == int(round(Final_Top))
            Same_Size = int(round(Start_Width)) == int(round(Final_Width)) and int(round(Start_Height)) == int(round(Final_Height))
            if Same_Pos and (not Size_Anim or Same_Size):
                def Snap_Same():
                    if not self._Widget.winfo_exists():
                        return
                    self._Place_Geometry(Final_Left, Final_Top, Final_Width, Final_Height)
                    self._Animating = False
                    if Hide:
                        self.Hide()
                    if self._On_Animate:
                        self._On_Animate()
                self._GUI._Frame.after(0, Snap_Same)
                return
            def Show_Start():
                if not self._Widget.winfo_exists():
                    return
                self._Place_Geometry(Start_Left, Start_Top, Start_Width, Start_Height)
            self._GUI._Frame.after(0, Show_Start)
            Dx = Final_Left - Start_Left
            Dy = Final_Top - Start_Top
            Dw = Final_Width - Start_Width if Size_Anim else 0.0
            Dh = Final_Height - Start_Height if Size_Anim else 0.0
            Dist = math.hypot(math.hypot(Dx, Dy), math.hypot(Dw, Dh))
            if Dist == 0.0:
                def Snap_Final():
                    if not self._Widget.winfo_exists():
                        return
                    self._Place_Geometry(Final_Left, Final_Top, Final_Width, Final_Height)
                    self._Animating = False
                    if Hide:
                        self.Hide()
                    if self._On_Animate:
                        self._On_Animate()
                self._GUI._Frame.after(0, Snap_Final)
                return
            if self._Animate_Speed and self._Animate_Speed > 0:
                Duration = max(0.001, Dist / float(self._Animate_Speed))
            else:
                Duration = max(0.001, float(self._Animate_Time))
            Ease = self._Animate_Ease or (lambda t: t)
            Target_FPS = 90.0
            Frame_Interval = 1.0 / Target_FPS
            self._Animating = True
            Stop = self._Anim_Stop
            def Worker():
                T0 = time.perf_counter()
                Next_Tick = T0
                Last = None
                while not Stop.is_set():
                    Now = time.perf_counter()
                    T = (Now - T0) / Duration
                    if T >= 1.0:
                        def Snap_End():
                            if not self._Widget.winfo_exists():
                                return
                            self._Place_Geometry(Final_Left, Final_Top, Final_Width, Final_Height)
                            self._Animating = False
                            if Hide:
                                self.Hide()
                            if self._On_Animate:
                                self._On_Animate()
                        self._GUI._Frame.after(0, Snap_End)
                        return
                    K = Ease(max(0.0, min(1.0, T)))
                    X = Start_Left + Dx * K
                    Y = Start_Top + Dy * K
                    W = Start_Width + Dw * K
                    H = Start_Height + Dh * K
                    Cur = (int(round(X)), int(round(Y)), int(round(W)), int(round(H)))
                    if Cur != Last:
                        Last = Cur
                        def Post(C=Cur):
                            if not self._Widget.winfo_exists():
                                return
                            if self._Animating:
                                self._Place_Geometry(C[0], C[1], C[2], C[3])
                        self._GUI._Frame.after(0, Post)
                    Next_Tick += Frame_Interval
                    Sleep_For = Next_Tick - time.perf_counter()
                    if Sleep_For < -2 * Frame_Interval:
                        Next_Tick = time.perf_counter()
                        Sleep_For = Frame_Interval
                    if Sleep_For > 0:
                        time.sleep(Sleep_For)
            self.Show()
            if Thread:
                T = threading.Thread(target=Worker, daemon=True)
                self._Anim_Thread = T
                T.start()
            else:
                Worker()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Animate -> {E}")
            self.Animate_Cancel()

    def Animate_Cancel(self):
        try:
            self._Animating = False
            if self._Anim_Thread and self._Anim_Thread.is_alive():
                self._Anim_Stop.set()
                self._Anim_Thread.join(timeout=0.2)
            self._Anim_Stop.clear()
            self._Anim_Thread = None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Animate_Cancel -> {E}")
            
    def Get(self):
        try:
            return self._Widget.get()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get -> {E}")
            
    def Set(self, Value):
        try:
            self._Widget.config(state=TK.NORMAL)
            self._Widget.delete(0, TK.END)
            self._Widget.insert(0, Value)
            if self._Disable:
                State = TK.DISABLED
            else:
                State = TK.NORMAL
            self._Widget.config(state=State)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Set -> {E}")
            
    def Widget(self):
        try:
            return self._Widget
        except Exception as E:
            self._GUI.Error(f("{self._Type} -> Widget -> {E}"))
            
    def Bind(self, **Input):
        try:
            if 'On_Show' in Input:
                self._On_Show = Input['On_Show']
            if 'On_Hide' in Input:
                self._On_Hide = Input['On_Hide']
            if 'On_Animate' in Input:
                self._On_Animate = Input['On_Animate']
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
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Config -> {E}")
            
    def Move(self, Left=None, Top=None):
        try:
            if Left is not None:
                self._Left += Left
            if Top is not None:
                self._Top += Top
            if (Left is not None or Top is not None) and self._Initialized and self._Display:
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
            if (Left is not None or Top is not None) and self._Initialized and self._Display:
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
            if (Left is not None or Top is not None) and self._Initialized and self._Display:
                if self._Display and not self._Animating:
                    self._Place_Geometry(self._Left, self._Top, 0, 0)
            return [int(self._Left), int(self._Top)]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Position -> {E}")
            
    def Size(self, Width=False, Height=False):
        try:
            if Width:
                self._Width = Width
            if Height:
                self._Height = Height
            if (Width or Height) and self._Initialized and self._Display:
                if self._Display and not self._Animating:
                    self._Place_Geometry(self._Left, self._Top, self._Width, self._Height)
            return [int(self._Width), int(self._Height)]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Size -> {E}")
            
    def Box(self):
        try:
            return [self._Widget.winfo_x(), self._Widget.winfo_y(), self._Widget.winfo_width(), self._Widget.winfo_height()]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Box -> {E}")
        
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
            Left = round((Left/self._Width)*100, 3)
            Top = round((Top/self._Height)*100, 3)
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
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                Event_Bind(self._Widget, On_Hover_In=lambda E: self.On_Hover_In(E), On_Hover_Out=lambda E: self.On_Hover_Out(E))
                self._Initialized = True
            if self._Disable:
                State = TK.DISABLED
            else:
                State = TK.NORMAL
            if self._Secure:
                Show = '*'
            else:
                Show = ''
            
            self._Font = TK.font.Font(family=self._Font_Family, size=self._Font_Size, weight=self._Font_Weight)
            self._Widget.config(background=self._Background, foreground=self._Foreground, font=self._Font, state=State, show=Show, justify=self._Align, bd=0, highlightthickness=0, relief=TK.FLAT)
            self._Widget.config(disabledbackground=self._Disable_Background, disabledforeground=self._Disable_Foreground, selectbackground=self._Select_Background, selectforeground=self._Select_Foreground)
            self._Widget['highlightbackground']=self._Border_Color
            self._Widget['highlightcolor']=self._Border_Color
            self._Widget['highlightthickness']=self._Border_Size
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