# IMPORT LIBRARIES
import io
import base64
from PIL import Image as PIL_Image
from .N_GUI import GUI
from .N_Image_Lite import Image_Lite
from .N_Custom import Event_Bind

def Create_Image(Image_Data):
    try:
        Image_Data = base64.b64decode(Image_Data)
        return PIL_Image.open(io.BytesIO(Image_Data))
    except:
        pass

Image_True = Create_Image("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")
Image_False = Create_Image("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")
           
class Switch:

    def __init__(self, Main, *args, **kwargs):
        self._GUI = GUI._Instance
        if self._GUI is not None:
            self._Type = "Switch"
            try:
                self._Config = ['Name', 'Auto_Dark', 'Background', 'Light_Background', 'Dark_Background', 'Resize_Width', 'Resize', 'Resize_Height', 'Move', 'Move_Left', 'Move_Top', 'Popup', 'Display', 'Left', 'Top', 'Width', 'Height']
                self._Initialized = False
                self._Widget = []
                self._Name = False
                self._Last_Name = False
                self._Resize_Font, self._Resize, self._Resize_Width, self._Resize_Height, self._Move, self._Move_Left, self._Move_Top = False, True, True, True, True, True, True
                self._Image = {True: Image_True, False: Image_False}
                self._Popup = False
                self._Display = True
                self._Size_Update = False
                self._Resize_Index = 0
                self._Main = Main
                self._Frame = Image_Lite(self._Main)
                self._Frame.Config(Convert_Type='RGBA')
                self._Border_Color = '#000000'
                self._Border_Size = 0
                self._Background = self._Main._Background
                self._Background_Main = True
                self._Auto_Dark = True
                self._Check = False
                self._Resizable = self._Main._Resizable
                self._On_Change = False
                self._On_Show = False
                self._On_Hide = False
            except Exception as E:
                self._GUI.Error(f"{self._Type} -> Init -> {E}")
        else:
            print("Error: Gluonix -> GUI Instance Has Not Been Created")

    def __str__(self):
        return "Nucleon_Glunoix_Switch[]"

    def __repr__(self):
        return "Nucleon_Glunoix_Switch[]"
    
    def Copy(self, Name=False, Main=False):
        try:
            if not Main:
                Main = self._Main
            Instance = type(self)(Main)
            for Key in self._Config:
                if hasattr(self, "_"+Key):
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
            self._Display = True
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Display -> {E}")
    
    def Grab(self, Path=False):
        try:
            return self._GUI.Grab_Widget(Path=Path, Widget=self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Grab -> {E}")
            
    def Animate(self):
        try:
            self._Frame.Animate()
            self.Show()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Animate -> {E}")
            self.Animate_Cancel()
            
    def Animate_Cancel(self):
        try:
            self._Frame.Animate_Cancel()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Animate_Cancel -> {E}")
            
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
            if "Width" in Input or "Height" in Input:
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
                self._Frame.Config(Background=self._Background, Aspect_Ratio=False)
                self._Frame.Config(Transparent=True, Use_Foreground=True)
                self._Frame.Bind(On_Click=lambda E: self.Set_On_Click())
                self._Frame.Create()
                self._Frame.Config(Convert_Type='RGBA', Pil=True)
                if not self._Display:
                    self.Hide()
                self._Main._Widget.append(self)
                self._Initialized = True
            self._Frame.Set(Path=self._Image[self._Check])
            self.Resize()
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
            
    def Update_Color(self):
        try:
            self._GUI.Initiate_Colors(self)
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Update_Color -> {E}")
            
    def Relocate(self, Direct=False):
        try:
            self.Display()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Relocate -> {E}")
            
    def Resize(self):
        try:
            self._Resize_Index = self._GUI._Resize_Index
            self.Relocate()
        except Exception as E:
            self._GUI.Error(f"{self._Type} -> Resize -> {E}")
            