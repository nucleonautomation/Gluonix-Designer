# IMPORT LIBRARIES
import threading, math, time
from .N_Custom import Event_Bind_Canvas
        
class Canvas_Text_Old:
    def __init__(self, Main):
        self._Canvas = Main
        self._Config = ['Name', 'Width', 'Height', 'Left', 'Top', 'Animate_Left', 'Animate_Top', 'Animate_Width', 'Animate_Height', 'Animate_Time', 'Color', 'Size', 'Value', 'Weight', 'Font', 'Resize', 'Anchor', 'Resize_Font', 'Translucent', 'Alpha']
        self._Display = True
        self._Resize_Index = 0
        self._Resize = True
        self._Name = False
        self._Last_Name = False
        self._Resize_Font = True
        self._Type = 'Canvas_Text'
        self._Left, self._Top, self._Width = 0, 0, 0
        self._Value = ''
        self._Color = '#000000'
        self._Size = 20
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
        self._Translucent = False
        self._Alpha = 25
        self._Height = 0
        self._Weight = 'normal'
        self._Font = 'Helvetica'
        self._Anchor = 'nw'
        self._Justify = 'center'
        self._Widget = self._Canvas._Frame.create_text(0, 0, text=self._Value, fill=self._Color, font=(self._Font, self._Size, self._Weight), anchor=self._Anchor, width=self._Width, justify=self._Justify)
        self._Canvas._Widget.append(self)
        self._Resizable = self._Canvas._Resizable
        self._On_Show = False
        self._On_Hide = False
        self._On_Animate = False

    def __str__(self):
        return "Nucleon_Glunoix_Canvas_Text[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Canvas_Text[]"

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
                    Instance.Create()
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
    
    def Set(self, Value):
        try:
            self._Value = Value
            self._Canvas._Frame.itemconfig(self._Widget, text=self._Value)
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Set -> {E}")
    
    def Get(self, Value):
        try:
            return self._Value
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Get -> {E}")
        
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
            Stripple = f'gray{self.Stripple()}' if self._Translucent else ''
            self._Canvas._Frame.itemconfig(self._Widget, text=self._Value, fill=self._Color, font=(self._Font, self._Size_Current, self._Weight), anchor=self._Anchor, width=self._Width_Current, justify=self._Justify, stipple=Stripple)
            self._Canvas._Frame.coords(self._Widget, self._X_Current, self._Y_Current)
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
            if self._Resize and self._Resizable:
                self.Adjustment()
                self._X_Current = self._Left * self._Width_Ratio
                self._Y_Current = self._Top * self._Height_Ratio
                self._Width_Current = self._Width * self._Width_Ratio
            else:
                self._X_Current = self._Left
                self._Y_Current = self._Top
                self._Width_Current = self._Width
            if self._Resize_Font:
                self.Adjustment()
                if self._Width_Ratio < self._Height_Ratio:
                    self._Size_Current = math.floor(self._Size * self._Width_Ratio)
                else:
                    self._Size_Current = math.floor(self._Size * self._Height_Ratio)
            else:
                self._Size_Current = self._Size
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