# IMPORT LIBRARIES
import tkinter as TK
import threading, math, time
from .N_GUI import GUI
from .N_Custom import Event_Bind
from .N_Custom import Event_Bind_Canvas
from .N_Canvas_Line import Canvas_Line
from .N_Canvas_Polyline import Canvas_Polyline
from .N_Canvas_Pie import Canvas_Pie
from .N_Canvas_Arc import Canvas_Arc
from .N_Canvas_Circle import Canvas_Circle
from .N_Canvas_Oval import Canvas_Oval
from .N_Canvas_Rectangle import Canvas_Rectangle
from .N_Canvas_RectangleR import Canvas_RectangleR
from .N_Canvas_Polygon import Canvas_Polygon
from .N_Canvas_Image import Canvas_Image
from .N_Canvas_Text import Canvas_Text
from .N_Canvas_Text_Old import Canvas_Text_Old
from .N_Player import Player
from .N_Video import Video
from .N_Editor import Editor

class Canvas:

    def __init__(self, Main, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Canvas"
            try:
                try:
                    TK.Canvas.tagraise = TK.Canvas.tkraise
                    del TK.Canvas.tkraise, TK.Canvas.lift
                except Exception:
                    self.Nothing = False
                self._Config = ['Name', 'Auto_Dark', 'Background', 'Light_Background', 'Dark_Background', 'Border_Color', 'Light_Border_Color', 'Dark_Border_Color', 'Border_Size', 'Resize', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height', 'Animate_Left', 'Animate_Top', 'Animate_Width', 'Animate_Height', 'Animate_Time', 'Radius', 'Shadow_Size', 'Shadow_Color', 'Light_Shadow_Color', 'Dark_Shadow_Color', 'Shadow_Full', 'Hover_Background', 'Light_Hover_Background', 'Dark_Hover_Background', 'Hover_Border_Color', 'Light_Hover_Border_Color', 'Dark_Hover_Border_Color', 'Hover_Shadow_Color', 'Light_Hover_Shadow_Color', 'Dark_Hover_Shadow_Color']
                self._Initialized = False
                self._Name = False
                self._Last_Name = False
                self._Widget = []
                self._Item = []
                self._Resize = True
                self._Popup = False
                self._Display = True
                self._Main = Main
                self._Frame = TK.Canvas(self._Main._Frame)
                self._Border_Color = '#000000'
                self._Border_Size = 0
                self._Border = []
                self._Shadow_Size = 0
                self._Shadow_Color = '#d5d8dc'
                self._Shadow_Full = True
                self._Radius = 0
                self._Hover_Background = False
                self._Hover_Border_Color = False
                self._Hover_Shadow_Color = False
                self._Last_Background = False
                self._Last_Border_Color = False
                self._Last_Shadow_Color = False
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
                self._Rounded = []
                self._Background = self._Main._Background
                self._Background_Main = True
                self._On_Resize = False
                self._Auto_Dark = True
                self._On_Show = False
                self._On_Hide = False
                self._On_Animate = False
                self._Configure_After_Id = None
                self._Last_Configure_Event = None
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Canvas[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Canvas[]"
    
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
            for Each in self._Widget:
                Each.Copy(Main=Instance)
            return Instance
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Copy -> {E}")
        
    def Delete(self):
        try:
            self.Animate_Cancel()
            self.Clear()
            self._Main._Widget.remove(self)
            self._Frame.delete(self._Border)
            self._Frame.destroy()
            if self:
                del self
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete -> {E}")

    def Clear(self):
        try:
            for Each in self._Widget:
                Each.Delete()
            for Each in self._Frame.find_all():
                self._Frame.delete(Each)
            self.Rounded()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Clear -> {E}")

    def Refresh(self):
        try:
            self._Frame.update_idletasks()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Refresh -> {E}")
            
    def Hide(self):
        try:
            self.Animate_Cancel()
            self._Frame.place_forget()
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
            self._Frame.place(**Place_Args)
            self._Frame.lift()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> _Place_Geometry -> {E}")
            
    def On_Configure(self, Event):
        try:
            self._Last_Configure_Event = Event
            if self._Configure_After_Id is not None:
                self._Frame.after_cancel(self._Configure_After_Id)
            self._Configure_After_Id = self._Frame.after(10, self.On_Configure_Debounced)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Configure -> {E}")
            
    def On_Configure_Debounced(self):
        try:
            self._Configure_After_Id = None
            Event = self._Last_Configure_Event
            if not Event:
                return
            self.Rounded(Event.width, Event.height)
            T = threading.Thread(target=self.On_Configure_Thread, args=(Event,), daemon=True)
            T.start()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Configure_Debounced -> {E}")
    
    def On_Configure_Thread(self, Event):
        try:
            for Each in self._Item:
                try:
                    if Each._Display:
                        Each.Resize(Event)
                except Exception as E:
                    self._GUI.Error(f"{self._Type} -> On_Configure -> {E}")
            if self._On_Resize:
                self._On_Resize(Event)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Configure_Thread -> {E}")
            
    def Show(self):
        try:
            if self._Animating:
                return
            self._Display = True
            self._Place_Geometry(self._Left, self._Top, self._Width, self._Height)
            for Each in self._Widget:
                try:
                    if Each._Display:
                        Each.Show()
                except Exception:
                    self.Nothing = False
            if self._On_Show:
                self._On_Show()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Show -> {E}")
            
    def Animate(self, Widget=None, Hide=False, Thread=True):
        try:
            self.Animate_Cancel()
            Final_Left = float(self._Left)
            Final_Top = float(self._Top)
            Final_Width = float(self._Width)
            Final_Height = float(self._Height)
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
                Width_I = int(round(Final_Width))
                Height_I = int(round(Final_Height))
                self.Rounded(Width_I, Height_I)
                self._Place_Geometry(Final_Left, Final_Top, Final_Width, Final_Height)
                self._Display = True
                for Each in self._Widget:
                    try:
                        if Each._Display:
                            Each.Show()
                    except Exception:
                        self.Nothing = False
                if Widget is not None:
                    self._Frame.itemconfigure(Widget, state='normal')
                    self._Frame.tag_raise(Widget)
                    self._Frame.coords(Widget, Width_I/2, Height_I/2)
                if self._On_Animate:
                    self._On_Animate()
                if Hide:
                    self.Hide()
                return
            def Show_Start():
                if not self._Frame.winfo_exists():
                    return
                Width_I = int(round(Start_Width))
                Height_I = int(round(Start_Height))
                self.Rounded(Width_I, Height_I)
                self._Place_Geometry(Start_Left, Start_Top, Start_Width, Start_Height)
                self._Display = True
                for Each in self._Widget:
                    try:
                        if Each._Display:
                            Each.Show()
                    except Exception:
                        self.Nothing = False
                if Widget is not None:
                    self._Frame.itemconfigure(Widget, state='normal')
                    self._Frame.tag_raise(Widget)
                    self._Frame.coords(Widget, Width_I/2, Height_I/2)
            self._Frame.after(0, Show_Start)
            Dx = Final_Left - Start_Left
            Dy = Final_Top - Start_Top
            Dw = Final_Width - Start_Width if Size_Anim else 0.0
            Dh = Final_Height - Start_Height if Size_Anim else 0.0
            Dist = math.hypot(math.hypot(Dx, Dy), math.hypot(Dw, Dh))
            if Dist == 0.0:
                def Snap_Same():
                    if not self._Frame.winfo_exists():
                        return
                    Width_I = int(round(Final_Width))
                    Height_I = int(round(Final_Height))
                    self.Rounded(Width_I, Height_I)
                    self._Place_Geometry(Final_Left, Final_Top, Final_Width, Final_Height)
                    self._Display = True
                    for Each in self._Widget:
                        try:
                            if Each._Display:
                                Each.Show()
                        except Exception:
                            self.Nothing = False
                    if Widget is not None:
                        self._Frame.itemconfigure(Widget, state='normal')
                        self._Frame.tag_raise(Widget)
                        self._Frame.coords(Widget, Width_I/2, Height_I/2)
                    if self._On_Animate:
                        self._On_Animate()
                    if Hide:
                        self.Hide()
                self._Frame.after(0, Snap_Same)
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
                        def Snap_Final():
                            if not self._Frame.winfo_exists():
                                return
                            Width_I = int(round(Final_Width))
                            Height_I = int(round(Final_Height))
                            self.Rounded(Width_I, Height_I)
                            self._Place_Geometry(Final_Left, Final_Top, Final_Width, Final_Height)
                            for Each in self._Widget:
                                try:
                                    if Each._Display:
                                        Each.Show()
                                except Exception:
                                    self.Nothing = False
                            self._Animating = False
                            if Widget is not None:
                                self._Frame.itemconfigure(Widget, state='normal')
                                self._Frame.tag_raise(Widget)
                                self._Frame.coords(Widget, Width_I/2, Height_I/2)
                            if Hide:
                                self.Hide()
                            if self._On_Animate:
                                self._On_Animate()
                        self._Frame.after(0, Snap_Final)
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
                            if not self._Frame.winfo_exists():
                                return
                            if self._Animating:
                                Width_I = C[2]
                                Height_I = C[3]
                                self.Rounded(Width_I, Height_I)
                                self._Place_Geometry(C[0], C[1], C[2], C[3])
                                for Each in self._Widget:
                                    try:
                                        if Each._Display:
                                            Each.Show()
                                    except Exception:
                                        self.Nothing = False
                                if Widget is not None:
                                    self._Frame.itemconfigure(Widget, state='normal')
                                    self._Frame.tag_raise(Widget)
                                    self._Frame.coords(Widget, Width_I/2, Height_I/2)
                        self._Frame.after(0, Post)
                    Next_Tick += Frame_Interval
                    Sleep_For = Next_Tick - time.perf_counter()
                    if Sleep_For < -2 * Frame_Interval:
                        Next_Tick = time.perf_counter()
                        Sleep_For = Frame_Interval
                    if Sleep_For > 0:
                        time.sleep(Sleep_For)
            self._Display = True
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
            
    def Focus(self):
        try:
            self._Frame.focus_set()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Focus -> {E}")
    
    def Grab(self, Path=False):
        try:
            return self._GUI.Grab_Widget(Path=Path, Widget=self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Grab -> {E}")
            
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
            if 'On_Animate' in Input:
                self._On_Animate = Input['On_Animate']
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
            
    def On_Hover_In(self, E):
        try:
            Config = {}
            if self._Hover_Background:
                self._Last_Background = self._Background
                Config['Background'] = self._Hover_Background
            if self._Hover_Border_Color:
                self._Last_Border_Color = self._Border_Color
                Config['Border_Color'] = self._Hover_Border_Color
            if self._Hover_Shadow_Color:
                self._Last_Shadow_Color = self._Shadow_Color
                Config['Shadow_Color'] = self._Hover_Shadow_Color
            if len(Config)>0:
                self.Config(**Config)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> On_Hover_In -> {E}")
            
    def On_Hover_Out(self, E):
        try:
            Config = {}
            if self._Hover_Background and self._Last_Background:
                Config['Background'] = self._Last_Background if self._Background==self._Hover_Background else self._Background
            if self._Hover_Border_Color and self._Last_Border_Color:
                Config['Border_Color'] = self._Last_Border_Color if self._Border_Color==self._Hover_Border_Color else self._Border_Color
            if self._Hover_Shadow_Color and self._Last_Shadow_Color:
                Config['Shadow_Color'] = self._Last_Shadow_Color if self._Shadow_Color==self._Hover_Shadow_Color else self._Shadow_Color
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
            if Width or Height:
                if self._Display and not self._Animating:
                    self._Place_Geometry(self._Left, self._Top, self._Width, self._Height)
            return [int(self._Width), int(self._Height)]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Size -> {E}")
            
    def Box(self):
        try:
            return [self._Frame.winfo_x(), self._Frame.winfo_y(), self._Frame.winfo_width(), self._Frame.winfo_height()]
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
            Left =  round((Left/self._Width)*100, 3)
            Top =  round((Top/self._Height)*100, 3)
            return [Width, Height, Left, Top]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Locate_Reverse -> {E}")
            
    def Create(self):
        try:
            First_Init = not self._Initialized
            if not self._Background:
                self._Background = self._Main._Background
                if not hasattr(self, "_Light_Background"):
                    setattr(self, "_Light_Background", self._Background)
                if not hasattr(self, "_Dark_Background"):
                    setattr(self, "_Dark_Background", self._GUI.Invert(self._Background))
            Temp_Background = self._Background
            if self._Auto_Dark and not self._GUI._Dark_Mode:
                self.Update_Color()
            if First_Init:
                self.Update_Color()
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                Event_Bind(self._Frame, On_Hover_In=lambda E: self.On_Hover_In(E), On_Hover_Out=lambda E: self.On_Hover_Out(E))
                self._Frame.bind("<Configure>", self.On_Configure, add="+")
                self._Initialized = True
            if self._Radius:
                Temp_Background = self._Main._Background
            self._Frame.config(background=Temp_Background, width=self._Width, height=self._Height, highlightthickness=0)
            self.Rounded()
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
            
    def Rounded(self, Width=False, Height=False):
        try:
            for Each in self._Rounded:
                self._Frame.delete(Each)
            self._Rounded = []
            if not Width:
                Width = getattr(self, "_Width", 0)
            if not Height:
                Height = getattr(self, "_Height", 0)
            Radius = min(self._Radius, Width / 2, Height / 2) if Width>0 and Height>0 else 0
            X1 = self._Shadow_Size
            Y1 = self._Shadow_Size
            X2 = Width-self._Shadow_Size-1
            Y2 = Height-self._Shadow_Size-1
            Reducer = 0
            if not self._Shadow_Full:
                Reducer = self._Shadow_Size
            for i in range(self._Shadow_Size):
                Offset = self._Shadow_Size-i
                Intensity = (self._Shadow_Size-i) / self._Shadow_Size if self._Shadow_Size>0 else 0
                Shadow_Fill = self.Fade(self._Shadow_Color, Intensity) if self._Shadow_Size>0 else self._Shadow_Color
                self._Rounded.append(self.Round_Rectangle(X1-Offset+(Reducer/2), Y1-Offset+Reducer, X2+Offset-(Reducer/2), Y2+Offset, Radius, outline=Shadow_Fill, fill=Shadow_Fill, smooth=True))
            if self._Border_Size>0 and Width>0 and Height>0:
                self._Rounded.append(self.Round_Rectangle(X1, Y1, X2, Y2, Radius, outline=self._Border_Color, fill=self._Border_Color, smooth=True))
            X1 = self._Border_Size+self._Shadow_Size
            Y1 = self._Border_Size+self._Shadow_Size
            X2 = Width-self._Border_Size-self._Shadow_Size-1
            Y2 = Height-self._Border_Size-self._Shadow_Size-1
            if Width>0 and Height>0:
                self._Rounded.append(self.Round_Rectangle(X1, Y1, X2, Y2, Radius, outline=self._Background, fill=self._Background, smooth=True))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rounded -> {E}")
            
    def RGB(self, Color):
        try:
            return [int(Color[i:i+2], 16) for i in (1, 3, 5)]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> RGB -> {E}")
    
    def HEX(self, Color):
        try:
            return f'#{Color[0]:02x}{Color[1]:02x}{Color[2]:02x}'
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> HEX -> {E}")

    def Fade(self, Color, Intensity):
        try:
            R1, G1, B1 = self.RGB(Color)
            R2, G2, B2 = self.RGB(self._Main._Background)
            R = int(R1 + (R2 - R1) * Intensity)
            G = int(G1 + (G2 - G1) * Intensity)
            B = int(B1 + (B2 - B1) * Intensity)
            return self.HEX([R, G, B])
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> FADE -> {E}")
            
    def Points(self, Radius):
        try:
            Radius = math.ceil(Radius)
            if Radius<1:
                Radius = 1
            for i in range(Radius + 1):
                Angle = math.pi * (i / Radius) * 0.5
                X = (math.cos(Angle) - 1) * Radius
                Y = (math.sin(Angle) - 1) * Radius
                yield (X, Y)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Points -> {E}")
            
    def Round_Rectangle(self, X1, Y1, X2, Y2, Radius, **Args):
        try:
            if Radius>1:
                Points = []
                Cos_Sin_R = tuple(self.Points(Radius))
                for Cos_R, Sin_R in Cos_Sin_R:
                    Points.append((X2 + Sin_R, Y1 - Cos_R))
                for Cos_R, Sin_R in Cos_Sin_R:
                    Points.append((X2 + Cos_R, Y2 + Sin_R))
                for Cos_R, Sin_R in Cos_Sin_R:
                    Points.append((X1 - Sin_R, Y2 + Cos_R))
                for Cos_R, Sin_R in Cos_Sin_R:
                    Points.append((X1 - Cos_R, Y1 - Sin_R))
                return self._Frame.create_polygon(Points, **Args)
            else:
                del Args['smooth']
                return self._Frame.create_rectangle(X1, Y1, X2, Y2, **Args)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Round_Rectangle -> {E}")
            
    def Bbox(self, Item=False):
        try:
            if Item:
                return self._Frame.bbox(Item)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Position -> {E}")

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
            
    def Line(self, Name=False):
        try:
            Item = Canvas_Line(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Line -> {E}")
            
    def Polyline(self, Name=False):
        try:
            Item = Canvas_Polyline(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Polyline -> {E}")
                
    def Pie(self, Name=False):
        try:
            Item = Canvas_Pie(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Pie -> {E}")
                
    def Arc(self, Name=False):
        try:
            Item = Canvas_Arc(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Arc -> {E}")
                
    def Circle(self, Name=False):
        try:
            Item = Canvas_Circle(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Circle -> {E}")
                
    def Oval(self, Name=False):
        try:
            Item = Canvas_Oval(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Oval -> {E}")
            
    def Polygon(self, Name=False):
        try:
            Item = Canvas_Polygon(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Polygon -> {E}")
                
    def Rectangle(self, Name=False):
        try:
            Item = Canvas_Rectangle(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rectangle -> {E}")
                
    def RectangleR(self, Name=False):
        try:
            Item = Canvas_RectangleR(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> RectangleR -> {E}")
                
    def Image(self, Name=False):
        try:
            Item = Canvas_Image(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Image -> {E}")
            
    def Text(self, Name=False):
        try:
            Item = Canvas_Text(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Text -> {E}")
            
    def Text_Old(self, Name=False):
        try:
            Item = Canvas_Text_Old(self)
            if Name:
                Item.Config(Name=Name)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Text_Old -> {E}")
            
    def Player(self):
        try:
            Item = Player(self)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Player -> {E}")
            
    def Video(self):
        try:
            Item = Video(self)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Video -> {E}")
            
    def Editor(self):
        try:
            Item = Editor(self)
            return Item
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Editor -> {E}")