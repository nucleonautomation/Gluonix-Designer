# IMPORT LIBRARIES
import os
import threading, math, time
from io import BytesIO
import urllib
from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk
from .N_Custom import Event_Bind_Canvas
        
class Canvas_Image:
    
    def __init__(self, Main):
        self._Canvas = Main
        self._Config = ['Name', 'Width', 'Height', 'Left', 'Top', 'Animate_Left', 'Animate_Top', 'Animate_Width', 'Animate_Height', 'Animate_Time', 'Anchor', 'Photo', 'Resize', 'Rotate', 'Path', 'Path_Initial', 'Transparent', 'Skew_Horizontal', 'Skew_Vertical', 'Aspect_Ratio']
        self._Display = True
        self._Resize = True
        self._Name = False
        self._Last_Name = False
        self._Type = 'Canvas_Image'
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
        self._Anchor = 'nw'
        self._Image = False
        self._Image_Garbage = False
        self._Path = False
        self._Path_Memory = False
        self._Path_Initial = False
        self._Photo = False
        self._Transparent = True
        self._Rotate = 0
        self._Angle = 0
        self._Skew_Horizontal = 0
        self._Skew_Vertical = 0
        self._Aspect_Ratio = True
        self._Width, self._Height, self._Left, self._Top = 0, 0, 0, 0
        self._Widget = self._Canvas._Frame.create_image(0, 0, anchor=self._Anchor, image=None)
        self._Canvas._Widget.append(self)
        self._Canvas._Item.append(self)
        self._On_Show = False
        self._On_Hide = False
        self._On_Animate = False
        self._Is_Gif = False
        self._Gif_Frames = []
        self._Gif_Durations = []
        self._Gif_Loop = 1
        self._Gif_Index = 0
        self._Gif_Stop = threading.Event()
        self._Gif_Thread = None
        self._Gif_Running = False
        self._TK_Image = None
        self._Configure_After_Id = None

    def __str__(self):
        return "Nucleon_Glunoix_Canvas_Image[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Canvas_Image[]"

    def Copy(self, Name=False, Main=False):
        try:
            if not Main:
                Main = self._Canvas
            if Main._Type in ['Canvas', 'Scroll', 'Group']:
                Temp_Main = Main
                Temp_Type = Temp_Main._Type
                while Temp_Type=='Group':
                    Temp_Main = Temp_Main._Main
                    Temp_Type = Temp_Main._Type
                if Temp_Type=='Canvas' or Temp_Type=='Scroll':
                    Instance = type(self)(Main)
                    for Key in self._Config:
                        if hasattr(self, "_"+Key):
                            setattr(Instance, "_"+Key, getattr(self, "_"+Key))
                    if Name:
                        setattr(Instance, "_Name", Name)
                    Instance.Create()
                    return Instance
                else:
                    raise Exception('Widget can only copy to Canvas/Scroll')
            else:
                raise Exception('Widget can only copy to Canvas/Scroll')
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Copy -> {E}")
            
    def Delete(self):
        try:
            self.Animate_Cancel()
            if hasattr(self,'Stop'):
                self.Stop()
            self._Canvas._Widget.remove(self)
            self._Canvas._Frame.delete(self._Widget)
            if self:
                del self
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Delete -> {E}")

    def Hide(self):
        try:
            self.Animate_Cancel()
            if hasattr(self,'Stop'):
                self.Stop()
            self._Canvas._Frame.itemconfigure(self._Widget, state='hidden')
            self._Display = False
            if self._On_Hide:
                self._On_Hide()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Hide -> {E}")

    def Show(self):
        try:
            if not self._Display and self._Resize and self._Canvas._Type!='Scroll':
                self.Create()
            self._Canvas._Frame.itemconfigure(self._Widget, state='normal')
            self._Canvas._Frame.tag_raise(self._Widget)
            self._Display = True
            if self._On_Show:
                self._On_Show()
            self.Run()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Show -> {E}")
            
    def Animate(self, Hide=False, Thread=True):
        try:
            self.Animate_Cancel()
            Final_Left = float(self._Left)
            Final_Top = float(self._Top)
            Final_Width = float(self._Width)
            Final_Height = float(self._Height)
            Start_Left = float(self._Animate_Left)
            Start_Top = float(self._Animate_Top)
            Animate_Width = float(self._Animate_Width)
            Animate_Height = float(self._Animate_Height)
            Size_Anim = not (Animate_Width == 0 and Animate_Height == 0)
            Start_Width = Animate_Width if Size_Anim else Final_Width
            Start_Height = Animate_Height if Size_Anim else Final_Height
            Same_Pos = int(round(Start_Left)) == int(round(Final_Left)) and int(round(Start_Top)) == int(round(Final_Top))
            Same_Size = int(round(Start_Width)) == int(round(Final_Width)) and int(round(Start_Height)) == int(round(Final_Height))
            if Same_Pos and (not Size_Anim or Same_Size):
                self.Config(Left=int(round(Final_Left)), Top=int(round(Final_Top)), Width=int(round(Final_Width)), Height=int(round(Final_Height)))
                self.Show()
                return
            def Show_Start():
                if not self._Canvas._Frame.winfo_exists():
                    return
                self.Config(Left=int(round(Start_Left)), Top=int(round(Start_Top)), Width=int(round(Start_Width)), Height=int(round(Start_Height)))
            self._Canvas._Frame.after(0, Show_Start)
            Dx = Final_Left - Start_Left
            Dy = Final_Top - Start_Top
            Dw = Final_Width - Start_Width if Size_Anim else 0.0
            Dh = Final_Height - Start_Height if Size_Anim else 0.0
            Dist = math.hypot(math.hypot(Dx, Dy), math.hypot(Dw, Dh))
            if Dist == 0.0:
                def Snap_Same():
                    if not self._Canvas._Frame.winfo_exists():
                        return
                    self.Config(Left=int(round(Final_Left)), Top=int(round(Final_Top)), Width=int(round(Final_Width)), Height=int(round(Final_Height)))
                    self.Show()
                self._Canvas._Frame.after(0, Snap_Same)
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
                            if not self._Canvas._Frame.winfo_exists():
                                return
                            self.Config(Left=int(round(Final_Left)), Top=int(round(Final_Top)), Width=int(round(Final_Width)), Height=int(round(Final_Height)))
                            self._Animating = False
                            if Hide:
                                self.Hide()
                            if self._On_Animate:
                                self._On_Animate()
                        self._Canvas._Frame.after(0, Snap_Final)
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
                            if not self._Canvas._Frame.winfo_exists():
                                return
                            if self._Animating:
                                self.Config(Left=C[0], Top=C[1], Width=C[2], Height=C[3])
                        self._Canvas._Frame.after(0, Post)
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
            self._Canvas._GUI.Error(f"{self._Type} -> Animate -> {E}")
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
            self._Canvas._GUI.Error(f"{self._Type} -> Animate_Cancel -> {E}")
            
    def Clear(self):
        try:
            if self._Image:
                try:
                    self._Image.close()
                except:
                    pass
            self._Image = False
            self._Image_Width = 0
            self._Image_Height = 0
            self._Canvas._Frame.itemconfig(self._Widget, image=None)
            self._TK_Image = None
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Clear -> {E}")

    def Set(self, Path):
        try:
            if hasattr(self,'Stop'):
                self.Stop()
            self._Path = Path
            self._Path_Memory = self._Path
            if isinstance(Path, str):
                Url_Parsed = urllib.parse.urlparse(Path)
                if Url_Parsed.scheme in ("http", "https") or self.Is_Large_File(Path):
                    self.Async_Open(Path)
                    return
            self.Open()
            self.Load()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Set -> {E}")

    def Initial(self):
        try:
            if self._Path_Initial:
                if hasattr(self,'Stop'):
                    self.Stop()
                self.Set(self._Path_Initial)
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Initial -> {E}")
            
    def Refresh(self):
        try:
            if self._Path:
                self.Set(self._Path)
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Refresh -> {E}")
        
    def Bind(self, **Input):
        try:
            if 'On_Show' in Input:
                self._On_Show = Input['On_Show']
            if 'On_Hide' in Input:
                self._On_Hide = Input['On_Hide']
            if 'On_Animate' in Input:
                self._On_Animate = Input['On_Animate']
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
                self.Create()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Config -> {E}")
            
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
            self._Canvas._GUI.Error(f"{self._Type} -> Move -> {E}")
            
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
            self._Canvas._GUI.Error(f"{self._Type} -> Center -> {E}")
        
    def Position(self, Left=None, Top=None):
        try:
            if Left is not None:
                self._Left = Left
            if Top is not None:
                self._Top = Top
            if Left is not None or Top is not None:
                self.Create()
            return [self._Left, self._Top]
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Position -> {E}")
            
    def Size(self, Width=False, Height=False):
        try:
            if Width:
                self._Width = Width
            if Height:
                self._Height = Height
            if Width or Height:
                self.Create()
            return [self._Width, self._Height]
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Size -> {E}")
            
    def Box(self):
        try:
            Box = self._Canvas._Frame.bbox(self._Widget)
            X1, Y1, X2, Y2 = Box
            Width = X2 - X1
            Height = Y2 - Y1
            return [X1, Y1, Width, Height]
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Box -> {E}")

    def Is_Large_File(self, Path):
        try:
            if isinstance(Path, str) and os.path.exists(Path):
                Threshold_Bytes = 8*1024*1024
                return os.path.getsize(Path) > Threshold_Bytes
            return False
        except Exception:
            return False

    def Async_Open(self, Path):
        try:
            Path_Obj = Path
            def Worker():
                try:
                    Data_Bytes = None
                    if isinstance(Path_Obj, str):
                        Url_Parsed = urllib.parse.urlparse(Path_Obj)
                        if Url_Parsed.scheme in ("http", "https"):
                            with urllib.request.urlopen(Path_Obj) as Response:
                                Data_Bytes = Response.read()
                        elif os.path.exists(Path_Obj):
                            with open(Path_Obj, "rb") as File_Handle:
                                Data_Bytes = File_Handle.read()
                                if not self._Path_Initial:
                                    self._Path_Initial = Path_Obj
                    if not Data_Bytes:
                        def Post_Clear():
                            self.Clear()
                        self._Canvas._Frame.after(0, Post_Clear)
                        return
                    with PIL_Image.open(BytesIO(Data_Bytes)) as Pil_Obj:
                        Is_Gif = False
                        Gif_Frames = []
                        Gif_Durations = []
                        Gif_Loop = 1
                        if getattr(Pil_Obj, "is_animated", False):
                            Is_Gif = True
                            try:
                                Gif_Loop = int(Pil_Obj.info.get("loop", 1))
                            except:
                                Gif_Loop = 1
                            Frame_Count = getattr(Pil_Obj, "n_frames", 0) or 0
                            Frame_Index = 0
                            while True:
                                try:
                                    Pil_Obj.seek(Frame_Index)
                                    Frame_Image = Pil_Obj.convert("RGBA").copy()
                                    Duration = int(Pil_Obj.info.get("duration", 100))
                                    Gif_Frames.append(Frame_Image)
                                    Gif_Durations.append(max(1, Duration))
                                    Frame_Index += 1
                                    if Frame_Count and Frame_Index >= Frame_Count:
                                        break
                                except EOFError:
                                    break
                            if Gif_Frames:
                                Image_Obj = Gif_Frames[0]
                            else:
                                Is_Gif = False
                                Image_Obj = Pil_Obj.copy()
                        else:
                            Image_Obj = Pil_Obj.copy()
                        Image_Width, Image_Height = Image_Obj.size
                    def Post():
                        try:
                            if Path_Obj != self._Path:
                                return
                            self._Is_Gif = Is_Gif
                            self._Gif_Frames = Gif_Frames
                            self._Gif_Durations = Gif_Durations
                            self._Gif_Loop = Gif_Loop
                            self._Gif_Index = 0
                            self._Image = Image_Obj
                            self._Image_Width = Image_Width
                            self._Image_Height = Image_Height
                            self.Load()
                        except Exception as E2:
                            self._Canvas._GUI.Error(f"{self._Type} -> Async_Open -> {E2}")
                    self._Canvas._Frame.after(0, Post)
                except Exception as E3:
                    def Post_Error():
                        self.Clear()
                        self._Canvas._GUI.Error(f"{self._Type} -> Async_Open -> {E3}")
                    self._Canvas._Frame.after(0, Post_Error)
            Thread_Obj = threading.Thread(target=Worker, daemon=True)
            Thread_Obj.start()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Async_Open -> {E}")
   
    def Open(self):
        try:
            if hasattr(self, "Stop"):
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
            Type_Module = getattr(type(Path_Obj), "__module__", "")
            Type_Name = type(Path_Obj).__name__
            if Type_Name.endswith("PhotoImage") or ("ImageTk" in Type_Module) or ("tkinter" in Type_Module):
                if Path_Obj:
                    self._Image = Path_Obj
                return
            if hasattr(Path_Obj, "__array_interface__") or Type_Module.startswith("numpy"):
                if Path_Obj is not None:
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
            Data_Bytes = None
            if isinstance(Path_Obj, str):
                Url_Parsed = urllib.parse.urlparse(Path_Obj)
                if Url_Parsed.scheme in ("http", "https"):
                    with urllib.request.urlopen(Path_Obj) as Response:
                        Data_Bytes = Response.read()
                elif os.path.exists(Path_Obj):
                    with open(Path_Obj, "rb") as File_Handle:
                        Data_Bytes = File_Handle.read()
                    if not self._Path_Initial:
                        self._Path_Initial = Path_Obj
                else:
                    self.Clear()
                    return
            else:
                self.Clear()
                return
            with PIL_Image.open(BytesIO(Data_Bytes)) as Pil_Obj:
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
            self.Clear()
            self._Canvas._GUI.Error(f"{self._Type} -> Open -> {E}")

    def Convert(self):
        try:
            if not self._Image:
                return False
            if self._Resize and self._Canvas._Type!='Scroll':
                Left, Right, Width, Height = self._Canvas.Box()
                Width_Ratio = Width/self._Canvas._Width
                Height_Ratio = Height/self._Canvas._Height
            else:
                Width_Ratio = 1
                Height_Ratio = 1
            Temp_Image = self._Image.rotate(self._Rotate + self._Angle, PIL_Image.NEAREST, expand=1)
            if self._Transparent:
                Temp_Image = Temp_Image.convert('RGBA')
            else:
                Temp_Image = Temp_Image.convert('HSV')
            W_Orig, H_Orig = Temp_Image.size
            W_Tgt = int(max(1, round(self._Width*Width_Ratio)))
            H_Tgt = int(max(1, round(self._Height*Height_Ratio)))
            if W_Tgt<=0 or H_Tgt<=0:
                W_Tgt = max(1, W_Orig)
                H_Tgt = max(1, H_Orig)
            if getattr(self, "_Aspect_Ratio", True):
                Image_Aspect = W_Orig/H_Orig if H_Orig!=0 else 1.0
                Frame_Aspect = W_Tgt/H_Tgt if H_Tgt!=0 else 1.0
                if Image_Aspect>Frame_Aspect:
                    New_Width = W_Tgt
                    New_Height = int(max(1, round(W_Tgt/Image_Aspect)))
                else:
                    New_Height = H_Tgt
                    New_Width = int(max(1, round(H_Tgt*Image_Aspect)))
                Temp_Image = Temp_Image.resize((New_Width, New_Height), PIL_Image.NEAREST)
            else:
                Temp_Image = Temp_Image.resize((W_Tgt, H_Tgt), PIL_Image.NEAREST)
            W, H = Temp_Image.size
            Skew_X = max(-100.0, min(100.0, float(self._Skew_Horizontal or 0.0)))
            Skew_Y = max(-100.0, min(100.0, float(self._Skew_Vertical or 0.0)))
            Delta_X = min((W - 1) * 0.5, (abs(Skew_X) / 100.0) * (W * 0.5))
            Delta_Y = min((H - 1) * 0.5, (abs(Skew_Y) / 100.0) * (H * 0.5))
            TL_X = 0.0
            TL_Y = 0.0
            TR_X = float(W)
            TR_Y = 0.0
            BR_X = float(W)
            BR_Y = float(H)
            BL_X = 0.0
            BL_Y = float(H)
            if Skew_X > 0:
                TL_X = Delta_X
                TR_X = W - Delta_X
            elif Skew_X < 0:
                BL_X = Delta_X
                BR_X = W - Delta_X
            if Skew_Y > 0:
                TR_Y = Delta_Y
                BR_Y = H - Delta_Y
            elif Skew_Y < 0:
                TL_Y = Delta_Y
                BL_Y = H - Delta_Y
            if Delta_X == 0 and Delta_Y == 0:
                return PIL_ImageTk.PhotoImage(Temp_Image)
            Src_Points = [(0.0, 0.0), (float(W), 0.0), (float(W), float(H)), (0.0, float(H))]
            Dst_Points = [(TL_X, TL_Y), (TR_X, TR_Y), (BR_X, BR_Y), (BL_X, BL_Y)]
            A = []
            B_Vals = []
            for (X, Y), (U, V) in zip(Dst_Points, Src_Points):
                A.append([X, Y, 1, 0, 0, 0, -U * X, -U * Y])
                B_Vals.append(U)
                A.append([0, 0, 0, X, Y, 1, -V * X, -V * Y])
                B_Vals.append(V)
            N = 8
            for I in range(N):
                A[I].append(B_Vals[I])
            for Col in range(N):
                Pivot = max(range(Col, N), key=lambda R: abs(A[R][Col]))
                if abs(A[Pivot][Col]) < 1e-12:
                    continue
                if Pivot != Col:
                    A[Col], A[Pivot] = A[Pivot], A[Col]
                Pivot_Val = A[Col][Col]
                Inv_Pivot = 1.0 / Pivot_Val
                for J in range(Col, N + 1):
                    A[Col][J] *= Inv_Pivot
                for R in range(Col + 1, N):
                    Factor = A[R][Col]
                    if Factor != 0.0:
                        for J in range(Col, N + 1):
                            A[R][J] -= Factor * A[Col][J]
            Coeffs = [0.0] * N
            for I in reversed(range(N)):
                S = A[I][N]
                for J in range(I + 1, N):
                    S -= A[I][J] * Coeffs[J]
                Coeffs[I] = S
            try:
                Warped_Image = Temp_Image.transform((W, H), PIL_Image.PERSPECTIVE, Coeffs, resample=PIL_Image.BICUBIC, fillcolor=(0, 0, 0, 0) if self._Transparent else None)
            except TypeError:
                Background_Image = PIL_Image.new('RGBA' if self._Transparent else Temp_Image.mode, (W, H), (0, 0, 0, 0) if self._Transparent else 0)
                Warped_Image = Temp_Image.transform((W, H), PIL_Image.PERSPECTIVE, Coeffs, resample=PIL_Image.BICUBIC)
                if self._Transparent and Warped_Image.mode != 'RGBA':
                    Warped_Image = Warped_Image.convert('RGBA')
                Background_Image.paste(Warped_Image, (0, 0), Warped_Image.split()[3] if self._Transparent and Warped_Image.mode == 'RGBA' else None)
                Warped_Image = Background_Image
            return PIL_ImageTk.PhotoImage(Warped_Image)
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Convert -> {E}")
            return False

    def Load(self):
        try:
            if self._Image:
                Image = self._Image if self._Photo else self.Convert()
                if not Image:
                    return
                self._Canvas._Frame.itemconfig(self._Widget, image=Image)
                self._TK_Image = Image
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Load -> {E}")

    def Create(self):
        try:
            if self._Resize and self._Canvas._Type!='Scroll':
                Left, Right, Width, Height = self._Canvas.Box()
                Width_Ratio = Width/self._Canvas._Width
                Height_Ratio = Height/self._Canvas._Height
            else:
                Width_Ratio = 1
                Height_Ratio = 1
            self._X = self._Left
            self._Y = self._Top
            self._Canvas._Frame.itemconfig(self._Widget, anchor=self._Anchor)
            self._Canvas._Frame.coords(self._Widget, self._X*Width_Ratio, self._Y*Height_Ratio)
            if not self._Image:
                self.Open()
            self.Load()
            if self._Name!=self._Last_Name:
                if self._Last_Name:
                    if self._Last_Name in self._Canvas.__dict__:
                        del self._Canvas.__dict__[self._Last_Name]
                if self._Name:
                    self._Canvas.__dict__[self._Name] = self
                self._Last_Name = self._Name
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Create -> {E}")
            
    def Resize(self, Event):
        try:
            self._Canvas._Frame.itemconfigure(self._Widget, state='normal')
            self._Canvas._Frame.tag_raise(self._Widget)
            if self._Configure_After_Id is not None:
                self._Canvas._Frame.after_cancel(self._Configure_After_Id)
            self._Configure_After_Id = self._Canvas._Frame.after(50, self.On_Resize_Debounced)
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Resize -> {E}")

    def On_Resize_Debounced(self):
        try:
            self._Configure_After_Id = None
            if not self._Display:
                return
            self.Create()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> On_Resize_Debounced -> {E}")

    def Rotate(self, Value=0):
        try:
            self._Angle+=Value
            self.Load()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Rotate -> {E}")
            
    def Run(self):
        try:
            if not getattr(self,"_Is_Gif",False) or len(getattr(self,"_Gif_Frames",[]))==0:
                return
            if self._Gif_Running:
                return
            self._Gif_Stop.clear()
            self._Gif_Running=True
            def Worker():
                Loops=0
                while self._Gif_Running and not self._Gif_Stop.is_set():
                    if not self._Canvas._Frame.winfo_exists():
                        break
                    Frame=self._Gif_Frames[self._Gif_Index]
                    Dur=self._Gif_Durations[self._Gif_Index]
                    def Post(F=Frame):
                        if not self._Canvas._Frame.winfo_exists():
                            return
                        self._Image=F
                        self._Image_Width,self._Image_Height=F.size
                        self.Load()
                    self._Canvas._Frame.after(0,Post)
                    if self._Gif_Stop.wait(Dur/1000.0):
                        break
                    self._Gif_Index=(self._Gif_Index+1)%len(self._Gif_Frames)
                    if self._Gif_Index==0:
                        Loops+=1
                        if self._Gif_Loop!=0 and Loops>=self._Gif_Loop:
                            break
                self._Gif_Running=False
            self._Gif_Thread=threading.Thread(target=Worker,daemon=True)
            self._Gif_Thread.start()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Run -> {E}")

    def Stop(self):
        try:
            if self._Gif_Thread and self._Gif_Thread.is_alive():
                self._Gif_Running=False
                self._Gif_Stop.set()
                self._Gif_Thread.join(timeout=0.2)
            self._Gif_Stop.clear()
            self._Gif_Thread=None
            self._Gif_Index=0
            if self._Is_Gif and len(self._Gif_Frames)>0:
                self._Image=self._Gif_Frames[0]
                self._Image_Width,self._Image_Height=self._Image.size
                self.Load()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Stop -> {E}")