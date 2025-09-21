# IMPORT LIBRARIES
import os
from io import BytesIO
import urllib
from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk
import tkinter as TK
import threading, math, time
from .N_GUI import GUI
from .N_Custom import Event_Bind

PIL_Image.MAX_IMAGE_PIXELS = None

class Image_Lite:
    
    def __init__(self, Main, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Image_Lite"
            try:
                self._Config = ['Name', 'Auto_Dark', 'Background', 'Light_Background', 'Dark_Background', 'Use_Foreground', 'Foreground', 'Light_Foreground', 'Dark_Foreground', 'Resize_Width', 'Resize', 'Resize_Height', 'Move', 'Move_Left', 'Move_Top', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height', 'Animate_Left', 'Animate_Top', 'Animate_Width', 'Animate_Height', 'Animate_Time', 'Path', 'Path_Initial', 'Rotate', 'Transparent', 'Aspect_Ratio', 'Convert_Type', 'Tolerance', 'Hover_Background', 'Light_Hover_Background', 'Dark_Hover_Background', 'Hover_Foreground']
                self._Initialized = False
                self._Name = False
                self._Last_Name = False
                self._Resize_Font, self._Resize, self._Resize_Width, self._Resize_Height, self._Move, self._Move_Left, self._Move_Top = False, True, True, True, True, True, True
                self._Popup = False
                self._Display = True
                self._Size_Update = False
                self._Resize_Index = 0
                self._Main = Main
                self._Widget = TK.Label(self._Main._Frame)
                self._Background = self._Main._Background
                self._Background_Main = True
                self._Use_Foreground = False
                self._Foreground = False
                self._Hover_Background = False
                self._Hover_Foreground = False
                self._Last_Background = False
                self._Last_Foreground = False
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
                self._Tolerance = 10
                self._Image = False
                self._Path = False
                self._Path_Memory = False
                self._Path_Initial = False
                self._Rotate = 0
                self._Angle = 0
                self._Transparent = True
                self._Aspect_Ratio = True
                self._Convert_Type = 'RGBA'
                self._Resizable = self._Main._Resizable
                self._Auto_Dark = True
                self._On_Show = False
                self._On_Hide = False
                self._On_Animate = False
                self._On_Hover_In = False
                self._On_Hover_Out = False
                self._Is_Gif = False
                self._Gif_Frames = []
                self._Gif_Durations = []
                self._Gif_Loop = 1
                self._Gif_Index = 0
                self._Gif_Stop = threading.Event()
                self._Gif_Thread = None
                self._Gif_Running = False
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")
    
    def __str__(self):
        return "Nucleon_Glunoix_Image_Lite[]"
    
    def __repr__(self):
        return "Nucleon_Glunoix_Image_Lite[]"
    
    def Copy(self, Name=False, Main=False):
        try:
            if not Main:
                Main = self._Main
            Instance = type(self)(Main)
            for Key in self._Config:
                if hasattr(self, "_"+Key):
                    setattr(Instance, "_"+Key, getattr(self, "_"+Key))
            setattr(Instance, "_Name", Name)
            Instance.Create()
            return Instance
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Copy -> {E}")
    
    def Delete(self):
        try:
            self.Animate_Cancel()
            self.Stop()
            self._Main._Widget.remove(self)
            self._Widget.destroy()
            if self:
                del self
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete -> {E}")
    
    def Hide(self):
        try:
            self.Animate_Cancel()
            self.Stop()
            self._Widget.place_forget()
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
            self.Run()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Show -> {E}")
    
    def Display(self):
        try:
            if self._Animating:
                return
            self._Widget.place(x=self._Left_Current, y=self._Top_Current, width=self._Width_Current, height=self._Height_Current)
            self._Widget.lift()
            self._Display = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Display -> {E}")
    
    def Grab(self, Path=False):
        try:
            return self._GUI.Grab_Widget(Path=Path, Widget=self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Grab -> {E}")
    
    def Animate(self, Hide=False):
        try:
            self.Animate_Cancel()
            if not hasattr(self, "_Width_Current") or not hasattr(self, "_Height_Current"):
                self.Resize(Trigger=False)
            Final_Left = float(self._Left)
            Final_Top = float(self._Top)
            Final_Width = float(self._Width_Current)
            Final_Height = float(self._Height_Current)
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
                self._Widget.place(x=int(round(Final_Left)), y=int(round(Final_Top)), width=int(round(Final_Width)), height=int(round(Final_Height)))
                self._Widget.lift()
                self._Display = True
                return
            def Show_Start():
                if not self._Widget.winfo_exists():
                    return
                self._Widget.place(x=int(round(Start_Left)), y=int(round(Start_Top)), width=int(round(Start_Width)), height=int(round(Start_Height)))
                self._Widget.lift()
                self._Display = True
            self._GUI._Frame.after(0, Show_Start)
            Dx = Final_Left - Start_Left
            Dy = Final_Top - Start_Top
            Dw = Final_Width - Start_Width if Size_Anim else 0.0
            Dh = Final_Height - Start_Height if Size_Anim else 0.0
            Dist = math.hypot(math.hypot(Dx, Dy), math.hypot(Dw, Dh))
            if Dist == 0.0:
                def Snap_Same():
                    if not self._Widget.winfo_exists():
                        return
                    self._Widget.place(x=int(round(Final_Left)), y=int(round(Final_Top)), width=int(round(Final_Width)), height=int(round(Final_Height)))
                    self._Widget.lift()
                    self._Display = True
                self._GUI._Frame.after(0, Snap_Same)
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
                            if not self._Widget.winfo_exists():
                                return
                            self._Widget.place(x=int(round(Final_Left)), y=int(round(Final_Top)), width=int(round(Final_Width)), height=int(round(Final_Height)))
                            self._Animating = False
                            if Hide:
                                self.Hide()
                            if self._On_Animate:
                                self._On_Animate()
                        self._GUI._Frame.after(0, Snap_Final)
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
                                self._Widget.place(x=C[0], y=C[1], width=C[2], height=C[3])
                        self._GUI._Frame.after(0, Post)
                    Next_Tick += Frame_Interval
                    Sleep_For = Next_Tick - time.perf_counter()
                    if Sleep_For < -2 * Frame_Interval:
                        Next_Tick = time.perf_counter()
                        Sleep_For = Frame_Interval
                    if Sleep_For > 0:
                        time.sleep(Sleep_For)
            self.Show()
            T = threading.Thread(target=Worker, daemon=True)
            self._Anim_Thread = T
            T.start()
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
    
    def Set(self, Path):
        try:
            self.Stop()
            self._Path = Path
            self._Path_Memory = self._Path
            self.Open()
            self.Relocate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Set -> {E}")
    
    def Initial(self):
        try:
            if self._Path_Initial:
                if hasattr(self,'Stop'):
                    self.Stop()
                self.Set(self._Path_Initial)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Initial -> {E}")
    
    def Reset(self):
        try:
            self._Angle = 0
            self.Open()
            self.Relocate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Reset -> {E}")
    
    def Refresh(self):
        try:
            self.Open()
            self.Relocate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Refresh -> {E}")
    
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
            if 'On_Animate' in Input:
                self._On_Animate = Input['On_Animate']
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
                Config['Background'] = self._Last_Background if self._Background==self._Hover_Background else self._Background
            if self._Hover_Foreground and self._Last_Foreground:
                Config['Foreground'] = self._Last_Foreground if self._Foreground==self._Hover_Foreground else self._Foreground
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
                self.Relocate()
            return [self._Left, self._Top]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Position -> {E}")
    
    def Size(self, Width=False, Height=False):
        try:
            if Width:
                self._Width = Width
            if Height:
                self._Height = Height
            if Width or Height:
                self.Relocate()
            return [self._Width, self._Height]
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Size -> {E}")
    
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
                self._Width_Current, self._Height_Current, self._Left_Current, self._Top_Current, = self._Width, self._Height, self._Left, self._Top
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                Event_Bind(self._Widget, On_Hover_In=lambda E: self.On_Hover_In(E), On_Hover_Out=lambda E: self.On_Hover_Out(E))
                self._Initialized = True
            self._Widget.config(background=self._Background)
            if isinstance(self._Path, str) and isinstance(self._Path_Memory, str):
                if self._Path != self._Path_Memory:
                    self._Path_Memory = self._Path
                    self.Open()
            elif isinstance(self._Path, list) and isinstance(self._Path_Memory, list):
                if not all(a == b for a, b in zip(self._Path, self._Path_Memory)):
                    self._Path_Memory = self._Path
                    self.Open()
            elif type(self._Path) != type(self._Path_Memory):
                self._Path_Memory = self._Path
                self.Open()
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
    
    def Update_Color(self):
        try:
            self._GUI.Initiate_Colors(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Color -> {E}")
    
    def RGB(self, HEX):
        try:
            if HEX.startswith('#'):
                HEX = HEX[1:]
            R = int(HEX[0:2], 16)
            G = int(HEX[2:4], 16)
            B = int(HEX[4:6], 16)
            return (R, G, B)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> RGB -> {E}")
    
    def Open(self):
        try:
            self.Stop()
            self._Is_Gif = False
            self._Gif_Frames = []
            self._Gif_Durations = []
            self._Gif_Loop = 1
            self._Gif_Index = 0
            if self._Image:
                try:
                    self._Image.close()
                except:
                    pass
            self._Image = False
            Path_Obj = self._Path
            if hasattr(Path_Obj, "__array_interface__") or (hasattr(Path_Obj, "__class__") and getattr(type(Path_Obj), "__module__", "").startswith("numpy")):
                self._Image = PIL_Image.fromarray(Path_Obj)
                self._Image_Width, self._Image_Height = self._Image.size
                return
            if isinstance(Path_Obj, PIL_Image.Image):
                Pil_Obj = Path_Obj
                if getattr(Pil_Obj, "is_animated", False):
                    self._Is_Gif = True
                    try:
                        self._Gif_Loop = int(getattr(Pil_Obj, "info", {}).get("loop", 1))
                    except:
                        self._Gif_Loop = 1
                    Frame_Count = getattr(Pil_Obj, "n_frames", 0) or 0
                    Frame_Index = 0
                    while True:
                        try:
                            Pil_Obj.seek(Frame_Index)
                            Frame_Image = Pil_Obj.convert("RGBA").copy()
                            Duration = int(getattr(Pil_Obj, "info", {}).get("duration", 100))
                            self._Gif_Frames.append(Frame_Image)
                            self._Gif_Durations.append(max(1, Duration))
                            Frame_Index += 1
                            if Frame_Count and Frame_Index >= Frame_Count:
                                break
                        except EOFError:
                            break
                    if self._Gif_Frames:
                        self._Image = self._Gif_Frames[0]
                        self._Image_Width, self._Image_Height = self._Image.size
                    else:
                        self._Is_Gif = False
                        self._Image = Pil_Obj.copy()
                        self._Image_Width, self._Image_Height = self._Image.size
                else:
                    self._Image = Pil_Obj.copy()
                    self._Image_Width, self._Image_Height = self._Image.size
                return
            Data = None
            if isinstance(Path_Obj, str):
                Parsed = urllib.parse.urlparse(Path_Obj)
                if Parsed.scheme in ("http", "https"):
                    with urllib.request.urlopen(Path_Obj) as Response:
                        Data = Response.read()
                elif os.path.exists(Path_Obj):
                    with open(Path_Obj, "rb") as File_Handle:
                        Data = File_Handle.read()
                    if not self._Path_Initial:
                        self._Path_Initial = Path_Obj
                else:
                    self._Widget.configure(image=None)
                    self._Widget.image=None
                    return
            else:
                self._Widget.configure(image=None)
                self._Widget.image=None
                return
            with PIL_Image.open(BytesIO(Data)) as Pil_Obj:
                if getattr(Pil_Obj, "is_animated", False):
                    self._Is_Gif = True
                    try:
                        self._Gif_Loop = int(Pil_Obj.info.get("loop", 1))
                    except:
                        self._Gif_Loop = 1
                    Frame_Count = getattr(Pil_Obj, "n_frames", 0) or 0
                    Frame_Index = 0
                    while True:
                        try:
                            Pil_Obj.seek(Frame_Index)
                            Frame_Image = Pil_Obj.convert("RGBA").copy()
                            Duration = int(Pil_Obj.info.get("duration", 100))
                            self._Gif_Frames.append(Frame_Image)
                            self._Gif_Durations.append(max(1, Duration))
                            Frame_Index += 1
                            if Frame_Count and Frame_Index >= Frame_Count:
                                break
                        except EOFError:
                            break
                    if self._Gif_Frames:
                        self._Image = self._Gif_Frames[0]
                        self._Image_Width, self._Image_Height = self._Image.size
                    else:
                        self._Is_Gif = False
                        self._Image = Pil_Obj.copy()
                        self._Image_Width, self._Image_Height = self._Image.size
                else:
                    self._Image = Pil_Obj.copy()
                    self._Image_Width, self._Image_Height = self._Image.size
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Open -> {E}")

    def Convert(self, Frame_Width, Frame_Height):
        try:
            Temp_Image = self._Image.rotate(self._Rotate+self._Angle, PIL_Image.NEAREST, expand=0)
            Image_Ratio = self._Image_Width / self._Image_Height
            Frame_Ratio = Frame_Width / Frame_Height
            if Image_Ratio>=Frame_Ratio:
                Width = Frame_Width
                Width_Ratio = Width / self._Image_Width
                Height = self._Image_Height * Width_Ratio
                Top = (Frame_Height - Height) / 2
                Left = 0
            if Image_Ratio<Frame_Ratio:
                Height = Frame_Height
                Height_Ratio = Height / self._Image_Height
                Width = self._Image_Width * Height_Ratio
                Top = 0
                Left = (Frame_Width - Width) / 2
            if self._Transparent:
                if self._Convert_Type=='RGBA' and self._Foreground and self._Use_Foreground:
                    Temp_Image = Temp_Image.convert(self._Convert_Type)
                    Temp_Color = self.RGB(self._Foreground)
                    Pixel_Data = Temp_Image.load()
                    Temp_Width, Temp_Height = Temp_Image.size
                    for Y in range(Temp_Height):
                        for X in range(Temp_Width):
                            R, G, B, A = Pixel_Data[X, Y]
                            if R == 0 and G == 0 and B == 0:
                                Pixel_Data[X, Y] = (*Temp_Color, A)
            if self._Aspect_Ratio:
                Temp_Image = Temp_Image.resize((int(Width), int(Height)), PIL_Image.NEAREST)
            else:
                Temp_Image = Temp_Image.resize((int(self._Width_Current), int(self._Height_Current)), PIL_Image.NEAREST)
            Temp_Image_TK = PIL_ImageTk.PhotoImage(Temp_Image)
            return {"Image": Temp_Image_TK, "Top": Top, "Left": Left}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Convert -> {E}")
    
    def Load(self):
        try:
            if self._Height_Current>0 and self._Width_Current>0:
                Image = self.Convert(self._Width_Current, self._Height_Current)
                self._Widget.configure(image=Image['Image'])
                self._Widget.image = Image['Image']
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Load -> {E}")
    
    def Rotate(self, Value=0):
        try:
            self._Angle+=Value
            self.Load()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Rotate -> {E}")
    
    def Adjustment(self):
        try:
            Width_Difference = self._Main._Width_Current - self._Main._Width
            Height_Difference = self._Main._Height_Current - self._Main._Height
            Width_Ratio = self._Width / (self._Main._Width - self._Main._Border_Size * 2)
            Height_Ratio = self._Height / (self._Main._Height - self._Main._Border_Size * 2)
            Center_X = self._Left + self._Width / 2
            Center_Y = self._Top + self._Height / 2
            Is_Right = Center_X > self._Main._Width / 2
            Is_Bottom = Center_Y > self._Main._Height / 2
            self._Width_Adjustment = Width_Difference * Width_Ratio
            self._Height_Adjustment = Height_Difference * Height_Ratio
            if Is_Right:
                Distance_From_Right = self._Main._Width - (self._Left + self._Width)
                Ratio = Distance_From_Right / self._Main._Width
                self._Left_Adjustment = Width_Difference * (1 - Ratio) - self._Width_Adjustment
            else:
                Ratio = self._Left / self._Main._Width
                self._Left_Adjustment = Width_Difference * Ratio
            if Is_Bottom:
                Distance_From_Bottom = self._Main._Height - (self._Top + self._Height)
                Ratio = Distance_From_Bottom / self._Main._Height
                self._Top_Adjustment = Height_Difference * (1 - Ratio) - self._Height_Adjustment
            else:
                Ratio = self._Top / self._Main._Height
                self._Top_Adjustment = Height_Difference * Ratio
            if not self._Resize_Width and self._Move_Left and Is_Right:
                self._Left_Adjustment += self._Width_Adjustment
            if not self._Resize_Height and self._Move_Top and Is_Bottom:
                self._Top_Adjustment += self._Height_Adjustment
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Adjustment -> {E}")
    
    def Relocate(self, Direct=False):
        try:
            if self._Animating and not Direct:
                return
            if Direct or self._Resizable:
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
            else:
                self._Width_Current = self._Width
                self._Height_Current = self._Height
                self._Left_Current = self._Left
                self._Top_Current = self._Top
            if self._Image:
                self.Load()
            if self._Display:
                self.Display()
                self.Run()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Relocate -> {E}")
    
    def Resize(self):
        try:
            self._Resize_Index = self._GUI._Resize_Index
            self.Relocate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Resize -> {E}")
    
    def Run(self):
        try:
            if not self._Is_Gif or len(self._Gif_Frames)==0:
                return
            if self._Gif_Running:
                return
            self._Gif_Stop.clear()
            self._Gif_Running = True
            def Worker():
                Loops = 0
                while self._Gif_Running and not self._Gif_Stop.is_set():
                    if not self._Widget.winfo_exists():
                        break
                    Frame = self._Gif_Frames[self._Gif_Index]
                    Dur = self._Gif_Durations[self._Gif_Index]
                    def Post(F=Frame):
                        if not self._Widget.winfo_exists():
                            return
                        self._Image = F
                        self._Image_Width, self._Image_Height = F.size
                        self.Load()
                    self._GUI._Frame.after(0, Post)
                    if self._Gif_Stop.wait(Dur/1000.0):
                        break
                    self._Gif_Index = (self._Gif_Index+1) % len(self._Gif_Frames)
                    if self._Gif_Index==0:
                        Loops += 1
                        if self._Gif_Loop!=0 and Loops>=self._Gif_Loop:
                            break
                self._Gif_Running = False
            self._Gif_Thread = threading.Thread(target=Worker, daemon=True)
            self._Gif_Thread.start()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Run -> {E}")
    
    def Stop(self):
        try:
            if self._Gif_Thread and self._Gif_Thread.is_alive():
                self._Gif_Running = False
                self._Gif_Stop.set()
                self._Gif_Thread.join(timeout=0.2)
            self._Gif_Stop.clear()
            self._Gif_Thread = None
            self._Gif_Index = 0
            if self._Is_Gif and len(self._Gif_Frames)>0:
                self._Image = self._Gif_Frames[0]
                self._Image_Width, self._Image_Height = self._Image.size
                self.Load()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Stop -> {E}")
