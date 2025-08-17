# IMPORT LIBRARIES
import os
from io import BytesIO
from requests import get as requests_get
from PIL import Image as PIL_Image, ImageTk as PIL_ImageTk
import tkinter as TK
import threading, math, time
from .N_GUI import GUI
from .N_Frame import Frame
from .N_Canvas import Canvas
from .N_Custom import Event_Bind

PIL_Image.MAX_IMAGE_PIXELS = None       
            
class Image_Zoom:

    def __init__(self, Main, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Image_Zoom"
            try:
                self._Config = ['Name', 'Auto_Dark', 'Background', 'Light_Background', 'Dark_Background', 'Border_Color', 'Light_Border_Color', 'Dark_Border_Color', 'Border_Size', 'Resize_Width', 'Resize', 'Resize_Height', 'Move', 'Move_Left', 'Move_Top', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height', 'Path', 'Path_Initial', 'Url', 'Array', 'Pil', 'Rotate', 'Transparent', 'Hover_Background', 'Light_Hover_Background', 'Dark_Hover_Background', 'Hover_Foreground', 'Light_Hover_Foreground', 'Dark_Hover_Foreground', 'Hover_Border_Color', 'Light_Hover_Border_Color', 'Dark_Hover_Border_Color']
                self._Initialized = False
                self._Name = False
                self._Last_Name = False
                self._Resize_Font, self._Resize, self._Resize_Width, self._Resize_Height, self._Move, self._Move_Left, self._Move_Top = False, True, True, True, True, True, True
                self._Popup = False
                self._Display = True
                self._Size_Update = False
                self._Resize_Index = 0
                self._Main = Main
                self._Frame = Canvas(self._Main)
                self._Frame.Bind(On_Click = self.Drag_Start)
                self._Frame.Bind(On_Drag = self.Drag)
                self._Frame.Bind(On_Mouse_Wheel = self.Zoom)
                self._Frame.Bind(On_Right_Click = self.Reset)
                self._Border_Color = '#000000'
                self._Border_Size = 0
                self._Background = self._Main._Background
                self._Background_Main = True
                self._Hover_Background = False
                self._Hover_Border_Color = False
                self._Last_Background = False
                self._Last_Border_Color = False
                self._Image = False
                self._Image_Window = False
                self._Path = False
                self._Path_Memory = False
                self._Path_Initial = False
                self._Url = False
                self._Array = False
                self._Pil = False
                self._Rotate = 0
                self._Angle = 0
                self._Transparent = True
                self._Zoom_Scale = 1.0
                self._Zoom_Center = None
                self._Resizable = self._Main._Resizable
                self._Auto_Dark = True
                self._On_Show = False
                self._On_Hide = False
                self._On_Hover_In = False
                self._On_Hover_Out = False
                self._On_Click = False
                self._On_Drag = False
                self._On_Mouse_Wheel = False
                self._On_Right_Click = False
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Image_Zoom[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Image_Zoom[]"
    
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
            self._Main._Widget.remove(self)
            self._Frame.Delete()
            if self:
                del self
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Delete -> {E}")
            
    def Hide(self):
        try:
            self._Frame.Hide()
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
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Show -> {E}")
            
    def Display(self):
        try:
            self._Frame.Show()
            self._Frame._Frame.tag_raise(self._Image_Window)
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
            self._Frame.Animate(Widget=self._Widget)
            self.Show()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Animate -> {E}")
            self.Animate_Cancel()
            
    def Animate_Cancel(self):
        try:
            self._Frame.Animate_Cancel()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Animate_Cancel -> {E}")
            
    def Set(self, Path):
        try:
            self._Path = Path
            self._Path_Memory = self._Path
            self.Open()
            if not self._Image_Window:
                self.Relocate()
            else:
                self.Load()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Set -> {E}")
            
    def Initial(self):
        try:
            if self._Path_Initial:
                Load_Setup = [self._Array, self._Url, self._Pil]
                self._Array, self._Url, self._Pil = False, False, False
                self.Set(self._Path_Initial)
                self._Array, self._Url, self._Pil = Load_Setup
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Initial -> {E}")
            
    def Refresh(self):
        try:
            self.Open()
            self.Relocate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Refresh -> {E}")
            
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
            if 'On_Hover_In' in Input:
                self._On_Hover_In = Input['On_Hover_In']
            Input['On_Hover_In'] = lambda E: self.On_Hover_In(E)
            if 'On_Hover_Out' in Input:
                self._On_Hover_Out = Input['On_Hover_Out']
            Input['On_Hover_Out'] = lambda E: self.On_Hover_Out(E)
            if 'On_Click' in Input:
                self._On_Click = Input['On_Click']
                del Input['On_Click']
            if 'On_Drag' in Input:
                self._On_Drag = Input['On_Drag']
                del Input['On_Drag']
            if 'On_Mouse_Wheel' in Input:
                self._On_Mouse_Wheel = Input['On_Mouse_Wheel']
                del Input['On_Mouse_Wheel']
            if 'On_Right_Click' in Input:
                self._On_Right_Click = Input['On_Right_Click']
                del Input['On_Right_Click']
            self._Frame.Bind(**Input)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind -> {E}")
            
    def On_Hover_In(self, E):
        try:
            Config = {}
            if self._Hover_Background:
                self._Last_Background = self._Background
                Config['Background'] = self._Hover_Background
            if self._Hover_Border_Color:
                self._Last_Border_Color = self._Border_Color
                Config['Border_Color'] = self._Hover_Border_Color
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
            if self._Hover_Border_Color and self._Last_Border_Color:
                Config['Border_Color'] = self._Last_Border_Color if self._Border_Color==self._Hover_Border_Color else self._Border_Color
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
            self._Frame.Config(**Input)
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
                self._Frame.Position(Left=self._Left, Top=self._Top)
                self.Relocate()
            return self._Frame.Position()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Position -> {E}")
            
    def Size(self, Width=False, Height=False):
        try:
            if Width:
                self._Width = Width
            if Height:
                self._Height = Height
            if Width or Height:
                self._Frame.Size(Width=self._Width, Height=self._Height)
                self.Relocate()
            return self._Frame.Size()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Size -> {E}")
        
    def Locate(self, Width, Height, Left, Top):
        try:
            Width = self._Width*(Width/100)
            Height = self._Height*(Height/100)
            Left = self._Width*(Left/100)-self._Border_Size
            Top = self._Height*(Top/100)-self._Border_Size
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
                self._Frame.Config(Width=self._Width_Current, Height=self._Height_Current, Left=self._Left_Current, Top=self._Top_Current)
                self._Frame.Config(Background=self._Background, Border_Size=self._Border_Size, Border_Color=self._Border_Color)
                self._Frame.Create()
                self._Frame.Bind(On_Hover_In=lambda E: self.On_Hover_In(E), On_Hover_Out=lambda E: self.On_Hover_Out(E))
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                self._Initialized = True
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
            
    def Open(self):
        try:
            if self._Image:
                self._Image.close()
            if self._Url and self._Path:
                Image_Data = requests_get(self._Path)
                self._Image = PIL_Image.open(BytesIO(Image_Data.content))
            elif self._Array and self._Path is not None:
                self._Image = PIL_Image.fromarray(self._Path)
            elif self._Pil and self._Path:
                self._Image = self._Path.copy()
            elif self._Path and os.path.exists(self._Path):
                self._Image = PIL_Image.open(self._Path)
                if not self._Path_Initial:
                    self._Path_Initial = self._Path
            else:
                self._Image = None
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
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Open -> {E}")
            
    def Convert(self, Frame_Width, Frame_Height):
        try:
            if not self._Image:
                return {"Image": None, "Top": 0, "Left": 0}
            Zoom_W = self._Image_Width / self._Zoom_Scale
            Zoom_H = self._Image_Height / self._Zoom_Scale
            CX, CY = self._Zoom_Center
            CX = max(Zoom_W // 2, min(self._Image_Width - Zoom_W // 2, CX))
            CY = max(Zoom_H // 2, min(self._Image_Height - Zoom_H // 2, CY))
            self._Zoom_Center = (CX, CY)
            Left = CX - Zoom_W // 2
            Top = CY - Zoom_H // 2
            Right = Left + Zoom_W
            Bottom = Top + Zoom_H
            Crop = self._Image.crop((int(Left), int(Top), int(Right), int(Bottom)))
            if self._Transparent:
                Crop = Crop.convert("RGBA")
            Image_Width, Image_Height = Crop.size
            Image_Aspect = Image_Width / Image_Height
            Frame_Aspect = Frame_Width / Frame_Height
            if Image_Aspect > Frame_Aspect:
                New_Width = int(Frame_Width)
                New_Height = int(Frame_Width / Image_Aspect)
            else:
                New_Height = int(Frame_Height)
                New_Width = int(Frame_Height * Image_Aspect)
            Crop = Crop.resize((New_Width, New_Height), PIL_Image.NEAREST)
            Left = (Frame_Width - New_Width) // 2
            Top = (Frame_Height - New_Height) // 2
            Crop_TK = PIL_ImageTk.PhotoImage(Crop)
            return {"Image": Crop_TK, "Top": Top, "Left": Left}
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Convert -> {E}")
            return {"Image": None, "Top": 0, "Left": 0}
            
    def Load(self):
        try:
            if self._Height_Current > 0 and self._Width_Current > 0:
                Image = self.Convert(self._Width_Current, self._Height_Current)
                if Image["Image"] is None:
                    return
                if not self._Image_Window:
                    self._Image_Window = self._Frame._Frame.create_image(Image['Left'], Image['Top'], image=Image['Image'], anchor='nw')
                    self._Frame._Frame.Temp_Image = Image['Image']
                else:
                    self._Frame._Frame.itemconfig(self._Image_Window, image=Image['Image'])
                    self._Frame._Frame.coords(self._Image_Window, Image['Left'], Image['Top'])
                    self._Frame._Frame.Temp_Image = Image['Image']
                self._Frame._Frame.itemconfigure(self._Image_Window, state='normal')
                self._Frame._Frame.tag_raise(self._Image_Window)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Load -> {E}")
                
    def Drag_Start(self, Event):
        try:
            self._Drag_Last_X = self._Frame._Frame.canvasx(Event.x)
            self._Drag_Last_Y = self._Frame._Frame.canvasy(Event.y)
            if self._On_Click:
                self._On_Click(Event)
        except Exception:
            self._Drag_Last_X, self._Drag_Last_Y = 0, 0
            
    def Drag(self, Event):
        try:
            if not self._Image:
                return
            Curr_X = self._Frame._Frame.canvasx(Event.x)
            Curr_Y = self._Frame._Frame.canvasy(Event.y)
            Delta_X = Curr_X - self._Drag_Last_X
            Delta_Y = Curr_Y - self._Drag_Last_Y
            self._Drag_Last_X = Curr_X
            self._Drag_Last_Y = Curr_Y
            View_W = self._Image_Width / self._Zoom_Scale
            View_H = self._Image_Height / self._Zoom_Scale
            Move_X_Img = -Delta_X * (View_W / self._Width_Current)
            Move_Y_Img = -Delta_Y * (View_H / self._Height_Current)
            New_CX = self._Zoom_Center[0] + Move_X_Img
            New_CY = self._Zoom_Center[1] + Move_Y_Img
            Half_W = View_W / 2
            Half_H = View_H / 2
            New_CX = max(Half_W, min(self._Image_Width - Half_W, New_CX))
            New_CY = max(Half_H, min(self._Image_Height - Half_H, New_CY))
            self._Zoom_Center = (New_CX, New_CY)
            self.Load()
            if self._On_Drag:
                self._On_Drag(Event)
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
            CanvasX = self._Frame._Frame.canvasx(Event.x)
            CanvasY = self._Frame._Frame.canvasy(Event.y)
            Img_X, Img_Y = self._Frame._Frame.coords(self._Image_Window)
            Mouse_Rel_X = (CanvasX - Img_X) / self._Width_Current
            Mouse_Rel_Y = (CanvasY - Img_Y) / self._Height_Current
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
            if self._On_Mouse_Wheel:
                self._On_Mouse_Wheel(Event)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Zoom -> {E}")

    def Reset(self, Event=False):
        try:
            self._Angle = 0
            self._Zoom_Scale = 1.0
            if self._Image:
                self._Zoom_Center = (self._Image_Width // 2, self._Image_Height // 2)
            self.Relocate()
            if self._On_Right_Click:
                self._On_Right_Click(Event)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Reset -> {E}")
            
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
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Relocate -> {E}")
            
    def Resize(self):
        try:
            self._Resize_Index = self._GUI._Resize_Index
            self.Relocate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Resize -> {E}")