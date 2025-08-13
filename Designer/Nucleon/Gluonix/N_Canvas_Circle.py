# IMPORT LIBRARIES
import threading, math, time
from .N_Custom import Event_Bind_Canvas
        
class Canvas_Circle:
    def __init__(self, Main):
        self._Canvas = Main
        self._Config = ['Name', 'Outline', 'Fill', 'Left', 'Top', 'Animate_Left', 'Animate_Top', 'Animate_Radius', 'Animate_Time', 'Radius', 'Thickness', 'Resize']
        self._Display = True
        self._Resize_Index = 0
        self._Resize = True
        self._Name = False
        self._Last_Name = False
        self._Type = 'Canvas_Circle'
        self._Outline = '#000000'
        self._Fill = '#000000'
        self._Thickness = 1
        self._Animating = False
        self._Anim_Stop = threading.Event()
        self._Anim_Thread = None
        self._Animate_Ease = lambda t: (1 - (1 - t)**3)
        self._Animate_Speed = None
        self._Animate_Left = 0
        self._Animate_Top = 0
        self._Animate_Radius = 0
        self._Animate_Time = 1.0
        self._Left, self._Top, self._Radius = 0, 0, 0
        self._X1 = abs(self._Left - self._Radius)
        self._Y1 = abs(self._Top - self._Radius)
        self._X2 = abs(self._Left + self._Radius)
        self._Y2 = abs(self._Top + self._Radius)
        self._Widget = self._Canvas._Frame.create_oval(self._X1, self._Y1, self._X2, self._Y2, outline=self._Outline, width=self._Thickness, fill=self._Fill)
        self._Canvas._Widget.append(self)
        self._Resizable = self._Canvas._Resizable
        self._On_Show = False
        self._On_Hide = False
        self._On_Animate = False

    def __str__(self):
        return "Nucleon_Glunoix_Canvas_Circle[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Canvas_Circle[]"

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
            
    def Animate(self, Hide=False):
        try:
            self.Animate_Cancel()
            Final_Left = float(self._Left)
            Final_Top = float(self._Top)
            Final_Radius = float(self._Radius)
            Start_Left = float(self._Animate_Left)
            Start_Top = float(self._Animate_Top)
            Animate_Radius = float(getattr(self, "_Animate_Radius", 0))
            Size_Anim = Animate_Radius != 0
            Start_Radius = Animate_Radius if Size_Anim else Final_Radius
            Same_Pos = int(round(Start_Left)) == int(round(Final_Left)) and int(round(Start_Top)) == int(round(Final_Top))
            Same_Size = int(round(Start_Radius)) == int(round(Final_Radius))
            if Same_Pos and (not Size_Anim or Same_Size):
                self.Config(Left=int(round(Final_Left)), Top=int(round(Final_Top)), Radius=int(round(Final_Radius)))
                self.Show()
                return
            def Show_Start():
                if not self._Canvas._Frame.winfo_exists():
                    return
                self.Config(Left=int(round(Start_Left)), Top=int(round(Start_Top)), Radius=int(round(Start_Radius)))
            self._Canvas._Frame.after(0, Show_Start)
            Dx = Final_Left - Start_Left
            Dy = Final_Top - Start_Top
            Dr = Final_Radius - Start_Radius if Size_Anim else 0.0
            Dist = math.hypot(math.hypot(Dx, Dy), Dr)
            if Dist == 0.0:
                def Snap_Same():
                    if not self._Canvas._Frame.winfo_exists():
                        return
                    self.Config(Left=int(round(Final_Left)), Top=int(round(Final_Top)), Radius=int(round(Final_Radius)))
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
                            self.Config(Left=int(round(Final_Left)), Top=int(round(Final_Top)), Radius=int(round(Final_Radius)))
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
                    R = Start_Radius + Dr * K
                    Cur = (int(round(X)), int(round(Y)), int(round(R)))
                    if Cur != Last:
                        Last = Cur
                        def Post(C=Cur):
                            if not self._Canvas._Frame.winfo_exists():
                                return
                            if self._Animating:
                                self.Config(Left=C[0], Top=C[1], Radius=C[2])
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
            
    def Radius(self, Value=False):
        try:
            if Radius:
                self._Radius = Radius
                self.Relocate()
            return self._Radius
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Size -> {E}")
        
    def Create(self):
        try:
            self._Canvas._Frame.itemconfig(self._Widget, outline=self._Outline, width=self._Thickness, fill=self._Fill)
            self._Canvas._Frame.coords(self._Widget, self._X1, self._Y1, self._X2, self._Y2)
            if self._Name!=self._Last_Name:
                if self._Last_Name:
                    if self._Last_Name in self._Canvas.__dict__:
                        del self._Canvas.__dict__[self._Last_Name]
                if self._Name:
                    self._Canvas.__dict__[self._Name] = self
                self._Last_Name = self._Name
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Create -> {E}")

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
                Left  = self._Left * self._Width_Ratio
                Top   = self._Top  * self._Height_Ratio
                Ratio = min(self._Width_Ratio, self._Height_Ratio)
                Radius = self._Radius * Ratio
                self._X1 = Left - Radius
                self._Y1 = Top  - Radius
                self._X2 = Left + Radius
                self._Y2 = Top  + Radius
            else:
                self._X1 = self._Left - self._Radius
                self._Y1 = self._Top  - self._Radius
                self._X2 = self._Left + self._Radius
                self._Y2 = self._Top  + self._Radius
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