# IMPORT LIBRARIES
import io
import base64
from PIL import Image as PIL_Image
from .N_GUI import GUI
from .N_Image import Image
from .N_Custom import Event_Bind

class Check:

    def __init__(self, Main, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Check"
            try:
                self._Config = ['Name', 'Background', 'Light_Background', 'Dark_Background', 'Border_Color', 'Light_Border_Color', 'Dark_Border_Color', 'Border_Size', 'Resize_Width', 'Resize', 'Resize_Height', 'Move', 'Move_Left', 'Move_Top', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height']
                self._Initialized = False
                self._Widget = []
                self._Name = False
                self._Last_Name = False
                self._Resize_Font, self._Resize, self._Resize_Width, self._Resize_Height, self._Move, self._Move_Left, self._Move_Top = False, True, True, True, True, True, True
                self._Image_True = "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"
                self._Image_False = "iVBORw0KGgoAAAANSUhEUgAAAYMAAAGDBAMAAAA7SmEhAAAAGFBMVEUAAAAAAAAAAAAAAAD////+/v7u7u7U1NR4psh4AAAACHRSTlP/++/4/////7Y4qEwAAAHASURBVHic7dJBDQIxAEVBDghAAhKQwAFQAFbQjwASusmy9JHMHJse/ku72wEAAAAAAD90mD1gvePsAeud3o/2l7bzuGo/e+OAhAIJBRIKJBRIKJBQIKFAQoGEAgkFEgokFEgokFAgoUBCgYQCCQUSCiQUSCiQUCChQEKBhAIJBRIKJBRIKJBQIKFAQoGEAgkFEgokFEgokFAgoUBCgYQCCQUSCiQUSCiQUCChQEKBhAIJBRIKJBRIKJBQIKFAQoGEAgkFEgokFEgokFAgoUBCgYQCCQUSCiQUSCiQUCChQEKBhAIJBRIKJBRIKJBQIKFAQoGEAgkFEgokFEgokFAgoUDC5h7jK/WE2/hKPWEBCQUSCiQUSCiQUCChQEKBhAIJBRIKJBRIKJBQIKFAQoGEAgkFEgokFEgokFAgoUBCgYQCCQUSCiQUSCiQUCChQEKBhAIJBRIKJBRIKJBQIKFAQoGEAgkFEgokFGyecL1/ZecH27/C8ys7P/CRCiQUSCiQUCChQEKBhAIJBRIKJBRIKJBQIKFAQoGEAgkFEgokFEgokFAgoUBCgYQCCQUSCiQULEj4N4fZAwAAAAAAAGZ4AU5MI+KASNT3AAAAAElFTkSuQmCC"
                self._Image = {True: self.Create_Image(self._Image_True), False: self.Create_Image(self._Image_False)}
                self._Popup = False
                self._Display = True
                self._Main = Main
                self._Frame = Image(self._Main)
                self._Frame.Config(Convert_Type='RGBA')
                self._Border_Color = '#000000'
                self._Border_Size = 0
                self._Background = self._Main._Background
                self._Background_Main = True
                self._Check = False
                self._On_Change = False
                self._On_Show = False
                self._On_Hide = False
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Check[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Check[]"
    
    def Copy(self, Name=False, Main=False):
        try:
            if not Main:
                Main = self._Main
            Instance = type(self)(Main)
            for Key in self._Config:
                setattr(Instance, "_"+Key, getattr(self, "_"+Key))
            if Name:
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
            self.Resize()
            if self._On_Show:
                self._On_Show()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Show -> {E}")
            
    def Display(self):
        try:
            self._Frame.Show()
            self._Display = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Display -> {E}")
    
    def Grab(self, Path=False):
        try:
            return self._GUI.Grab_Widget(Path=Path, Widget=self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Grab -> {E}")
            
    def Get(self):
        try:
            return self._Check
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Get -> {E}")
            
    def Set(self, Check):
        try:
            if Check!=self._Check:
                self._Check = Check
                self._Frame.Set(Path=self._Image[self._Check])
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Set -> {E}")
            
    def Set_On_Click(self):
        try:
            self._Check = not self._Check
            self._Frame.Set(Path=self._Image[self._Check])
            if self._On_Change:
                self._On_Change()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Set_On_Click -> {E}")
            
    def Widget(self):
        try:
            return self._Frame._Widget
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Widget -> {E}")
            
    def Bind(self, **Input):
        try:
            if 'On_Show' in Input:
                self._On_Show = Input['On_Show']
            if 'On_Hide' in Input:
                self._On_Hide = Input['On_Hide']
            if 'On_Change' in Input:
                self._On_Change = Input['On_Change']
            self._Frame.Bind(**Input)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Bind -> {E}")
            
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
            if self._Initialized and Run:
                self.Create()
            if "Background" in Input:
                self._Background_Main = not bool(Input["Background"])
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Config -> {E}")
            
    def Position(self, Left=None, Top=None):
        try:
            if Left is not None:
                self._Left = Left
            if Top is not None:
                self._Top = Top
            if Left is not None or Top is not None:
                self._Frame.Position(Left=Left, Top=Top)
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
                self._Frame.Size(Width=Width, Height=Height)
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
            
    def Create_Image(self, Image_Data):
        try:
            Image_Data = base64.b64decode(Image_Data)
            return PIL_Image.open(io.BytesIO(Image_Data))
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Create_Image -> {E}")
            
    def Create(self):
        try:
            if not self._Background:
                self._Background = self._Main._Background
                if not hasattr(self, "_Light_Background"):
                    setattr(self, "_Light_Background", self._Background)
                if not hasattr(self, "_Dark_Background"):
                    setattr(self, "_Dark_Background", self._GUI.Invert(self._Background))
            if not self._Initialized:
                self._GUI.Initiate_Colors(self)
                self._Width_Current, self._Height_Current, self._Left_Current, self._Top_Current, = self._Width, self._Height, self._Left, self._Top
                self._Frame.Config(Width=self._Width_Current, Height=self._Height_Current, Left=self._Left_Current, Top=self._Top_Current)
                self._Frame.Config(Background=self._Background, Border_Size=self._Border_Size, Border_Color=self._Border_Color)
                self._Frame.Config(Transparent=True)
                self._Frame.Bind(On_Click=lambda E: self.Set_On_Click())
                self._Frame.Create()
                self._Frame.Config(Convert_Type='RGBA', Pil=True)
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                self._Initialized = True
            self._Frame.Set(Path=self._Image[self._Check])
            self.Relocate()
            if self._Display:
                self.Display()
            if self._Name!=self._Last_Name:
                if self._Last_Name:
                    if self._Last_Name in self._Main.__dict__:
                        del self._Main.__dict__[self._Last_Name]
                if self._Name:
                    self._Main.__dict__[self._Name] = self
                self._Last_Name = self._Name
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Create -> {E}")
            
    def Relocate(self, Direct=False):
        try:
            self.Display()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Relocate -> {E}")
            
    def Resize(self):
        try:
            self.Relocate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Resize -> {E}")
            