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
        self._Config = ['Name', 'Width', 'Height', 'Left', 'Top', 'Animate_Left', 'Animate_Top', 'Animate_Width', 'Animate_Height', 'Animate_Time', 'Anchor', 'Url', 'Array', 'Pil', 'Photo', 'Resize', 'Rotate', 'Path', 'Path_Initial', 'Transparent']
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
        self._Width, self._Height, self._Width_Old, self._Height_Old, self._Left, self._Top = 0, 0, 0, 0, 0, 0
        self._Widget = self._Canvas._Frame.create_image(0, 0, anchor=self._Anchor, image=None)
        self._Canvas._Widget.append(self)
        self._Resizable = self._Canvas._Resizable
        self._On_Show = False
        self._On_Hide = False

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

    def Hide(self):
        try:
            self.Animate_Cancel()
            self._Canvas._Frame.itemconfigure(self._Widget, state='hidden')
            self._Display = False
            if self._On_Hide:
                self._On_Hide()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type}-> Hide -> {E}")
            
    def Show(self):
        try:
            self._Display = True
            if self._Resizable and self._Resize_Index<self._Canvas._GUI._Resize_Index:
                self.Resize()
            else:
                self.Display()
            if self._On_Show:
                self._On_Show()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Show -> {E}")

    def Display(self):
        try:
            self._Canvas._Frame.itemconfigure(self._Widget, state='normal')
            self._Canvas._Frame.tag_raise(self._Widget)
            self._Display = True
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Display -> {E}")
            
    def Animate(self):
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

    def Delete(self):
        try:
            self.Animate_Cancel()
            self._Canvas._Widget.remove(self)
            self._Canvas._Frame.delete(self._Widget)
            if self:
                del self
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Delete -> {E}")
        
    def Set(self, Path):
        try:
            self._Path = Path
            self._Path_Memory = self._Path
            self.Open()
            self.Load()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Set -> {E}")
            
    def Initial(self):
        try:
            if self._Path_Initial:
                Load_Setup = [self._Array, self._Url, self._Pil, self._Photo]
                self._Array, self._Url, self._Pil, self._Photo = False, False, False, False
                self.Set(self._Path_Initial)
                self._Array, self._Url, self._Pil, self._Photo = Load_Setup
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
            if Left is not None or Top is not None:
                self.Position(Left=Left, Top=Top)
            return True
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Move -> {E}")
        
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
            if self._Image:
                self._Image.close()
            if self._Url:
                if self._Path:
                    Image_Data = requests_get(self._Path)
                    self._Image = PIL_Image.open(BytesIO(Image_Data.content))
            elif self._Array:
                if self._Path is not None:
                    self._Image = PIL_Image.fromarray(self._Path)
            elif self._Pil:
                if self._Path:
                    self._Image = self._Path.copy()
            elif self._Photo:
                if self._Path:
                    self._Image = self._Path
            else:
                if self._Path and os.path.exists(self._Path):
                    self._Image = PIL_Image.open(self._Path)
                    if not self._Path_Initial:
                        self._Path_Initial = self._Path
            if self._Image and not self._Photo:
                self._Image_Width, self._Image_Height = self._Image.size
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Open -> {E}")
        
    def Convert(self):
        try:
            Temp_Image = self._Image.rotate(self._Rotate+self._Angle, PIL_Image.NEAREST, expand=0)
            if self._Transparent:
                Temp_Image_Convert = Temp_Image.convert('RGBA')
            else:
                Temp_Image_Convert = Temp_Image.convert("HSV")
            Width, Height = Temp_Image.size
            if self._Width_Current>0 and self._Height_Current>0:
                Temp_Image = Temp_Image.resize((int(self._Width_Current), int(self._Height_Current)), PIL_Image.NEAREST)
            elif self._Width_Current and self._Height_Current<1:
                Ratio = Height/Width
                Temp_Image = Temp_Image.resize((int(self._Width_Current), int(self._Width_Current*Ratio)), PIL_Image.NEAREST)
            elif self._Width_Current<1 and self._Height_Current:
                Ratio = Width/Height
                Temp_Image = Temp_Image.resize((int(self._Height_Current*Ratio), int(self._Height_Current)), PIL_Image.NEAREST)
            else:
                Temp_Image = Temp_Image.copy()
            self._Width_Old, self._Height_Old = self._Width_Current, self._Height_Current
            Temp_Image_TK = PIL_ImageTk.PhotoImage(Temp_Image)
            return Temp_Image_TK
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
            self.Create()
            if self._Display:
                self.Display()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Relocate -> {E}")
            
    def Resize(self):
        try:
            self._Resize_Index = self._Canvas._GUI._Resize_Index
            self.Relocate()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Resize -> {E}")
            