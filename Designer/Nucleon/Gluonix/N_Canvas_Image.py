# IMPORT LIBRARIES
import os
import threading, math, time
from io import BytesIO
from requests import get as requests_get
from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk
from .N_Custom import Event_Bind_Canvas
        
class Canvas_Image:
    
    def __init__(self, Main):
        self._Canvas = Main
        self._Config = ['Name', 'Width', 'Height', 'Left', 'Top', 'Animate_Left', 'Animate_Top', 'Animate_Width', 'Animate_Height', 'Animate_Time', 'Anchor', 'Url', 'Array', 'Pil', 'Photo', 'Resize', 'Rotate', 'Path', 'Path_Initial', 'Transparent', 'Skew_Horizontal', 'Skew_Vertical']
        self._Display = True
        self._Resize_Index = 0
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
        self._Url = False
        self._Array = False
        self._Pil = False
        self._Photo = False
        self._Transparent = True
        self._Rotate = 0
        self._Angle = 0
        self._Skew_Horizontal = 0
        self._Skew_Vertical = 0
        self._Width, self._Height, self._Width_Old, self._Height_Old, self._Left, self._Top = 0, 0, 0, 0, 0, 0
        self._Widget = self._Canvas._Frame.create_image(0, 0, anchor=self._Anchor, image=None)
        self._Canvas._Widget.append(self)
        self._Resizable = self._Canvas._Resizable
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
                    Temp_Main = Main._Main
                    Temp_Type = Temp_Main._Type
                if Temp_Type=='Canvas' or Temp_Type=='Scroll':
                    Instance = type(self)(Main)
                    for Key in self._Config:
                        if hasattr(self, "_"+Key):
                            setattr(Instance, "_"+Key, getattr(self, "_"+Key))
                    if Name:
                        setattr(Instance, "_Name", Name)
                    Instance.Relocate()
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
            self._Display = True
            if self._Resizable and self._Resize_Index<self._Canvas._GUI._Resize_Index:
                self.Resize()
            else:
                self.Display()
            if self._On_Show:
                self._On_Show()
            self.Run()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Show -> {E}")

    def Display(self):
        try:
            self._Canvas._Frame.itemconfigure(self._Widget, state='normal')
            self._Canvas._Frame.tag_raise(self._Widget)
            self._Display = True
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Display -> {E}")
            
    def Animate(self, Hide=False):
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
            T = threading.Thread(target=Worker, daemon=True)
            self._Anim_Thread = T
            T.start()
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
            
    def Set(self, Path):
        try:
            if hasattr(self,'Stop'):
                self.Stop()
            self._Path = Path
            self._Path_Memory = self._Path
            self.Open()
            self.Load()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Set -> {E}")
            
    def Initial(self):
        try:
            if self._Path_Initial:
                if hasattr(self,'Stop'):
                    self.Stop()
                Load_Setup=[self._Array,self._Url,self._Pil,self._Photo]
                self._Array,self._Url,self._Pil,self._Photo=False,False,False,False
                self.Set(self._Path_Initial)
                self._Array,self._Url,self._Pil,self._Photo=Load_Setup
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Initial -> {E}")
            
    def Refresh(self):
        try:
            self.Open()
            self.Load()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Refresh -> {E}")
        
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
                self.Relocate()
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
                self.Relocate()
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
                self.Relocate()
            return [self._Width, self._Height]
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Size -> {E}")
        
    def Open(self):
        try:
            if hasattr(self,'Stop'):
                self.Stop()
            self._Is_Gif=False
            self._Gif_Frames=[]
            self._Gif_Durations=[]
            self._Gif_Loop=1
            self._Gif_Index=0
            if self._Image:
                try:self._Image.close()
                except:pass
            self._Image=False
            if self._Photo and self._Path:
                self._Image=self._Path
                return
            if self._Array and self._Path is not None:
                self._Image=PIL_Image.fromarray(self._Path)
                self._Image_Width,self._Image_Height=self._Image.size
                return
            if self._Pil and self._Path:
                T=self._Path
                if getattr(T,"is_animated",False):
                    self._Is_Gif=True
                    try:self._Gif_Loop=int(getattr(T,"info",{}).get("loop",1))
                    except:self._Gif_Loop=1
                    C=getattr(T,"n_frames",0) or 0
                    I=0
                    while True:
                        try:
                            T.seek(I)
                            F=T.convert("RGBA").copy()
                            D=int(getattr(T,"info",{}).get("duration",100))
                            self._Gif_Frames.append(F)
                            self._Gif_Durations.append(max(1,D))
                            I+=1
                            if C and I>=C:break
                        except EOFError:
                            break
                    if self._Gif_Frames:
                        self._Image=self._Gif_Frames[0]
                        self._Image_Width,self._Image_Height=self._Image.size
                    else:
                        self._Is_Gif=False
                        self._Image=T.copy()
                        self._Image_Width,self._Image_Height=self._Image.size
                else:
                    self._Image=T.copy()
                    self._Image_Width,self._Image_Height=self._Image.size
                return
            Data=None
            if self._Url and self._Path:
                Data=requests_get(self._Path).content
            elif self._Path and os.path.exists(self._Path):
                with open(self._Path,"rb") as F:
                    Data=F.read()
                if not self._Path_Initial:
                    self._Path_Initial=self._Path
            else:
                return
            with PIL_Image.open(BytesIO(Data)) as T:
                if getattr(T,"is_animated",False):
                    self._Is_Gif=True
                    try:self._Gif_Loop=int(T.info.get("loop",1))
                    except:self._Gif_Loop=1
                    C=getattr(T,"n_frames",0) or 0
                    I=0
                    while True:
                        try:
                            T.seek(I)
                            F=T.convert("RGBA").copy()
                            D=int(T.info.get("duration",100))
                            self._Gif_Frames.append(F)
                            self._Gif_Durations.append(max(1,D))
                            I+=1
                            if C and I>=C:break
                        except EOFError:
                            break
                    if self._Gif_Frames:
                        self._Image=self._Gif_Frames[0]
                        self._Image_Width,self._Image_Height=self._Image.size
                    else:
                        self._Is_Gif=False
                        self._Image=T.copy()
                        self._Image_Width,self._Image_Height=self._Image.size
                else:
                    self._Image=T.copy()
                    self._Image_Width,self._Image_Height=self._Image.size
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Open -> {E}")

    def Convert(self):
        try:
            Temp_Image = self._Image.rotate(self._Rotate + self._Angle, PIL_Image.NEAREST, expand=1)
            if self._Transparent:
                Temp_Image = Temp_Image.convert('RGBA')
            else:
                Temp_Image = Temp_Image.convert('HSV')
            W_Tgt = int(max(1, round(self._Width_Current))) if self._Width_Current else Temp_Image.size[0]
            H_Tgt = int(max(1, round(self._Height_Current))) if self._Height_Current else Temp_Image.size[1]
            if W_Tgt > 0 and H_Tgt > 0:
                Temp_Image = Temp_Image.resize((W_Tgt, H_Tgt), PIL_Image.NEAREST)
            W, H = Temp_Image.size
            Skew_X = max(-100.0, min(100.0, float(self._Skew_Horizontal or 0.0)))
            Skew_Y = max(-100.0, min(100.0, float(self._Skew_Vertical or 0.0)))
            Delta_X = min((W - 1) * 0.5, (abs(Skew_X) / 100.0) * (W * 0.5))
            Delta_Y = min((H - 1) * 0.5, (abs(Skew_Y) / 100.0) * (H * 0.5))
            TL_X, TL_Y = 0.0, 0.0
            TR_X, TR_Y = float(W), 0.0
            BR_X, BR_Y = float(W), float(H)
            BL_X, BL_Y = 0.0, float(H)
            if Skew_X > 0:
                TL_X = Delta_X; TR_X = W - Delta_X
            elif Skew_X < 0:
                BL_X = Delta_X; BR_X = W - Delta_X
            if Skew_Y > 0:
                TR_Y = Delta_Y; BR_Y = H - Delta_Y
            elif Skew_Y < 0:
                TL_Y = Delta_Y; BL_Y = H - Delta_Y
            if Delta_X == 0 and Delta_Y == 0:
                self._Width_Old, self._Height_Old = self._Width_Current, self._Height_Current
                return PIL_ImageTk.PhotoImage(Temp_Image)
            Src_Points = [(0.0, 0.0), (float(W), 0.0), (float(W), float(H)), (0.0, float(H))]
            Dst_Points = [(TL_X, TL_Y), (TR_X, TR_Y), (BR_X, BR_Y), (BL_X, BL_Y)]
            A = []; B_Vals = []
            for (X, Y), (U, V) in zip(Dst_Points, Src_Points):
                A.append([X, Y, 1, 0, 0, 0, -U * X, -U * Y]); B_Vals.append(U)
                A.append([0, 0, 0, X, Y, 1, -V * X, -V * Y]); B_Vals.append(V)
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
            self._Width_Old, self._Height_Old = self._Width_Current, self._Height_Current
            return PIL_ImageTk.PhotoImage(Warped_Image)
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Convert -> {E}")
        
    def Load(self):
        try:
            if self._Image:
                Image = self._Image if self._Photo else self.Convert()
                self._Image_Garbage = Image
                self._Canvas._Frame.itemconfig(self._Widget, image=Image)
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Load -> {E}")
        
    def Create(self):
        try:
            self._Canvas._Frame.itemconfig(self._Widget, anchor=self._Anchor)
            self._Canvas._Frame.coords(self._Widget, self._X_Current, self._Y_Current)
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
            
    def Rotate(self, Value=0):
        try:
            self._Angle+=Value
            self.Load()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Rotate -> {E}")

    def Adjustment(self):
        try:
            self._Width_Ratio = self._Canvas._Width_Current / self._Canvas._Width
            self._Height_Ratio = self._Canvas._Height_Current / self._Canvas._Height
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Adjustment -> {E}")
            
    def Relocate(self, Direct=False):
        try:
            if Direct or (self._Resize and self._Resizable):
                self.Adjustment()
                self._X_Current = self._Left * self._Width_Ratio
                self._Y_Current = self._Top * self._Height_Ratio
                self._Width_Current = self._Width * self._Width_Ratio
                self._Height_Current = self._Height * self._Height_Ratio
            else:
                self._X_Current = self._Left
                self._Y_Current = self._Top
                self._Width_Current = self._Width
                self._Height_Current = self._Height
            Angle_Total = (self._Rotate + self._Angle) % 360
            if Angle_Total:
                Angle_Rad = math.radians(Angle_Total if Angle_Total <= 180 else 360 - Angle_Total)
                C = abs(math.cos(Angle_Rad))
                S = abs(math.sin(Angle_Rad))
                New_W = self._Width_Current * C + self._Height_Current * S
                New_H = self._Width_Current * S + self._Height_Current * C
                Dx = (New_W - self._Width_Current) * 0.5
                Dy = (New_H - self._Height_Current) * 0.5
                self._X_Current -= Dx
                self._Y_Current -= Dy
                self._Width_Current = New_W
                self._Height_Current = New_H
            self.Create()
            if self._Display:
                self.Display()
                self.Run()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Relocate -> {E}")
            
    def Resize(self):
        try:
            self._Resize_Index = self._Canvas._GUI._Resize_Index
            self.Relocate()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Resize -> {E}")
            
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