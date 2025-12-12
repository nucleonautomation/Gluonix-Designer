# IMPORT LIBRARIES
from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk
from .N_Image import Image
from .N_Custom import Event_Bind

PIL_Image.MAX_IMAGE_PIXELS = None
            
class Dynamic_Image(Image):
    
    def __init__(self, Main, *args, **kwargs):
        super().__init__(Main, *args, **kwargs)
        self._Type = "Dynamic_Image"
        self._Zoom_Scale = 1.0
        self._Zoom_Center = None
        self._Drag_Last_X = 0
        self._Drag_Last_Y = 0
        Event_Bind(self._Widget, On_Click=lambda E: self.Drag_Start(E), On_Drag=lambda E: self.Drag(E), On_Mouse_Wheel=lambda E: self.Zoom(E), On_Right_Click=lambda E: self.Reset(E))

    def __str__(self):
        return "Nucleon_Glunoix_Dynamic_Image[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Dynamic_Image[]"
    
    def Clear(self):
        try:
            super().Clear()
            self._Zoom_Scale = 1.0
            self._Zoom_Center = None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Clear -> {E}")

    def Initial(self):
        try:
            if self._Path_Initial:
                if hasattr(self, 'Stop'):
                    self.Stop()
                self.Set(self._Path_Initial)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Initial -> {E}")
    
    def Refresh(self):
        try:
            self.Open()
            self.Load()
            if self._Display and not self._Animating:
                self.Show()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Refresh -> {E}")
    
    def Open(self):
        try:
            super().Open()
            if self._Image:
                self._Image_Width, self._Image_Height = self._Image.size
                if self._Zoom_Center is None:
                    self._Zoom_Center = (self._Image_Width // 2, self._Image_Height // 2)
                CX, CY = self._Zoom_Center
                CX = max(0, min(CX, self._Image_Width))
                CY = max(0, min(CY, self._Image_Height))
                self._Zoom_Center = (CX, CY)
                if not hasattr(self, "_Zoom_Scale"):
                    self._Zoom_Scale = 1.0
            else:
                self.Clear()
        except Exception as E:
            self.Clear()
            self._GUI.Error(f"{self._Type} -> Open -> {E}")
    
    def Convert(self, Frame_Width, Frame_Height):
        try:
            if not self._Image or Frame_Width<=0 or Frame_Height<=0:
                return False
            if self._Zoom_Center is None:
                self._Zoom_Center = (self._Image_Width // 2, self._Image_Height // 2)
            Zoom_W = self._Image_Width / self._Zoom_Scale
            Zoom_H = self._Image_Height / self._Zoom_Scale
            CX, CY = self._Zoom_Center
            CX = max(Zoom_W / 2, min(self._Image_Width - Zoom_W / 2, CX))
            CY = max(Zoom_H / 2, min(self._Image_Height - Zoom_H / 2, CY))
            self._Zoom_Center = (CX, CY)
            Left = CX - Zoom_W / 2
            Top = CY - Zoom_H / 2
            Right = Left + Zoom_W
            Bottom = Top + Zoom_H
            Crop = self._Image.crop((int(Left), int(Top), int(Right), int(Bottom)))
            Angle = getattr(self, "_Rotate", 0) + getattr(self, "_Angle", 0)
            if Angle:
                Crop = Crop.rotate(Angle, PIL_Image.NEAREST, expand=0)
            if self._Transparent:
                Crop = Crop.convert("RGBA")
            Image_Width, Image_Height = Crop.size
            if Image_Width<=0 or Image_Height<=0:
                return False
            Inner_W = max(1, int(Frame_Width))
            Inner_H = max(1, int(Frame_Height))
            Aspect_Ratio = getattr(self, "_Aspect_Ratio", True)
            Image_Aspect = Image_Width / Image_Height
            Frame_Aspect = Inner_W / Inner_H
            if not Aspect_Ratio:
                New_Width = Inner_W
                New_Height = Inner_H
                Crop = Crop.resize((New_Width, New_Height), PIL_Image.NEAREST)
                Left_Off = 0
                Top_Off = 0
            else:
                Use_Cover = self._Zoom_Scale>1.0001
                if Use_Cover:
                    if Image_Aspect>Frame_Aspect:
                        New_Height = Inner_H
                        New_Width = int(max(1, round(Inner_H*Image_Aspect)))
                    else:
                        New_Width = Inner_W
                        New_Height = int(max(1, round(Inner_W/Image_Aspect)))
                    if New_Width<=0 or New_Height<=0:
                        return False
                    Crop = Crop.resize((New_Width, New_Height), PIL_Image.NEAREST)
                    Left_Off = max(0, (New_Width - Inner_W)//2)
                    Top_Off = max(0, (New_Height - Inner_H)//2)
                    Crop = Crop.crop((Left_Off, Top_Off, Left_Off+Inner_W, Top_Off+Inner_H))
                    Left_Off = 0
                    Top_Off = 0
                else:
                    if Image_Aspect>Frame_Aspect:
                        New_Width = Inner_W
                        New_Height = int(max(1, round(Inner_W/Image_Aspect)))
                    else:
                        New_Height = Inner_H
                        New_Width = int(max(1, round(Inner_H*Image_Aspect)))
                    if New_Width<=0 or New_Height<=0:
                        return False
                    Crop = Crop.resize((New_Width, New_Height), PIL_Image.NEAREST)
                    Left_Off = (Inner_W - New_Width) // 2
                    Top_Off = (Inner_H - New_Height) // 2
            Crop_TK = PIL_ImageTk.PhotoImage(Crop)
            return {"Image": Crop_TK, "Top": Top_Off, "Left": Left_Off}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Convert -> {E}")
            return False

    def Drag_Start(self, Event):
        try:
            self._Drag_Last_X = Event.x
            self._Drag_Last_Y = Event.y
        except Exception:
            self._Drag_Last_X, self._Drag_Last_Y = 0, 0
    
    def Drag(self, Event):
        try:
            if not self._Image:
                return
            Curr_X = Event.x
            Curr_Y = Event.y
            Delta_X = Curr_X - self._Drag_Last_X
            Delta_Y = Curr_Y - self._Drag_Last_Y
            self._Drag_Last_X = Curr_X
            self._Drag_Last_Y = Curr_Y
            View_W = self._Image_Width / self._Zoom_Scale
            View_H = self._Image_Height / self._Zoom_Scale
            Inner_W = max(1, self._Width - 2 * self._Border_Size)
            Inner_H = max(1, self._Height - 2 * self._Border_Size)
            Move_X_Img = -Delta_X * (View_W / Inner_W)
            Move_Y_Img = -Delta_Y * (View_H / Inner_H)
            New_CX = self._Zoom_Center[0] + Move_X_Img
            New_CY = self._Zoom_Center[1] + Move_Y_Img
            Half_W = View_W / 2
            Half_H = View_H / 2
            New_CX = max(Half_W, min(self._Image_Width - Half_W, New_CX))
            New_CY = max(Half_H, min(self._Image_Height - Half_H, New_CY))
            self._Zoom_Center = (New_CX, New_CY)
            self.Load()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Drag -> {E}")
    
    def Zoom(self, Event):
        try:
            if not self._Image:
                return
            Zoom_Factor = 1.1 if Event.delta > 0 else 0.9
            New_Zoom_Scale = self._Zoom_Scale * Zoom_Factor
            New_Zoom_Scale = max(1.0, New_Zoom_Scale)
            if New_Zoom_Scale == self._Zoom_Scale:
                return
            Inner_W = max(1, self._Width - 2 * self._Border_Size)
            Inner_H = max(1, self._Height - 2 * self._Border_Size)
            if Inner_W<=0 or Inner_H<=0:
                self._Zoom_Scale = New_Zoom_Scale
                self.Load()
                return
            Mouse_X = Event.x
            Mouse_Y = Event.y
            Mouse_Rel_X = (Mouse_X - self._Border_Size) / Inner_W
            Mouse_Rel_Y = (Mouse_Y - self._Border_Size) / Inner_H
            Mouse_Rel_X = max(0.0, min(1.0, Mouse_Rel_X))
            Mouse_Rel_Y = max(0.0, min(1.0, Mouse_Rel_Y))
            View_W = self._Image_Width / self._Zoom_Scale
            View_H = self._Image_Height / self._Zoom_Scale
            View_Left = self._Zoom_Center[0] - View_W / 2
            View_Top = self._Zoom_Center[1] - View_H / 2
            Mouse_Abs_X = View_Left + Mouse_Rel_X * View_W
            Mouse_Abs_Y = View_Top + Mouse_Rel_Y * View_H
            New_View_W = self._Image_Width / New_Zoom_Scale
            New_View_H = self._Image_Height / New_Zoom_Scale
            New_View_Left = Mouse_Abs_X - Mouse_Rel_X * New_View_W
            New_View_Top = Mouse_Abs_Y - Mouse_Rel_Y * New_View_H
            New_Center_X = New_View_Left + New_View_W / 2
            New_Center_Y = New_View_Top + New_View_H / 2
            Half_W = New_View_W / 2
            Half_H = New_View_H / 2
            New_Center_X = max(Half_W, min(self._Image_Width - Half_W, New_Center_X))
            New_Center_Y = max(Half_H, min(self._Image_Height - Half_H, New_Center_Y))
            self._Zoom_Scale = New_Zoom_Scale
            self._Zoom_Center = (New_Center_X, New_Center_Y)
            self.Load()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Zoom -> {E}")
    
    def Reset(self, Event=False):
        try:
            self._Angle = 0
            self._Zoom_Scale = 1.0
            if self._Image:
                self._Zoom_Center = (self._Image_Width // 2, self._Image_Height // 2)
            self.Load()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Reset -> {E}")