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

class Image_Open:

    def __init__(self):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = 'Image_Open'
            try:
                self._Config = ['Path', 'Rotate', 'Transparent', 'Aspect_Ratio']
                self._Image = False
                self._Path = False
                self._Path_Memory = False
                self._Rotate = 0
                self._Transparent = True
                self._Aspect_Ratio = True
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Image_Open[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Image_Open[]"
            
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
            for Each in self._Config:
                if Each in Input:
                    Value = Input[Each]
                    setattr(self, "_"+Each, Value)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Config -> {E}")
                
    def Open(self, Path=False):
        try:
            if Path is not False:
                self._Path = Path
            if self._Image:
                try:
                    self._Image.close()
                except:
                    pass
            self._Image = False
            Path_Obj = self._Path
            if isinstance(Path_Obj, PIL_Image.Image):
                self._Image = Path_Obj.copy()
            elif hasattr(Path_Obj, "__class__") and getattr(type(Path_Obj), "__module__", "").startswith("numpy"):
                self._Image = PIL_Image.fromarray(Path_Obj)
            elif isinstance(Path_Obj, str):
                Parsed = urllib.parse.urlparse(Path_Obj)
                if Parsed.scheme in ("http", "https"):
                    with urllib.request.urlopen(Path_Obj) as Response:
                        Data = Response.read()
                    self._Image = PIL_Image.open(BytesIO(Data))
                elif os.path.exists(Path_Obj):
                    self._Image = PIL_Image.open(Path_Obj)
                    if not getattr(self, "_Path_Initial", None):
                        self._Path_Initial = Path_Obj
                else:
                    self._Image = False
            else:
                self._Image = False
            if self._Image:
                self._Image_Width, self._Image_Height = self._Image.size
            else:
                self._Widget.configure(image=None)
                self._Widget.image=None
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Open -> {E}")
            
    def Get(self, Width=False, Height=False):
        try:
            Temp_Image = self._Image.rotate(self._Rotate, PIL_Image.NEAREST, expand=0)
            if Width and Height:
                Frame_Width = Width
                Frame_Height = Height
                Temp_Image = self._Image.rotate(self._Rotate, PIL_Image.NEAREST, expand=0)
                Image_Ratio = self._Image_Width / self._Image_Height
                Frame_Ratio = Frame_Width / Frame_Height
                if Image_Ratio>=Frame_Ratio:
                    Width = Frame_Width
                    Width_Ratio = Width / self._Image_Width
                    Height = self._Image_Height * Width_Ratio
                    self.Top = (Frame_Height - Height) / 2
                    self.Left = 0
                if Image_Ratio<Frame_Ratio:
                    Height = Frame_Height
                    Height_Ratio = Height / self._Image_Height
                    Width = self._Image_Width * Height_Ratio
                    self.Top = 0
                    self.Left = (Frame_Width - Width) / 2
                if self._Aspect_Ratio:
                    Temp_Image = Temp_Image.resize((int(Width), int(Height)), PIL_Image.NEAREST)
                else:
                    Temp_Image = Temp_Image.resize((int(self._Width_Current), int(self._Height_Current)), PIL_Image.NEAREST)
            if self._Transparent:
                Temp_Image = Temp_Image.convert("RGBA")
            Temp_Image = PIL_ImageTk.PhotoImage(Temp_Image)
            return Temp_Image
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get -> {E}")
