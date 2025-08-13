# IMPORT LIBRARIES
import threading, math, time
from .N_Custom import Event_Bind_Canvas
        
class Canvas_RectangleR:
    def __init__(self, Main):
        self._Canvas = Main
        self._Config = ['Name', 'Outline', 'Fill', 'Width', 'Height', 'Left', 'Top', 'Animate_Left', 'Animate_Top', 'Animate_Width', 'Animate_Height', 'Animate_Time', 'Angle', 'Radius', 'Thickness', 'Resize', 'Translucent', 'Alpha', 'Skew_Horizontal', 'Skew_Vertical']
        self._Display = True
        self._Resize_Index = 0
        self._Resize = True
        self._Name = False
        self._Last_Name = False
        self._Type = 'Canvas_RectangleR'
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
        self._Animate_Width = 0
        self._Animate_Height = 0
        self._Animate_Time = 1.0
        self._Angle = 0
        self._Radius = 0
        self._Translucent = False
        self._Alpha = 25
        self._Skew_Horizontal = 0
        self._Skew_Vertical = 0
        self._Width, self._Height, self._Left, self._Top = 1, 1, 1, 1
        self._Width_Current, self._Height_Current, self._Left_Current, self._Top_Current = 1, 1, 1, 1
        self._Widget = self._Canvas._Frame.create_polygon([0, 0, 0, 0], outline=self._Outline, width=self._Thickness, fill=self._Fill, smooth=True)
        self._Canvas._Widget.append(self)
        self._Resizable = self._Canvas._Resizable
        self._On_Show = False
        self._On_Hide = False
        self._On_Animate = False

    def __str__(self):
        return "Nucleon_Glunoix_Canvas_RectangleR[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Canvas_RectangleR[]"

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
            return self.Position(Left=Left, Top=Top)
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
        
    def Angle(self, Value=None):
        try:
            if Value is not None:
                self._Angle = Value
                self.Relocate()
            return self._Angle
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Angle -> {E}")
        
    def Rotate(self, Value=None):
        try:
            if Value is not None:
                self._Angle += Value
                self.Relocate()
            return self._Angle
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Rotate -> {E}")
            
    def Rotation(self, X, Y, CX, CY, Angle_Rad, Translate=(0, 0)):
        try:
            X -= CX
            Y -= CY
            RX = X * math.cos(Angle_Rad) - Y * math.sin(Angle_Rad)
            RY = X * math.sin(Angle_Rad) + Y * math.cos(Angle_Rad)
            return RX + Translate[0], RY + Translate[1]
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Rotation -> {E}")
            return X, Y
            
    def Arc(self, CX, CY, Start_Angle_Deg, Steps, Radius):
        try:
            return [
                (
                    CX + Radius * math.cos(math.radians(Start_Angle_Deg + i * 90 / Steps)),
                    CY + Radius * math.sin(math.radians(Start_Angle_Deg + i * 90 / Steps))
                )
                for i in range(Steps + 1)
            ]
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Arc -> {E}")
            
    def Rectangle(self):
        try:
            Width = self._Width_Current
            Height = self._Height_Current
            Radius = min(self._Radius, Width / 2, Height / 2)
            Angle_Rad = math.radians(self._Angle)
            Steps = 5
            HW, HH = Width / 2, Height / 2
            Rect_Points = []
            Rect_Points += self.Arc(-HW + Radius, -HH + Radius, 180, Steps, Radius)
            Rect_Points.append((HW - Radius, -HH))
            Rect_Points += self.Arc(HW - Radius, -HH + Radius, 270, Steps, Radius)
            Rect_Points.append((HW, HH - Radius))
            Rect_Points += self.Arc(HW - Radius, HH - Radius, 0, Steps, Radius)
            Rect_Points.append((-HW + Radius, HH))
            Rect_Points += self.Arc(-HW + Radius, HH - Radius, 90, Steps, Radius)
            Rect_Points.append((-HW, -HH + Radius))
            Skew_X = max(-100.0, min(100.0, float(self._Skew_Horizontal or 0.0)))
            Skew_Y = max(-100.0, min(100.0, float(self._Skew_Vertical or 0.0)))
            Delta_X = min((Width - 1) * 0.5, (abs(Skew_X) / 100.0) * (Width * 0.5))
            Delta_Y = min((Height - 1) * 0.5, (abs(Skew_Y) / 100.0) * (Height * 0.5))
            TL_X, TL_Y = 0.0, 0.0
            TR_X, TR_Y = float(Width), 0.0
            BR_X, BR_Y = float(Width), float(Height)
            BL_X, BL_Y = 0.0, float(Height)
            if Skew_X > 0:
                TL_X = Delta_X
                TR_X = Width - Delta_X
            elif Skew_X < 0:
                BL_X = Delta_X
                BR_X = Width - Delta_X
            if Skew_Y > 0:
                TR_Y = Delta_Y
                BR_Y = Height - Delta_Y
            elif Skew_Y < 0:
                TL_Y = Delta_Y
                BL_Y = Height - Delta_Y
            Src = [(0.0, 0.0), (float(Width), 0.0), (float(Width), float(Height)), (0.0, float(Height))]
            Dst = [(TL_X, TL_Y), (TR_X, TR_Y), (BR_X, BR_Y), (BL_X, BL_Y)]
            A = []
            B_Vals = []
            for (X, Y), (U, V) in zip(Src, Dst):
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
            a, b, c, d, e, f, g, h = Coeffs
            Skewed_Points = []
            for (X, Y) in Rect_Points:
                SX = X + HW
                SY = Y + HH
                Den = g * SX + h * SY + 1.0
                NX = (a * SX + b * SY + c) / Den
                NY = (d * SX + e * SY + f) / Den
                Skewed_Points.append((NX - HW, NY - HH))
            C_X, C_Y = self._Left_Current, self._Top_Current
            Final_Points = [self.Rotation(X, Y, 0, 0, Angle_Rad, Translate=(C_X, C_Y)) for (X, Y) in Skewed_Points]
            Flat_Points = [Coord for Point in Final_Points for Coord in Point]
            Stripple = f'gray{self.Stripple()}' if self._Translucent else ''
            self._Canvas._Frame.itemconfig(self._Widget, outline=self._Outline, width=self._Thickness, fill=self._Fill, stipple=Stripple, smooth=True)
            self._Canvas._Frame.coords(self._Widget, Flat_Points)
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Rectangle -> {E}")

    def Stripple(self):
        try:
            if 0 <= self._Alpha <= 12:
                return 12
            elif 13 <= self._Alpha <= 25:
                return 25
            elif 26 <= self._Alpha <= 50:
                return 50
            elif 51 <= self._Alpha <= 75:
                return 75
            else:
                return 100
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Stripple -> {E}")
            
    def Create(self):
        try:
            self.Rectangle()
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
                self._Left_Current = self._Left * self._Width_Ratio
                self._Width_Current = self._Width * self._Width_Ratio
                self._Top_Current = self._Top * self._Height_Ratio
                self._Height_Current = self._Height * self._Height_Ratio
            else:
                self._Left_Current = self._Left
                self._Width_Current = self._Width
                self._Top_Current = self._Top
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
