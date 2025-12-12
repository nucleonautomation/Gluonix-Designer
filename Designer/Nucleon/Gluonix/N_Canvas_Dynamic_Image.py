import os
import threading, math, time
from io import BytesIO
import urllib
from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk
from .N_Canvas_Image import Canvas_Image
from .N_Custom import Event_Bind_Canvas

class Canvas_Dynamic_Image(Canvas_Image):
    
    def __init__(self, Main):
        super().__init__(Main)
        self._Type = "Canvas_Dynamic_Image"
        self._Zoom_Scale = 1.0
        self._Zoom_Center = None
        self._Drag_Last_X = 0
        self._Drag_Last_Y = 0
        self._Image_Width = 0
        self._Image_Height = 0
        self._Hover_Active = False
        self._Canvas.Bind_Item(self._Widget, On_Click=self.Drag_Start)
        self._Canvas.Bind_Item(self._Widget, On_Drag=self.Drag)
        self._Canvas.Bind_Item(self._Widget, On_Right_Click=self.Reset)
        self._Canvas.Bind_Item(self._Widget, On_Hover_In=lambda E: self.Hover(True))
        self._Canvas.Bind_Item(self._Widget, On_Hover_Out=lambda E: self.Hover(False))
        self._Canvas.Bind(On_Mouse_Wheel=self.Zoom)

    def __str__(self):
        return "Nucleon_Glunoix_Canvas_Dynamic_Image[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Canvas_Dynamic_Image[]"
            
    def Clear(self):
        try:
            super().Clear()
            self._Zoom_Scale = 1.0
            self._Zoom_Center = None
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Clear -> {E}")

    def Open(self):
        try:
            super().Open()
            if self._Image:
                if not hasattr(self, "_Image_Width") or not hasattr(self, "_Image_Height") or not self._Image_Width or not self._Image_Height:
                    try:
                        self._Image_Width, self._Image_Height = self._Image.size
                    except Exception:
                        self._Image_Width, self._Image_Height = 0, 0
                if self._Image_Width and self._Image_Height:
                    if self._Zoom_Center is None:
                        self._Zoom_Center = (self._Image_Width // 2, self._Image_Height // 2)
                    CX, CY = self._Zoom_Center
                    CX = max(0, min(CX, self._Image_Width))
                    CY = max(0, min(CY, self._Image_Height))
                    self._Zoom_Center = (CX, CY)
                if not hasattr(self, "_Zoom_Scale") or self._Zoom_Scale < 1.0:
                    self._Zoom_Scale = 1.0
            else:
                self._Zoom_Scale = 1.0
                self._Zoom_Center = None
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Open -> {E}")

    def Convert(self):
        try:
            if not self._Image:
                return False
            if self._Resize and self._Canvas._Type!='Scroll':
                Left, Right, Width, Height = self._Canvas.Box()
                Width_Ratio = Width/self._Canvas._Width if getattr(self._Canvas, "_Width", 0) else 1
                Height_Ratio = Height/self._Canvas._Height if getattr(self._Canvas, "_Height", 0) else 1
            else:
                Width_Ratio = 1
                Height_Ratio = 1
            Frame_Width = int(max(1, round(self._Width*Width_Ratio)))
            Frame_Height = int(max(1, round(self._Height*Height_Ratio)))
            if Frame_Width<=0 or Frame_Height<=0:
                return False
            if not getattr(self, "_Image_Width", 0) or not getattr(self, "_Image_Height", 0):
                try:
                    self._Image_Width, self._Image_Height = self._Image.size
                except Exception:
                    return False
            if not self._Zoom_Center:
                self._Zoom_Center = (self._Image_Width/2.0, self._Image_Height/2.0)
            Zoom_Width = self._Image_Width/self._Zoom_Scale
            Zoom_Height = self._Image_Height/self._Zoom_Scale
            Zoom_Width = max(1.0, min(Zoom_Width, float(self._Image_Width)))
            Zoom_Height = max(1.0, min(Zoom_Height, float(self._Image_Height)))
            CX, CY = self._Zoom_Center
            CX = max(Zoom_Width/2.0, min(self._Image_Width - Zoom_Width/2.0, CX))
            CY = max(Zoom_Height/2.0, min(self._Image_Height - Zoom_Height/2.0, CY))
            self._Zoom_Center = (CX, CY)
            Left_C = CX - Zoom_Width/2.0
            Top_C = CY - Zoom_Height/2.0
            Right_C = Left_C + Zoom_Width
            Bottom_C = Top_C + Zoom_Height
            Base_Image = self._Image
            Crop = Base_Image.crop((int(Left_C), int(Top_C), int(Right_C), int(Bottom_C)))
            Angle = getattr(self, "_Rotate", 0) + getattr(self, "_Angle", 0)
            if Angle:
                Crop = Crop.rotate(Angle, PIL_Image.NEAREST, expand=1)
            if self._Transparent:
                Crop = Crop.convert("RGBA")
                Mode = "RGBA"
                Background = (0, 0, 0, 0)
            else:
                Mode = Crop.mode if Crop.mode in ["RGB", "L"] else "RGB"
                Crop = Crop.convert(Mode)
                Background = 0 if Mode=="L" else (0, 0, 0)
            Image_Width, Image_Height = Crop.size
            if Image_Width<=0 or Image_Height<=0:
                return False
            Aspect_Ratio = getattr(self, "_Aspect_Ratio", True)
            Image_Aspect = Image_Width/Image_Height
            Frame_Aspect = Frame_Width/Frame_Height
            Use_Cover = Aspect_Ratio and self._Zoom_Scale>1.0001
            if not Aspect_Ratio:
                New_Width = Frame_Width
                New_Height = Frame_Height
                Crop = Crop.resize((New_Width, New_Height), PIL_Image.NEAREST)
                Frame_Image = Crop
            else:
                if Use_Cover:
                    if Image_Aspect>Frame_Aspect:
                        New_Height = Frame_Height
                        New_Width = int(max(1, round(Frame_Height*Image_Aspect)))
                    else:
                        New_Width = Frame_Width
                        New_Height = int(max(1, round(Frame_Width/Image_Aspect)))
                    if New_Width<=0 or New_Height<=0:
                        return False
                    Crop = Crop.resize((New_Width, New_Height), PIL_Image.NEAREST)
                    Offset_X = max(0, (New_Width - Frame_Width)//2)
                    Offset_Y = max(0, (New_Height - Frame_Height)//2)
                    Crop = Crop.crop((Offset_X, Offset_Y, Offset_X+Frame_Width, Offset_Y+Frame_Height))
                    Frame_Image = Crop
                else:
                    if Image_Aspect>Frame_Aspect:
                        New_Width = Frame_Width
                        New_Height = int(max(1, round(Frame_Width/Image_Aspect)))
                    else:
                        New_Height = Frame_Height
                        New_Width = int(max(1, round(Frame_Height*Image_Aspect)))
                    if New_Width<=0 or New_Height<=0:
                        return False
                    Crop = Crop.resize((New_Width, New_Height), PIL_Image.NEAREST)
                    Frame_Image = PIL_Image.new(Mode, (Frame_Width, Frame_Height), Background)
                    Offset_X = (Frame_Width - New_Width)//2
                    Offset_Y = (Frame_Height - New_Height)//2
                    if Mode=="RGBA":
                        Alpha = Crop.split()[3] if Crop.mode=="RGBA" else None
                        Frame_Image.paste(Crop, (Offset_X, Offset_Y), Alpha)
                    else:
                        Frame_Image.paste(Crop, (Offset_X, Offset_Y))
            W = Frame_Image.size[0]
            H = Frame_Image.size[1]
            Skew_X = max(-100.0, min(100.0, float(getattr(self, "_Skew_Horizontal", 0.0) or 0.0)))
            Skew_Y = max(-100.0, min(100.0, float(getattr(self, "_Skew_Vertical", 0.0) or 0.0)))
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
                return PIL_ImageTk.PhotoImage(Frame_Image)
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
                Warped_Image = Frame_Image.transform((W, H), PIL_Image.PERSPECTIVE, Coeffs, resample=PIL_Image.BICUBIC, fillcolor=(0, 0, 0, 0) if self._Transparent and Mode=="RGBA" else None)
            except TypeError:
                Background_Image = PIL_Image.new(Mode, (W, H), Background)
                Warped_Image = Frame_Image.transform((W, H), PIL_Image.PERSPECTIVE, Coeffs, resample=PIL_Image.BICUBIC)
                if self._Transparent and Warped_Image.mode != "RGBA":
                    Warped_Image = Warped_Image.convert("RGBA")
                if Mode=="RGBA":
                    Background_Image.paste(Warped_Image, (0, 0), Warped_Image.split()[3])
                else:
                    Background_Image.paste(Warped_Image, (0, 0))
                Warped_Image = Background_Image
            return PIL_ImageTk.PhotoImage(Warped_Image)
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Convert -> {E}")
            return False

    def Load(self):
        try:
            if not self._Image:
                return
            if getattr(self, "_Photo", False):
                Image = self._Image
            else:
                Image = self.Convert()
            if not Image:
                return
            self._Canvas._Frame.itemconfig(self._Widget, image=Image)
            self._TK_Image = Image
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Load -> {E}")
                
    def Drag_Start(self, Event):
        try:
            self._Drag_Last_X = self._Canvas._Frame.canvasx(Event.x)
            self._Drag_Last_Y = self._Canvas._Frame.canvasy(Event.y)
        except Exception:
            self._Drag_Last_X, self._Drag_Last_Y = 0, 0

    def Drag(self, Event):
        try:
            if not self._Image or not self._Zoom_Center:
                return
            Curr_X = self._Canvas._Frame.canvasx(Event.x)
            Curr_Y = self._Canvas._Frame.canvasy(Event.y)
            Delta_X = Curr_X - self._Drag_Last_X
            Delta_Y = Curr_Y - self._Drag_Last_Y
            self._Drag_Last_X = Curr_X
            self._Drag_Last_Y = Curr_Y
            View_Width = self._Image_Width/self._Zoom_Scale
            View_Height = self._Image_Height/self._Zoom_Scale
            Box = self._Canvas._Frame.bbox(self._Widget)
            if not Box:
                return
            X1, Y1, X2, Y2 = Box
            Inner_Width = max(1, X2 - X1)
            Inner_Height = max(1, Y2 - Y1)
            Move_X_Image = -Delta_X*(View_Width/Inner_Width)
            Move_Y_Image = -Delta_Y*(View_Height/Inner_Height)
            New_Center_X = self._Zoom_Center[0] + Move_X_Image
            New_Center_Y = self._Zoom_Center[1] + Move_Y_Image
            Half_Width = View_Width/2.0
            Half_Height = View_Height/2.0
            New_Center_X = max(Half_Width, min(self._Image_Width - Half_Width, New_Center_X))
            New_Center_Y = max(Half_Height, min(self._Image_Height - Half_Height, New_Center_Y))
            self._Zoom_Center = (New_Center_X, New_Center_Y)
            self.Load()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Drag -> {E}")

    def Hover(self, Value):
        try:
            self._Hover_Active = Value
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Hover -> {E}")

    def Zoom(self, Event):
        try:
            if not self._Hover_Active:
                return
            if not self._Image:
                return
            Zoom_Factor = 1.1 if getattr(Event, "delta", 0)>0 else 0.9
            New_Zoom_Scale = self._Zoom_Scale*Zoom_Factor
            New_Zoom_Scale = max(1.0, New_Zoom_Scale)
            if New_Zoom_Scale == self._Zoom_Scale:
                return
            Canvas_X = self._Canvas._Frame.canvasx(Event.x)
            Canvas_Y = self._Canvas._Frame.canvasy(Event.y)
            Box = self._Canvas._Frame.bbox(self._Widget)
            if not Box:
                return
            X1, Y1, X2, Y2 = Box
            Inner_Width = max(1, X2 - X1)
            Inner_Height = max(1, Y2 - Y1)
            Mouse_Rel_X = (Canvas_X - X1)/Inner_Width
            Mouse_Rel_Y = (Canvas_Y - Y1)/Inner_Height
            View_Width = self._Image_Width/self._Zoom_Scale
            View_Height = self._Image_Height/self._Zoom_Scale
            View_Left = self._Zoom_Center[0] - View_Width/2.0
            View_Top = self._Zoom_Center[1] - View_Height/2.0
            Mouse_Abs_X = View_Left + Mouse_Rel_X*View_Width
            Mouse_Abs_Y = View_Top + Mouse_Rel_Y*View_Height
            New_View_Width = self._Image_Width/New_Zoom_Scale
            New_View_Height = self._Image_Height/New_Zoom_Scale
            New_View_Left = Mouse_Abs_X - Mouse_Rel_X*New_View_Width
            New_View_Top = Mouse_Abs_Y - Mouse_Rel_Y*New_View_Height
            New_Center_X = New_View_Left + New_View_Width/2.0
            New_Center_Y = New_View_Top + New_View_Height/2.0
            Half_Width = New_View_Width/2.0
            Half_Height = New_View_Height/2.0
            New_Center_X = max(Half_Width, min(self._Image_Width - Half_Width, New_Center_X))
            New_Center_Y = max(Half_Height, min(self._Image_Height - Half_Height, New_Center_Y))
            self._Zoom_Scale = New_Zoom_Scale
            self._Zoom_Center = (New_Center_X, New_Center_Y)
            self.Load()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Zoom -> {E}")

    def Reset(self, Event=False):
        try:
            self._Angle = 0
            self._Zoom_Scale = 1.0
            if self._Image and getattr(self, "_Image_Width", 0) and getattr(self, "_Image_Height", 0):
                self._Zoom_Center = (self._Image_Width//2, self._Image_Height//2)
            self.Load()
        except Exception as E:
            self._Canvas._GUI.Error(f"{self._Type} -> Reset -> {E}")
